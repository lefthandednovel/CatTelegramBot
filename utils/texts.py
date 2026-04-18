from pathlib import Path
from config import TEXTS_DIR

def load_text(filename: str) -> str:
    file_path = TEXTS_DIR / filename
    try:
        return file_path.read_text(encoding="UTF-8")
    except FileNotFoundError:
        print("Ошибка: файл отсутствует, невозможно прочитать")
    except Exception as e:
        return f"Ошибка {e}"
    
