import json
import os
from typing import List, Any
import logging
import shutil


class FileManager:
    def __init__(self, file_path="data/transactions.json"):
        self.file_path = file_path
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as f:
                json.dump([], f)

    def write_data(self, data: List[dict]) -> None:
        temp_file = self.file_path + ".tmp"
        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)

        os.replace(temp_file, self.file_path)

    def read_data(self) -> List[dict]:
        try:
            with open(self.file_path, "r", encoding='utf-8') as f:
                return json.load(f)

        except FileNotFoundError:
            return []

        except json.JSONDecodeError:
            logging.warning("transactions.json corrupted, resetting it")
            shutil.copy(self.file_path, self.file_path + ".bak")
            self.write_data([])
            return []