import json
import os


class FileManager:
    def __init__(self, file_path="data/transactions.json"):
        self.file_path = file_path
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as f:
                f.write("[]")

    def write_data(self, data):
        with open(self.file_path, "w", encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)
            f.write("\n")

    def read_data(self):
        try:
            with open(self.file_path, "r", encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []