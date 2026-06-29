"""設定・定数管理."""

import os
import platform
from pathlib import Path

# Dropbox App Key（PKCE方式）
# 環境変数 SHARE_APP_KEY があればそれを優先（個人検証用に自分のアプリキーを使える）。
DROPBOX_APP_KEY = os.environ.get("SHARE_APP_KEY", "ucgn1atuk1amz9l")

# Dropbox API 設定
DEFAULT_SCOPES = [
    "sharing.write",
    "sharing.read",
    "files.content.read",
    "files.content.write",
]

TOKEN_FILENAME = "token.json"
APP_DIR_NAME = "share-cli"


def get_data_dir() -> Path:
    """XDG Base Directory 準拠のデータディレクトリを返す."""
    system = platform.system()
    if system == "Windows":
        import os

        base = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
    elif system == "Darwin":
        base = Path.home() / "Library" / "Application Support"
    else:
        import os

        base = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
    return base / APP_DIR_NAME


def get_token_path() -> Path:
    """トークンファイルのフルパスを返す."""
    return get_data_dir() / TOKEN_FILENAME
