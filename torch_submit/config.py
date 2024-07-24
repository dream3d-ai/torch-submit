import os
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional

import yaml
from sqlalchemy import create_engine, text


@dataclass
class Node:
    """Represents a node in a cluster.

    Attributes:
        public_ip (str): The public IP address of the node.
        private_ip (Optional[str]): The private IP address of the node, if available.
        num_gpus (int): The number of GPUs available on the node.
        nproc (int): The number of processes that can run on the node.
        ssh_user (Optional[str]): The SSH username for accessing the node, if available.
        ssh_pub_key_path (Optional[str]): The path to the SSH public key file, if available.
    """

    public_ip: str
    private_ip: Optional[str]
    num_gpus: int
    nproc: int
    ssh_user: Optional[str]
    ssh_pub_key_path: Optional[str]

    def __post_init__(self):
        """Initialize the Node object after creation."""
        self.private_ip = self.private_ip or None
        self.ssh_user = self.ssh_user or None
        self.ssh_pub_key_path = self.ssh_pub_key_path or None
        self.num_gpus = int(self.num_gpus)
        self.nproc = int(self.nproc)

    @classmethod
    def from_db(cls, row: str):
        """Create a Node object from a database row string.

        Args:
            row (str): A string representation of the node data.

        Returns:
            Node: A new Node object created from the row data.
        """
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
        """Convert the Node object to a string representation for database storage.

        Returns:
            str: A string representation of the Node object.
        """
        return f"{self.public_ip}:{self.private_ip or 'None'}:{self.num_gpus}:{self.nproc}:{self.ssh_user or 'None'}:{self.ssh_pub_key_path or 'None'}"

    def __str__(self):
        """Return a string representation of the Node object.

        Returns:
            str: A string representation of the Node object.
        """
        return f"Node(public_ip={self.public_ip}, private_ip={self.private_ip}, num_gpus={self.num_gpus}, nproc={self.nproc}, ssh_user={self.ssh_user}, ssh_pub_key_path={self.ssh_pub_key_path})"

    def __hash__(self):
        """Return a hash value for the Node object.

        Returns:
            int: A hash value based on the public IP address.
        """
        return hash(self.public_ip)

    def __eq__(self, other):
        """Check if two Node objects are equal.

        Args:
            other: Another object to compare with.

        Returns:
            bool: True if the objects are equal, False otherwise.
        """
        if not isinstance(other, Node):
            return NotImplemented
        return self.public_ip == other.public_ip


@dataclass
class Cluster:
    """Represents a cluster of nodes.

    Attributes:
        head_node (Node): The head node of the cluster.
        worker_nodes (List[Node]): A list of worker nodes in the cluster.
    """

    head_node: Node
    worker_nodes: List[Node]


class DatabaseType(str, Enum):
    """Enumeration of supported database types.

    Attributes:
        POSTGRES: PostgreSQL database type.
        MYSQL: MySQL database type.
    """

    POSTGRES = "postgres"
    MYSQL = "mysql"
    
    @property
    def connection_string(self):
        """Get the SQLAlchemy connection string prefix for the database type.

        Returns:
            str: The connection string prefix.

        Raises:
            ValueError: If the database type is unknown.
        """
        if self == DatabaseType.POSTGRES:
            return "postgresql+psycopg2"
        elif self == DatabaseType.MYSQL:
            return "mysql"
        else:
            raise ValueError(f"Unknown database type: {self}")


@dataclass
class Database:
    """Represents a database configuration.

    Attributes:
        address (str): The address of the database server.
        port (int): The port number for the database connection.
        username (str): The username for database authentication.
        password (str | None): The password for database authentication, if required.
        type (DatabaseType): The type of the database (e.g., PostgreSQL, MySQL).
    """

    address: str
    port: int
    username: str
    password: str | None = None
    type: DatabaseType = DatabaseType.POSTGRES

    def __post_init__(self):
        """Initialize the Database object after creation."""
        self.port = int(self.port)
        self.type = DatabaseType(self.type)

    @classmethod
    def from_db(cls, row: str):
        """Create a Database object from a database row string.

        Args:
            row (str): A string representation of the database data.

        Returns:
            Database: A new Database object created from the row data.
        """
        address, port, username, password, type = row.split(":")
        return cls(
            address,
            int(port),
            username,
            password or None,
            DatabaseType(type),
        )

    @property
    def uri(self):
        """Get the database URI for SQLAlchemy connection.

        Returns:
            str: The database URI.
        """
        return f"{self.type.connection_string}://{self.username}:{self.password}@{self.address}:{self.port}/torch_submit"

    def to_db(self):
        """Convert the Database object to a string representation for database storage.

        Returns:
            str: A string representation of the Database object.
        """
        return f"{self.address}:{self.port}:{self.username}:{self.password or ''}:{self.type.value}"

    def __str__(self):
        """Return a string representation of the Database object.

        Returns:
            str: A string representation of the Database object.
        """
        return f"Database(type={self.type}, address={self.address}, port={self.port}, username={self.username}, password=****)"

    def __hash__(self):
        """Return a hash value for the Database object.

        Returns:
            int: A hash value based on the database attributes.
        """
        return (
            hash(self.type)
            + hash(self.address)
            + hash(self.port)
            + hash(self.username)
            + hash(self.password)
        )

    def __eq__(self, other):
        """Check if two Database objects are equal.

        Args:
            other: Another object to compare with.

        Returns:
            bool: True if the objects are equal, False otherwise.
        """
        if not isinstance(other, Database):
            return NotImplemented
        return (
            self.address == other.address
            and self.port == other.port
            and self.type == other.type
        )


class Config:
    """Manages the configuration for clusters and databases.

    This class handles loading, saving, and manipulating the configuration
    for clusters and databases used in the torch-submit system.
    """

    def __init__(self):
        """Initialize the Config object."""
        self.config_path = os.path.expanduser("~/.cache/torch-submit/config.yaml")
        self.clusters: Dict[str, Cluster] = {}
        self.databases: Dict[str, Database] = {}
        self.load_config()

    def load_config(self):
        """Load the configuration from the YAML file."""
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
        """Save the current configuration to the YAML file."""
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
        """Add a new cluster to the configuration.

        Args:
            name (str): The name of the cluster.
            head_node (Node): The head node of the cluster.
            worker_nodes (List[Node]): The list of worker nodes in the cluster.
        """
        self.clusters[name] = Cluster(head_node, worker_nodes)
        self.save_config()

    def remove_cluster(self, name: str):
        """Remove a cluster from the configuration.

        Args:
            name (str): The name of the cluster to remove.
        """
        if name in self.clusters:
            del self.clusters[name]
            self.save_config()

    def get_cluster(self, cluster_name: str) -> Cluster:
        """Get a cluster by its name.

        Args:
            cluster_name (str): The name of the cluster.

        Returns:
            Cluster: The requested cluster.

        Raises:
            ValueError: If the cluster is not found in the configuration.
        """
        if cluster_name not in self.clusters:
            raise ValueError(f"Cluster '{cluster_name}' not found in config")
        return self.clusters[cluster_name]

    def list_clusters(self) -> List[str]:
        """Get a list of all cluster names.

        Returns:
            List[str]: A list of cluster names.
        """
        return list(self.clusters.keys())

    def add_worker_node(self, cluster_name: str, worker_node: Node):
        """Add a worker node to a cluster.

        Args:
            cluster_name (str): The name of the cluster.
            worker_node (Node): The worker node to add.

        Raises:
            ValueError: If the cluster is not found in the configuration.
        """
        if cluster_name not in self.clusters:
            raise ValueError(f"Cluster '{cluster_name}' not found in config")
        self.clusters[cluster_name].worker_nodes.append(worker_node)
        self.save_config()

    def remove_worker_node(self, cluster_name: str, worker_node_ip: str):
        """Remove a worker node from a cluster.

        Args:
            cluster_name (str): The name of the cluster.
            worker_node_ip (str): The IP address of the worker node to remove.

        Raises:
            ValueError: If the cluster is not found in the configuration.
        """
        if cluster_name not in self.clusters:
            raise ValueError(f"Cluster '{cluster_name}' not found in config")
        self.clusters[cluster_name].worker_nodes = [
            node
            for node in self.clusters[cluster_name].worker_nodes
            if node.public_ip != worker_node_ip and node.private_ip != worker_node_ip
        ]
        self.save_config()

    def update_cluster(self, name: str, head_node: Node, worker_nodes: List[Node]):
        """Update an existing cluster in the configuration.

        Args:
            name (str): The name of the cluster to update.
            head_node (Node): The new head node for the cluster.
            worker_nodes (List[Node]): The new list of worker nodes for the cluster.

        Raises:
            ValueError: If the cluster is not found in the configuration.
        """
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
        """Add a new database to the configuration.

        Args:
            type (DatabaseType): The type of the database.
            name (str): The name of the database configuration.
            address (str): The address of the database server.
            port (int): The port number for the database connection.
            username (str): The username for database authentication.
            password (str): The password for database authentication.
        """
        self.databases[name] = Database(address, port, username, password, type)
        self.save_config()
        engine = create_engine(self.databases[name].uri.strip("/torch_submit"))
        with engine.connect() as conn:
            conn.execute(text("CREATE DATABASE IF NOT EXISTS torch_submit"))

    def remove_db(self, name: str):
        """Remove a database from the configuration.

        Args:
            name (str): The name of the database configuration to remove.
        """
        if name in self.databases:
            del self.databases[name]
            self.save_config()

    def get_db(self, db_name: str) -> Database:
        """Get a database configuration by its name.

        Args:
            db_name (str): The name of the database configuration.

        Returns:
            Database: The requested database configuration.

        Raises:
            ValueError: If the database configuration is not found.
        """
        if db_name not in self.databases:
            raise ValueError(f"Database '{db_name}' not found in config")
        return self.databases[db_name]

    def list_dbs(self) -> List[str]:
        """Get a list of all database configuration names.

        Returns:
            List[str]: A list of database configuration names.
        """
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
        """Update an existing database configuration.

        Args:
            type (str): The type of the database.
            name (str): The name of the database configuration to update.
            address (str): The new address of the database server.
            port (int): The new port number for the database connection.
            username (str): The new username for database authentication.
            password (str): The new password for database authentication.

        Raises:
            ValueError: If the specified database configuration is not found.
        """
        if name not in self.databases:
            raise ValueError(f"Database '{name}' not found in config")
        self.databases[name] = Database(address, port, username, password, type)
        self.save_config()
