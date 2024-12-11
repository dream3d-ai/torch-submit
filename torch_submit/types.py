from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional

from .config import Database, Node


class Executor(str, Enum):
    """Enumeration of different types of executors."""

    TORCHRUN = "torchrun"
    DISTRIBUTED = "distributed"
    OPTUNA = "optuna"


class JobStatus(str, Enum):
    """Enumeration of different job statuses."""

    SUBMITTED = "submitted"
    RUNNING = "running"
    STOPPING = "stopping"
    STOPPED = "stopped"
    FINISHED = "finished"
    CRASHED = "crashed"
    UNKNOWN = "unknown"


@dataclass
class Job:
    """
    A class representing a job to be executed.

    Attributes:
        id (str): The ID of the job.
        name (str): The name of the job.
        status (JobStatus): The current status of the job.
        working_dir (str): The working directory for the job.
        nodes (List[Node]): The list of nodes assigned to the job.
        cluster (str): The cluster to which the job belongs.
        command (str): The command to be executed for the job.
        max_restarts (int): The maximum number of restarts allowed for the job.
        num_gpus (Optional[int]): The number of GPUs allocated for the job.
        pids (Dict[Node, int]): A dictionary mapping nodes to process IDs.
        executor (Executor): The executor type for the job.
        docker_image (Optional[str]): The Docker image to be used for the job.
        database (Optional[Database]): The database configuration for the job.
        optuna_port (Optional[int]): The port for Optuna executor.
    """

    id: str
    name: str
    status: JobStatus
    working_dir: str
    nodes: List[Node]
    cluster: str
    command: str
    max_restarts: int = 0
    num_gpus: Optional[int] = None
    pids: Dict[Node, int] = field(default_factory=dict)
    executor: Executor = field(default_factory=Executor.TORCHRUN)
    docker_image: Optional[str] = None
    database: Optional[Database] = None
    optuna_port: Optional[int] = None

    def __post_init__(self):
        """Post-initialization checks for the Job class."""
        if self.executor == Executor.OPTUNA and not self.optuna_port:
            raise ValueError("Optuna executor requires a port")

    @classmethod
    def from_json(cls, data: dict) -> "Job":
        """Create Job from JSON dictionary."""
        nodes = [Node.from_json(n) for n in data["nodes"]]
        pids = {}
        for node_ip, pid in data["pids"].items():
            node = next((n for n in nodes if n.public_ip == node_ip), None)
            if node:
                pids[node] = pid
        database = Database.from_json(data["database"]) if data["database"] else None
        return cls(
            id=data["id"],
            name=data["name"],
            status=JobStatus(data["status"]),
            working_dir=data["working_dir"],
            nodes=nodes,
            cluster=data["cluster"],
            command=data["command"],
            max_restarts=data["max_restarts"],
            num_gpus=data["num_gpus"],
            pids=pids,
            executor=Executor(data["executor"]),
            docker_image=data["docker_image"],
            database=database,
            optuna_port=data["optuna_port"],
        )

    def to_json(self) -> dict:
        """Convert Job to JSON-serializable dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status.value,
            "working_dir": self.working_dir,
            "nodes": [node.to_json() for node in self.nodes],
            "cluster": self.cluster,
            "command": self.command,
            "max_restarts": self.max_restarts,
            "num_gpus": self.num_gpus,
            "pids": {node.public_ip: pid for node, pid in self.pids.items()},
            "executor": self.executor.value,
            "docker_image": self.docker_image,
            "database": self.database.to_json() if self.database else None,
            "optuna_port": self.optuna_port,
        }

    def get_executor(self):
        """
        Get the appropriate executor instance for the job.

        Returns:
            An instance of the appropriate executor class.

        Raises:
            ValueError: If an unknown executor type is specified or if Docker image is not supported for the executor.
        """
        from .executor import (
            DistributedExecutor,
            DockerDistributedExecutor,
            OptunaExecutor,
            TorchrunExecutor,
        )

        if self.executor == Executor.TORCHRUN and self.docker_image:
            raise ValueError("Docker image is not supported for torchrun executor")
        elif self.executor == Executor.TORCHRUN:
            return TorchrunExecutor(self)
        elif self.executor == Executor.DISTRIBUTED and self.docker_image:
            return DockerDistributedExecutor(self)
        elif self.executor == Executor.DISTRIBUTED:
            return DistributedExecutor(self)
        elif self.executor == Executor.OPTUNA and self.docker_image:
            raise ValueError("Docker image is not supported for optuna executor")
        elif self.executor == Executor.OPTUNA:
            return OptunaExecutor(self)
        else:
            raise ValueError(f"Unknown executor: {self.executor}")

    def __str__(self):
        """
        Return a string representation of the Job instance.

        Returns:
            str: A string representation of the Job instance.
        """
        return (
            f"Job("
            f"id={self.id}, "
            f"name={self.name}, "
            f"status={self.status.value}, "
            f"working_dir={self.working_dir}, "
            f"nodes={self.nodes}, "
            f"cluster={self.cluster}, "
            f"command={self.command}, "
            f"max_restarts={self.max_restarts}, "
            f"num_gpus={self.num_gpus}, "
            f"pids={self.pids}, "
            f"executor={self.executor}, "
            f"docker_image={self.docker_image}, "
            f"database={self.database}, "
            f"optuna_port={self.optuna_port}"
            f")"
        )
