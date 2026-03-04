#!/usr/bin/env bash
set -euo pipefail

if [[ "$(uname -s)" != "Darwin" ]]; then
  echo "This script must be run on macOS."
  exit 1
fi

"$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/build_posix.sh"
