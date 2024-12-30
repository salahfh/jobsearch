import functools
import hashlib
from pathlib import Path
from abc import ABC, abstractmethod
import json


class DataIntegrityException(Exception):
    pass


class Repository(ABC):
    def __init__(self, connection: dict):
        self.connection = connection

    @abstractmethod
    def read(self, key: str) -> dict:
        pass

    @abstractmethod
    def write(self, value: dict) -> str:
        pass

    @abstractmethod
    def read_all(self) -> list[dict]:
        pass

    def hash_value(self, value) -> str:
        return hashlib.sha256(value.encode("utf-8")).hexdigest()


class FileRepository(Repository):
    def __init__(self, connection):
        self.filepath: Path = Path(connection.get("filepath"))
        self.key: str = connection.get("key", "url")
        self.setup()

    def setup(self):
        if not self.filepath.exists():
            self.filepath.touch()

    @functools.cache
    def get_id(self, id: str) -> dict:
        with open(self.filepath) as f:
            for line in f:
                data = json.loads(line.strip())
                if data.get("id") == id:
                    return data
        return {}
    
    def read(self, key_value: str):
        id = self.hash_value(key_value)
        return self.get_id(id)

    def write(self, data: dict) -> str:
        key_hash = self.hash_value(data.get(self.key))
        data["id"] = key_hash

        if self.get_id(key_hash) != {}:
            raise DataIntegrityException(
                f"Cannot insert {data.get(self.key)} into data. It's already added."
            )

        value_str = json.dumps(data, separators=(",", ":"))
        with open(self.filepath, "a") as f:
            f.write(value_str + "\n")
        return key_hash
    
    def read_all(self):
        items = []
        with open(self.filepath) as f:
            for line in f:
                data = json.loads(line.strip())
                items.append(data)
        return items
