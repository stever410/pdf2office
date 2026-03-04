import json
import os
import re
import subprocess
import sys
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Callable


@dataclass(frozen=True)
class ReleaseAsset:
    name: str
    url: str
    size: int


@dataclass(frozen=True)
class ReleaseInfo:
    version: str
    tag_name: str
    html_url: str
    body: str
    asset: ReleaseAsset | None


class GitHubReleaseUpdater:
    _NON_BINARY_SUFFIXES = (
        ".txt",
        ".sha256",
        ".sha512",
        ".sig",
        ".asc",
        ".json",
        ".yml",
        ".yaml",
        ".md",
    )
    _BINARY_SUFFIXES = (
        ".exe",
        ".msi",
        ".dmg",
        ".pkg",
        ".appimage",
        ".deb",
        ".rpm",
        ".zip",
        ".tar.gz",
        ".tar.xz",
        ".tar.bz2",
    )

    def __init__(self, repo: str, current_version: str, timeout_sec: int = 6):
        self._repo = repo.strip()
        self._current_version = current_version.strip()
        self._timeout_sec = max(2, int(timeout_sec))

    def check_for_update(self) -> ReleaseInfo | None:
        release = self._fetch_latest_release()
        if self._compare_versions(release.version, self._current_version) <= 0:
            return None
        return release

    def download_release_asset(
        self,
        release: ReleaseInfo,
        dest_dir: Path,
        progress_cb: Callable[[int, int], None] | None = None,
    ) -> Path:
        if not release.asset:
            raise ValueError("No compatible release asset was found.")

        dest_dir.mkdir(parents=True, exist_ok=True)
        out_path = dest_dir / release.asset.name

        req = urllib.request.Request(
            release.asset.url,
            headers={"Accept": "application/octet-stream", "User-Agent": "pdf2office-updater"},
        )
        with urllib.request.urlopen(req, timeout=self._timeout_sec) as response:
            total = int(response.headers.get("Content-Length") or 0)
            downloaded = 0
            with open(out_path, "wb") as file:
                while True:
                    chunk = response.read(64 * 1024)
                    if not chunk:
                        break
                    file.write(chunk)
                    downloaded += len(chunk)
                    if progress_cb:
                        progress_cb(downloaded, total)
        return out_path

    @staticmethod
    def open_download(path: Path):
        if sys.platform == "win32":
            os.startfile(str(path))  # type: ignore[attr-defined]
            return
        if sys.platform == "darwin":
            subprocess.Popen(["open", str(path)])
            return
        subprocess.Popen(["xdg-open", str(path)])

    def _fetch_latest_release(self) -> ReleaseInfo:
        if not self._repo:
            raise ValueError("GitHub repo is not configured.")

        url = f"https://api.github.com/repos/{self._repo}/releases/latest"
        req = urllib.request.Request(
            url,
            headers={"Accept": "application/vnd.github+json", "User-Agent": "pdf2office-updater"},
        )
        with urllib.request.urlopen(req, timeout=self._timeout_sec) as response:
            data = json.loads(response.read().decode("utf-8"))

        tag_name = str(data.get("tag_name", "")).strip()
        html_url = str(data.get("html_url", "")).strip()
        body = str(data.get("body", "") or "")
        version = self._extract_version(tag_name) or self._extract_version(str(data.get("name", "")))
        if not version:
            raise ValueError("Could not parse release version from GitHub tag.")

        assets = data.get("assets", [])
        parsed_assets = []
        for asset in assets:
            name = str(asset.get("name", "")).strip()
            dl_url = str(asset.get("browser_download_url", "")).strip()
            size = int(asset.get("size", 0) or 0)
            if not name or not dl_url:
                continue
            parsed_assets.append(ReleaseAsset(name=name, url=dl_url, size=size))

        return ReleaseInfo(
            version=version,
            tag_name=tag_name,
            html_url=html_url,
            body=body,
            asset=self._pick_best_asset(parsed_assets),
        )

    @classmethod
    def _extract_version(cls, value: str) -> str:
        clean = value.strip()
        if clean.lower().startswith("v"):
            clean = clean[1:]
        match = re.search(r"\d+(?:\.\d+)+", clean)
        if match:
            return match.group(0)
        return ""

    @classmethod
    def _compare_versions(cls, left: str, right: str) -> int:
        l = cls._version_parts(left)
        r = cls._version_parts(right)
        max_len = max(len(l), len(r))
        l += [0] * (max_len - len(l))
        r += [0] * (max_len - len(r))
        if l > r:
            return 1
        if l < r:
            return -1
        return 0

    @staticmethod
    def _version_parts(version: str) -> list[int]:
        return [int(part) for part in re.findall(r"\d+", version)] or [0]

    def _pick_best_asset(self, assets: list[ReleaseAsset]) -> ReleaseAsset | None:
        valid_assets = [asset for asset in assets if self._is_binary_asset(asset.name)]
        if not valid_assets:
            return None

        return max(valid_assets, key=lambda asset: self._score_asset(asset.name))

    def _is_binary_asset(self, name: str) -> bool:
        lower = name.lower()
        if lower.endswith(self._NON_BINARY_SUFFIXES):
            return False
        return lower.endswith(self._BINARY_SUFFIXES)

    def _score_asset(self, name: str) -> int:
        lower = name.lower()
        score = 0

        platform = self._platform_name()
        target_keywords = self._platform_keywords(platform)
        other_keywords = self._platform_keywords("all") - target_keywords

        if any(keyword in lower for keyword in target_keywords):
            score += 40
        if any(keyword in lower for keyword in other_keywords):
            score -= 35

        for ext in self._preferred_extensions(platform):
            if lower.endswith(ext):
                score += 20

        if lower.endswith(".zip"):
            score += 10
        if "installer" in lower or "setup" in lower:
            score += 5
        return score

    @staticmethod
    def _platform_name() -> str:
        if sys.platform.startswith("win"):
            return "windows"
        if sys.platform == "darwin":
            return "macos"
        return "linux"

    @staticmethod
    def _platform_keywords(platform: str) -> set[str]:
        keywords = {
            "windows": {"win", "windows"},
            "macos": {"mac", "macos", "darwin", "osx"},
            "linux": {"linux"},
        }
        if platform == "all":
            return set().union(*keywords.values())
        return keywords[platform]

    @staticmethod
    def _preferred_extensions(platform: str) -> tuple[str, ...]:
        if platform == "windows":
            return (".exe", ".msi")
        if platform == "macos":
            return (".dmg", ".pkg")
        return (".appimage", ".deb", ".rpm", ".tar.gz")
