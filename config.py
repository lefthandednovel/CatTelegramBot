import os
from pathlib import Path

BASE_DIR = Path(__file__).parent
TEXTS_DIR = BASE_DIR / "txt_files"

BOT_TOKEN = open(TEXTS_DIR / "bot_token.txt").read()

CAT_API_LIMIT_MAX = 10
CAT_API_TIMEOUT = 10

