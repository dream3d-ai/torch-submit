import os
from dataclasses import dataclass
from typing import Dict, List

import yaml


@dataclass
class Database:
    address: str
    port: int

    @classmethod
    def from_db(cls, row: str):
        address, port = row.split(":")
        return cls(
            address,
            int(port),
        )

    def to_db(self):
        return f"{self.address}:{self.port}"

    def __str__(self):
        return f"Database(address={self.address}, port={self.port})"

    def __hash__(self):
        return hash(self.address) + hash(self.port)

    def __eq__(self, other):
        if not isinstance(other, Database):
            return NotImplemented
        return self.address == other.address and self.port == other.port


class DatabaseConfig:
    def __init__(self):
        self.config_path = os.path.expanduser("~/.cache/torch-submit/db_config.yaml")
        self.databases: Dict[str, Database] = {}
        self.load_config()

    def load_config(self):
        if not os.path.exists(self.config_path):
            return

        with open(self.config_path, "r") as f:
            config = yaml.safe_load(f) or {}

        for database_name, database_data in config.get("databases", {}).items():
            database = Database(**database_data)
            self.databases[database_name] = database

    def save_config(self):
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        config = {"clusters": {}}
        for database_name, database in self.databases.items():
            config["databases"][database_name] = {
                "address": database.address,
                "port": database.port,
            }
        with open(self.config_path, "w") as f:
            yaml.dump(config, f)

    def add_db(self, name: str, address: str, port: int):
        self.databases[name] = Database(address, port)
        self.save_config()

    def remove_db(self, name: str):
        if name in self.databases:
            del self.databases[name]
            self.save_config()

    def get_db(self, db_name: str) -> Database:
        if db_name not in self.databases:
            raise ValueError(f"Database '{db_name}' not found in config")
        return self.databases[db_name]

    def list_dbs(self) -> List[str]:
        return list(self.databases.keys())

    def update_db(self, name: str, address: str, port: int):
        if name not in self.databases:
            raise ValueError(f"Database '{name}' not found in config")
        self.databases[name] = Database(address, port)
        self.save_config()
