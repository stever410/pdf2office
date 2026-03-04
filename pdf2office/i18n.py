"""Locale-based i18n. Use detect_lang() for the default, STRINGS[lang] for lookups."""

import locale

STRINGS = {
    "vn": {
        "file_label":       "File PDF:",
        "browse_btn":       "Chọn file…",
        "format_label":     "Định dạng xuất",
        "convert_btn":      "Chuyển đổi",
        "status_initial":   "Chọn file PDF để bắt đầu.",
        "status_ready":     "Sẵn sàng. Chọn định dạng và nhấn Chuyển đổi.",
        "status_converting": "Đang chuyển đổi…",
        "status_no_tables": "Không tìm thấy bảng nào trong file PDF.",
        "status_done":      "Xuất thành công ở thư mục \"{name}\".",
        "status_error":     "Lỗi: {msg}",
        "browse_title":     "Chọn file PDF",
        "all_files":        "Tất cả file",
        "save_title":       "Lưu file",
        "error_title":      "Lỗi",
        "menu_language":    "Ngôn ngữ",
        "menu_help":        "Trợ giúp",
        "menu_check_updates": "Kiểm tra cập nhật…",
        "updates_title":    "Cập nhật",
        "updates_not_configured": "Chưa cấu hình kho GitHub. Hãy đặt APP_GITHUB_REPO trong metadata.py.",
        "updates_none":     "Bạn đang dùng phiên bản mới nhất (v{version}).",
        "updates_checking_error": "Không thể kiểm tra cập nhật: {msg}",
        "updates_prompt_download": "Có phiên bản mới v{latest} (hiện tại: v{current}).\nTệp: {asset}\n\nBạn có muốn tải ngay không?",
        "updates_prompt_open_page": "Có phiên bản mới v{latest} (hiện tại: v{current}).\nKhông tìm thấy tệp cài đặt phù hợp cho hệ điều hành này.\n\nMở trang phát hành?",
        "updates_release_notes": "Ghi chú phát hành",
        "updates_downloaded": "Đã tải bản cập nhật về:\n{path}\n\nMở ngay bây giờ?",
        "updates_downloaded_installer": "Đã tải gói cài đặt về:\n{path}\n\nKhởi chạy cài đặt ngay bây giờ? Ứng dụng sẽ đóng.",
        "updates_download_error": "Tải bản cập nhật thất bại: {msg}",
        "updates_open_error": "Không thể mở tệp đã tải: {msg}",
        "status_checking_updates": "Đang kiểm tra cập nhật…",
        "status_downloading_update": "Đang tải bản cập nhật: {name}…",
        "status_update_downloaded": "Đã tải xong bản cập nhật: {name}",
    },
    "en": {
        "file_label":       "PDF File:",
        "browse_btn":       "Browse…",
        "format_label":     "Output Format",
        "convert_btn":      "Convert",
        "status_initial":   "Select a PDF file to get started.",
        "status_ready":     "Ready. Choose a format and click Convert.",
        "status_converting": "Converting…",
        "status_no_tables": "No tables found in the PDF.",
        "status_done":      "Exported successfully to \"{name}\".",
        "status_error":     "Error: {msg}",
        "browse_title":     "Select PDF",
        "all_files":        "All files",
        "save_title":       "Save File",
        "error_title":      "Error",
        "menu_language":    "Language",
        "menu_help":        "Help",
        "menu_check_updates": "Check for Updates…",
        "updates_title":    "Updates",
        "updates_not_configured": "GitHub repository is not configured. Set APP_GITHUB_REPO in metadata.py.",
        "updates_none":     "You are using the latest version (v{version}).",
        "updates_checking_error": "Could not check for updates: {msg}",
        "updates_prompt_download": "A new version is available: v{latest} (current: v{current}).\nAsset: {asset}\n\nDo you want to download it now?",
        "updates_prompt_open_page": "A new version is available: v{latest} (current: v{current}).\nNo compatible installer asset was found for this OS.\n\nOpen the release page?",
        "updates_release_notes": "Release notes",
        "updates_downloaded": "Update downloaded to:\n{path}\n\nOpen it now?",
        "updates_downloaded_installer": "Installer downloaded to:\n{path}\n\nLaunch installer now? The app will close.",
        "updates_download_error": "Failed to download update: {msg}",
        "updates_open_error": "Could not open downloaded file: {msg}",
        "status_checking_updates": "Checking for updates…",
        "status_downloading_update": "Downloading update: {name}…",
        "status_update_downloaded": "Update downloaded: {name}",
    },
}


def detect_lang() -> str:
    try:
        code = locale.getdefaultlocale()[0] or ""
    except Exception:
        code = ""
    return "vn" if code.startswith("vi") else "en"
