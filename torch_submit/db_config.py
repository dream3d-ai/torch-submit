import os
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List

import yaml


class DatabaseType(str, Enum):
    POSTGRES = "postgres"
    MYSQL = "mysql"


@dataclass
class Database:
    address: str
    port: int
    username: str
    password: str | None = None
    type: DatabaseType = DatabaseType.POSTGRES

    @classmethod
    def from_db(cls, row: str):
        address, port, username, password, type = row.split(":")
        return cls(
            address,
            int(port),
            username,
            password or None,
            DatabaseType(type),
        )

    def to_uri(self):
        return f"{self.type}://{self.username}:{self.password}@{self.address}:{self.port}"

    def to_db(self):
        return f"{self.address}:{self.port}:{self.username}:{self.password or ''}:{self.type.value}"

    def __str__(self):
        return f"Database(type={self.type}, address={self.address}, port={self.port}, username={self.username}, password=****)"

    def __hash__(self):
        return (
            hash(self.type)
            + hash(self.address)
            + hash(self.port)
            + hash(self.username)
            + hash(self.password)
        )

    def __eq__(self, other):
        if not isinstance(other, Database):
            return NotImplemented
        return self.address == other.address and self.port == other.port and self.type == other.type


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
                "username": database.username,
                "password": database.password,
            }
        with open(self.config_path, "w") as f:
            yaml.dump(config, f)

    def add_db(self, type: DatabaseType, name: str, address: str, port: int):
        self.databases[name] = Database(address, port, type=type)
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

    def update_db(
        self, type: str, name: str, address: str, port: int, username: str, password: str
    ):
        if name not in self.databases:
            raise ValueError(f"Database '{name}' not found in config")
        self.databases[name] = Database(address, port, username, password, DatabaseType(type))
        self.save_config()
