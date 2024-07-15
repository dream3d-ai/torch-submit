from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple

from torch_submit.executor import DockerDistributedExecutor

from .cluster_config import Node


class Executor(str, Enum):
    TORCHRUN = "torchrun"
    DISTRIBUTED = "distributed"
    OPTUNA = "optuna"


class JobStatus(str, Enum):
    SUBMITTED = "submitted"
    RUNNING = "running"
    STOPPING = "stopping"
    STOPPED = "stopped"
    FINISHED = "finished"
    CRASHED = "crashed"
    UNKNOWN = "unknown"


@dataclass
class Job:
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
    docker_image: Optional[str] = None  # docker image

    @classmethod
    def from_db(cls, row: Tuple) -> "Job":
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
            image=row[11] or None,
        )

    def to_db(self) -> Tuple:
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
        )

    def get_executor(self):
        from .executor import (
            DistributedExecutor,
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
            f"docker_image={self.docker_image}"
            f")"
        )
