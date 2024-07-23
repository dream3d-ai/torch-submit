import os
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional

import yaml


@dataclass
class Node:
    public_ip: str
    private_ip: Optional[str]
    num_gpus: int
    nproc: int
    ssh_user: Optional[str]
    ssh_pub_key_path: Optional[str]

    def __post_init__(self):
        self.private_ip = self.private_ip or None
        self.ssh_user = self.ssh_user or None
        self.ssh_pub_key_path = self.ssh_pub_key_path or None
        self.num_gpus = int(self.num_gpus)
        self.nproc = int(self.nproc)

    @classmethod
    def from_db(cls, row: str):
        public_ip, private_ip, num_gpus, nproc, ssh_user, ssh_pub_key_path = row.split(
            ":"
        )
        return cls(
            public_ip,
            private_ip if private_ip != "None" else None,
            int(num_gpus),
            int(nproc),
            ssh_user if ssh_user != "None" else None,
            ssh_pub_key_path if ssh_pub_key_path != "None" else None,
        )

    def to_db(self):
        return f"{self.public_ip}:{self.private_ip or 'None'}:{self.num_gpus}:{self.nproc}:{self.ssh_user or 'None'}:{self.ssh_pub_key_path or 'None'}"

    def __str__(self):
        return f"Node(public_ip={self.public_ip}, private_ip={self.private_ip}, num_gpus={self.num_gpus}, nproc={self.nproc}, ssh_user={self.ssh_user}, ssh_pub_key_path={self.ssh_pub_key_path})"

    def __hash__(self):
        return hash(self.public_ip)

    def __eq__(self, other):
        if not isinstance(other, Node):
            return NotImplemented
        return self.public_ip == other.public_ip


@dataclass
class Cluster:
    head_node: Node
    worker_nodes: List[Node]


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

    def __post_init__(self):
        self.port = int(self.port)
        self.type = DatabaseType(self.type)

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
        return (
            f"{self.type}://{self.username}:{self.password}@{self.address}:{self.port}"
        )

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
        return (
            self.address == other.address
            and self.port == other.port
            and self.type == other.type
        )


class Config:
    def __init__(self):
        self.config_path = os.path.expanduser("~/.cache/torch-submit/config.yaml")
        self.clusters: Dict[str, Cluster] = {}
        self.databases: Dict[str, Database] = {}
        self.load_config()

    def load_config(self):
        if not os.path.exists(self.config_path):
            return

        with open(self.config_path, "r") as f:
            config = yaml.safe_load(f) or {}

        for cluster_name, cluster_data in config.get("clusters", {}).items():
            head_node = Node(**cluster_data["head_node"])
            worker_nodes = [Node(**node) for node in cluster_data["worker_nodes"]]
            self.clusters[cluster_name] = Cluster(head_node, worker_nodes)

        for database_name, database_data in config.get("databases", {}).items():
            database = Database(**database_data)
            self.databases[database_name] = database

    def save_config(self):
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        config = {"clusters": {}, "databases": {}}

        for cluster_name, cluster in self.clusters.items():
            config["clusters"][cluster_name] = {
                "head_node": {
                    "public_ip": cluster.head_node.public_ip,
                    "private_ip": cluster.head_node.private_ip or None,
                    "num_gpus": cluster.head_node.num_gpus,
                    "nproc": cluster.head_node.nproc,
                    "ssh_user": cluster.head_node.ssh_user or None,
                    "ssh_pub_key_path": cluster.head_node.ssh_pub_key_path or None,
                },
                "worker_nodes": [
                    {
                        "public_ip": node.public_ip,
                        "private_ip": node.private_ip or None,
                        "num_gpus": node.num_gpus,
                        "nproc": node.nproc,
                        "ssh_user": node.ssh_user or None,
                        "ssh_pub_key_path": node.ssh_pub_key_path or None,
                    }
                    for node in cluster.worker_nodes
                ],
            }

        for database_name, database in self.databases.items():
            config["databases"][database_name] = {
                "address": database.address,
                "port": database.port,
                "username": database.username,
                "password": database.password,
                "type": database.type.value,
            }

        with open(self.config_path, "w") as f:
            yaml.dump(config, f)

    # Cluster methods
    def add_cluster(self, name: str, head_node: Node, worker_nodes: List[Node]):
        self.clusters[name] = Cluster(head_node, worker_nodes)
        self.save_config()

    def remove_cluster(self, name: str):
        if name in self.clusters:
            del self.clusters[name]
            self.save_config()

    def get_cluster(self, cluster_name: str) -> Cluster:
        if cluster_name not in self.clusters:
            raise ValueError(f"Cluster '{cluster_name}' not found in config")
        return self.clusters[cluster_name]

    def list_clusters(self) -> List[str]:
        return list(self.clusters.keys())

    def add_worker_node(self, cluster_name: str, worker_node: Node):
        if cluster_name not in self.clusters:
            raise ValueError(f"Cluster '{cluster_name}' not found in config")
        self.clusters[cluster_name].worker_nodes.append(worker_node)
        self.save_config()

    def remove_worker_node(self, cluster_name: str, worker_node_ip: str):
        if cluster_name not in self.clusters:
            raise ValueError(f"Cluster '{cluster_name}' not found in config")
        self.clusters[cluster_name].worker_nodes = [
            node
            for node in self.clusters[cluster_name].worker_nodes
            if node.public_ip != worker_node_ip and node.private_ip != worker_node_ip
        ]
        self.save_config()

    def update_cluster(self, name: str, head_node: Node, worker_nodes: List[Node]):
        if name not in self.clusters:
            raise ValueError(f"Cluster '{name}' not found in config")
        self.clusters[name] = Cluster(head_node, worker_nodes)
        self.save_config()

    # Database methods
    def add_db(
        self,
        type: DatabaseType,
        name: str,
        address: str,
        port: int,
        username: str,
        password: str,
    ):
        self.databases[name] = Database(
            address, port, username, password, type
        )
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
        self,
        type: str,
        name: str,
        address: str,
        port: int,
        username: str,
        password: str,
    ):
        if name not in self.databases:
            raise ValueError(f"Database '{name}' not found in config")
        self.databases[name] = Database(
            address, port, username, password, type
        )
        self.save_config()
