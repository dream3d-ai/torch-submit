from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple

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
    def from_db(cls, row: Tuple) -> "Job":
        """
        Create a Job instance from a database row.

        Args:
            row (Tuple): A tuple representing a row from the database.

        Returns:
            Job: A Job instance created from the database row.
        """
        nodes = [Node.from_db(node) for node in row[4].split(",")]
        pids = {}
        if row[9]:
            for pair in row[9].split(","):
                node_ip, pid = pair.split(":")
                node = next((n for n in nodes if n.public_ip == node_ip), None)
                if node:
                    pids[node] = int(pid)

        return cls(
            id=row[0],
            name=row[1],
            status=JobStatus(row[2]),
            working_dir=row[3],
            nodes=nodes,
            cluster=row[5],
            command=row[6],
            max_restarts=int(row[7]),
            num_gpus=int(row[8]) if row[8] else None,
            pids=pids,
            executor=Executor(row[10]),
            docker_image=row[11] or None,
            database=Database.from_db(row[12]) if row[12] else None,
            optuna_port=int(row[13]) if row[13] else None,
        )

    def to_db(self) -> Tuple:
        """
        Convert the Job instance to a tuple for database storage.

        Returns:
            Tuple: A tuple representing the Job instance for database storage.
        """
        return (
            self.id,
            self.name,
            self.status.value,
            self.working_dir,
            ",".join([node.to_db() for node in self.nodes]),
            self.cluster,
            self.command,
            self.max_restarts,
            self.num_gpus or "",
            ",".join([f"{k}:{v}" for k, v in self.pids.items()]),
            self.executor.value,
            self.docker_image or "",
            self.database.to_db() or "" if self.database else "",
            self.optuna_port or "",
        )

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
