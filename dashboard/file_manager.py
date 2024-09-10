import json
import os


class FileManager:
    @staticmethod
    def load_json(file_path: str) -> dict:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return json.load(f)
        return {}

    @staticmethod
    def save_json(file_path: str, data: dict) -> None:
        dir_name = os.path.dirname(file_path)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        with open(file_path, 'w') as f:
            json.dump(data, f)

    @staticmethod
    def load_file(file_path: str, default_content: str = None) -> str:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return f.read()
        return default_content or ""

    @staticmethod
    def save_file(file_path: str, content: str) -> None:
        with open(file_path, 'w') as f:
            f.write(content)
