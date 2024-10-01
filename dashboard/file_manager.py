import json
import logging
import os


class FileManager:
    @staticmethod
    def load_json(file_path: str) -> dict:
        logging.debug(f"Loading JSON file: {file_path}")
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return json.load(f)

        logging.warning(f"File {file_path} does not exist. Returning empty dictionary.")
        return {}

    @staticmethod
    def save_json(file_path: str, data: dict) -> None:
        logging.debug(f"Saving JSON to file: {file_path}")
        dir_name = os.path.dirname(file_path)
        if not os.path.exists(dir_name):
            logging.debug(f"Directory {dir_name} does not exist. Creating it.")
            os.makedirs(dir_name)
        with open(file_path, 'w') as f:
            json.dump(data, f)

    @staticmethod
    def load_file(file_path: str, default_content: str = None) -> str:
        logging.debug(f"Loading file: {file_path}")
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return f.read()

        logging.warning(f"File {file_path} does not exist. Returning default content.")
        return default_content or ""

    @staticmethod
    def save_file(file_path: str, content: str) -> None:
        logging.debug(f"Saving content to file: {file_path}")
        with open(file_path, 'w') as f:
            f.write(content)
