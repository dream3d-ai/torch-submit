import fnmatch
import json
import os
import random
import zipfile
from abc import ABC, abstractmethod
from typing import Dict, Optional

import optuna
from fabric import Connection
from invoke import UnexpectedExit
from rich.console import Console

from .config import Config, Node
from .connection import NodeConnection
from .types import Job

console = Console()


class WorkingDirectoryArchiver:
    """
    A class to handle archiving of working directories for jobs.

    This class creates a zip archive of the specified working directory, including job metadata
    and excluding files specified in a .gitignore file.

    Attributes:
        job_id (str): The ID of the job.
        job_name (str): The name of the job.
        output_dir (str): The directory where the archive will be saved.
    """

    def __init__(self, job_id: str, job_name: str):
        """
        Initialize the WorkingDirectoryArchiver with job ID and job name.

        Args:
            job_id (str): The ID of the job.
            job_name (str): The name of the job.
        """
        self.job_id = job_id
        self.job_name = job_name

        self.output_dir = os.path.expanduser(f"~/.cache/torch-submit/jobs/{job_id}")
        os.makedirs(self.output_dir, exist_ok=True)

    def archive(self, working_dir: str) -> str:
        """
        Create a zip archive of the specified working directory.

        This method reads the .gitignore file in the working directory to determine which files
        to exclude from the archive. It also includes job metadata in the archive.

        Args:
            working_dir (str): The path to the working directory to be archived.

        Returns:
            str: The path to the created zip archive.
        """
        archive_name = f"{os.path.basename(working_dir)}.zip"
        archive_path = os.path.join(self.output_dir, archive_name)

        gitignore_path = os.path.join(working_dir, ".gitignore")
        ignore_patterns = []
        if os.path.exists(gitignore_path):
            with open(gitignore_path, "r") as gitignore_file:
                ignore_patterns = [
                    line.strip()
                    for line in gitignore_file
                    if line.strip() and not line.startswith("#")
                ]

        def should_ignore(path):
            """
            Determine if a file should be ignored based on .gitignore patterns.

            Args:
                path (str): The path to the file.

            Returns:
                bool: True if the file should be ignored, False otherwise.
            """
            rel_path = os.path.relpath(path, working_dir)
            return any(
                rel_path.startswith(pattern) or fnmatch.fnmatch(rel_path, pattern)
                for pattern in ignore_patterns
            )

        with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            # Write job metadata under .torch/job.json
            job_metadata = {
                "id": self.job_id,
                "name": self.job_name,
            }
            zipf.writestr(".torch_submit/job.json", json.dumps(job_metadata))

            # Archive files
            for root, dirs, files in os.walk(working_dir):
                dirs[:] = [
                    d
                    for d in dirs
                    if d != "__pycache__" and not should_ignore(os.path.join(root, d))
                ]
                for file in files:
                    file_path = os.path.join(root, file)
                    if not should_ignore(file_path):
                        arcname = os.path.relpath(file_path, working_dir)
                        zipf.write(file_path, arcname)

        return archive_path


class BaseExecutor(ABC):
    """
    Base class for executing jobs across a cluster.

    This class defines the structure for executing a job. Sub-classes must implement the get_command
    method, which generates the command to be executed on each node in the cluster. The execute method
    runs this command on each node, managing the setup and execution process.

    Methods:
        get_command(rank: int): Abstract method to create the command for the given node rank.
        execute() -> Dict[Node, int]: Executes the job command on each node in the cluster and returns
                                      a dictionary mapping nodes to their process IDs.
    """

    def __init__(self, job: Job):
        self.job = job
        self.remote_dir = f"/tmp/torch_submit_job_{self.job.id}"
        self.cluster = Config().get_cluster(self.job.cluster)

    @abstractmethod
    def get_command(self, rank: int, env_vars: Optional[Dict[str, str]] = None):
        """
        Generate the command to be executed on the given node rank.

        Args:
            rank (int): The rank of the node in the cluster.

        Returns:
            str: The command to be executed on the node.
        """
        ...

    def execute(self, env_vars: Optional[Dict[str, str]] = None) -> Dict[Node, int]:
        """
        Execute the job command on each node in the cluster.

        This method sets up the remote environment, copies the working directory,
        and runs the job command on each node in the cluster. It manages the setup
        and execution process, handling any exceptions that occur during execution.

        Returns:
            Dict[Node, int]: A dictionary mapping nodes to their process IDs.
        """
        pids = {}
        for rank, node in enumerate(
            [self.cluster.head_node] + self.cluster.worker_nodes
        ):
            try:
                with NodeConnection(node) as conn:
                    self._setup_remote_env(conn)
                    self._copy_working_dir(conn)
                    pids[node] = self._run_job(conn, rank, env_vars)
            except Exception:
                console.print_exception()
                console.print(f"Error executing job on node {node.public_ip}")
                pids[node] = None
        return pids

    def _prepare_command(self, rank: int, env_vars: Optional[Dict[str, str]] = None):
        return (
            f"cd {self.remote_dir} && "
            f"{self.get_command(rank, env_vars)} "
            f"{self.job.command}"
        )

    def _run_job(
        self,
        conn: Connection,
        node_rank: int,
        env_vars: Optional[Dict[str, str]] = None,
    ):
        """
        Run the job on the specified node.

        This method changes the directory to the remote directory, runs the provided torchrun command
        along with the job command, and captures the process ID of the running job.

        Args:
            conn (Connection): The connection object to the node.
            executor_command (str): The command with which to run the user-provided script.
            node_rank (int): The rank of the node in the cluster.

        Returns:
            int: The process ID of the running job.
        """
        console.print(
            f"[bold blue]Running job on {conn.host} (rank {node_rank})...[/bold blue]"
        )
        full_command = self._prepare_command(node_rank, env_vars)
        conn.run(
            "source ~/.profile && "
            f"{full_command} > {self.remote_dir}/output.log 2>&1 & "
            f"pid=$!; "
            f"echo $pid > {self.remote_dir}/job.pid; "
            f"wait $pid; "
            f"echo $? > {self.remote_dir}/exit_code",
            disown=True,
        )
        # Parse the PID from the job.pid file
        result = conn.run(f"cat {self.remote_dir}/job.pid", hide=True)
        pid = int(result.stdout.strip())
        return pid

    def _setup_remote_env(self, conn: Connection):
        conn.run(f"mkdir -p {self.remote_dir}")

    def _copy_working_dir(self, conn: Connection):
        remote_zip_path = f"{self.remote_dir}/working_dir.zip"
        console.print(
            f"[bold blue]Copying working directory to {conn.host}...[/bold blue]"
        )
        conn.put(self.job.working_dir, remote_zip_path)

        console.print(
            f"[bold blue]Unzipping working directory on {conn.host}...[/bold blue]"
        )
        conn.run(f"unzip -q -o {remote_zip_path} -d {self.remote_dir}")
        console.print("[bold green]Working directory successfully synced.[/bold green]")

    def cleanup(self):
        """
        Clean up the remote directories on all nodes.

        This method removes the remote directory created for the job on each node.
        If the cleanup fails on any node, a warning message is printed.
        """
        for node in self.job.nodes:
            try:
                with NodeConnection(node) as conn:
                    conn.run(f"rm -rf {self.remote_dir}")
            except UnexpectedExit:
                console.print(
                    f"[bold yellow]Warning: Could not clean up {self.remote_dir} on {node}[/bold yellow]"
                )


class DistributedExecutor(BaseExecutor):
    """
    The DistributedExecutor is responsible for setting up the environment for running
    distributed PyTorch jobs. It ensures that the necessary environment variables are set
    for the torch distributed environment, including MASTER_ADDR, MASTER_PORT, WORLD_SIZE,
    and NODE_RANK. These variables are essential for coordinating the distributed training
    process across multiple nodes and GPUs.

    Exposes the following environment variables to the user script:
        - MASTER_ADDR: The address of the master node.
        - MASTER_PORT: The port on which the master node is listening.
        - WORLD_SIZE: The total number of processes participating in the job.
        - NODE_RANK: The rank of the current node.
        - LOCAL_WORLD_SIZE: The number of processes on the current node.
    """

    def __init__(self, job: Job):
        super().__init__(job)
        self.port = random.randint(29400, 29499)

    def get_command(self, rank: int, env_vars: Optional[Dict[str, str]] = None):
        """
        Constructs the command to run the job with the torch distributed environment variables set.

        This method sets up the necessary environment variables for a distributed torch run, including
        MASTER_ADDR, MASTER_PORT, WORLD_SIZE, and NODE_RANK. It then appends the user-provided command
        to these environment variables.

        Args:
            rank (int): The rank of the current node.

        Returns:
            str: The full command to run the job with the necessary environment variables.
        """
        head_node = self.cluster.head_node
        ip = head_node.private_ip or head_node.public_ip

        world_size = 0
        for node in self.cluster.worker_nodes + [self.cluster.head_node]:
            world_size += node.num_gpus

        formatted_env_vars = " ".join(f"{k}={v}" for k, v in env_vars.items())

        return (
            f"MASTER_ADDR={ip} "
            f"MASTER_PORT={self.port} "
            f"WORLD_SIZE={world_size} "
            f"NODE_RANK={rank} "
            f"LOCAL_WORLD_SIZE={self.cluster.worker_nodes[rank].num_gpus} "
            f"{formatted_env_vars} "
        )


class TorchrunExecutor(BaseExecutor):
    def __init__(self, job: Job):
        super().__init__(job)
        self.port = random.randint(29400, 29499)

    def get_command(self, rank: int, env_vars: Optional[Dict[str, str]] = None):
        """
        Constructs the command to run the job with torchrun.

        This method sets up the necessary parameters for a torchrun command, including
        the number of nodes, the number of processes per node, the rendezvous backend,
        the rendezvous endpoint, the job ID, and the maximum number of restarts.

        Args:
            rank (int): The rank of the current node.

        Returns:
            str: The full command to run the job with torchrun.
        """
        nnodes = len(self.cluster.worker_nodes) + 1  # including head node

        # Determine nproc_per_node
        if rank == 0:  # Head node
            if self.job.num_gpus is not None:
                nproc_per_node = self.job.num_gpus
            elif self.cluster.head_node.num_gpus is not None:
                nproc_per_node = self.cluster.head_node.num_gpus
            else:
                nproc_per_node = 1  # Default to 1 if no GPU information is available
            omp_num_threads = self.cluster.head_node.nproc // nproc_per_node
        else:  # Worker node
            if self.job.num_gpus is not None:
                nproc_per_node = self.job.num_gpus
            elif self.cluster.worker_nodes[rank - 1].num_gpus is not None:
                nproc_per_node = self.cluster.worker_nodes[rank - 1].num_gpus
            else:
                nproc_per_node = 1  # Default to 1 if no GPU information is available
            omp_num_threads = (
                self.cluster.worker_nodes[rank - 1].nproc // nproc_per_node
            )

        if len(self.cluster.worker_nodes) == 0:
            rdzv_endpoint = f"localhost:{self.port}"
        else:
            head_node = self.cluster.head_node
            ip = head_node.private_ip or head_node.public_ip
            rdzv_endpoint = f"{ip}:{self.port}"

        formatted_env_vars = " ".join(f"{k}={v}" for k, v in env_vars.items())

        return (
            f"OMP_NUM_THREADS={omp_num_threads} "
            f"{formatted_env_vars} "
            f"nohup torchrun "
            f"--nnodes={nnodes} "
            f"--node_rank={rank} "
            f"--nproc-per-node={nproc_per_node} "
            f"--rdzv-backend=c10d "
            f"--rdzv-endpoint={rdzv_endpoint} "
            f"--rdzv-id={self.job.id} "
            f"--max-restarts={self.job.max_restarts} "
            "--no-python"
        )


class OptunaExecutor(DistributedExecutor):
    """
    The OptunaExecutor sets up and manages the execution of Optuna distributed optimization jobs.

    The head node runs a SQLite database for Optuna and exposes it to the cluster. Each node in the cluster
    runs a single Optuna process that will utilize all the GPUs available on that node.

    Exposes the following environment variables to the user script:
        - MASTER_ADDR: The address of the master node.
        - MASTER_PORT: The port on which the master node is listening.
        - WORLD_SIZE: The total number of processes participating in the job.
        - NODE_RANK: The rank of the current node.
        - STUDY_NAME: The name of the Optuna study (the job name).
        - DATABASE_URI: The URI of the database.
    """

    def __init__(self, job: Job):
        super().__init__(job)

    def get_command(self, rank: int, env_vars: Optional[Dict[str, str]] = None):
        if rank == 0:
            world_size = self.cluster.head_node.num_gpus
        else:
            world_size = self.cluster.worker_nodes[rank - 1].num_gpus

        formatted_env_vars = " ".join(f"{k}={v}" for k, v in env_vars.items())

        return (
            f"MASTER_ADDR=localhost "
            f"MASTER_PORT={self.port} "
            f"WORLD_SIZE={world_size} "
            f"NODE_RANK={rank} "
            f"OPTUNA_STUDY_NAME={self.job.name} "
            f"OPTUNA_STORAGE={self.job.database.uri} "
            f"{formatted_env_vars} "
        )

    def execute(self) -> Dict[Node, int]:
        """
        Set up the database on the head node and then run the DistributedExecutor execute method.

        This method first sets up the SQLite database on the head node for Optuna. After the database
        is set up, it calls the execute method of the DistributedExecutor to run the job command on
        each node in the cluster.

        Returns:
            Dict[Node, int]: A dictionary mapping nodes to their process IDs.
        """
        optuna.create_study(
            study_name=self.job.name,
            storage=self.job.database.uri,
        )
        with NodeConnection(self.cluster.head_node) as conn:
            conn.run(f"nohup optuna-dashboard --port {self.job.optuna_port} &")
            console.print(
                f"[bold blue]Optuna dashboard running on {self.cluster.head_node.public_ip}:{self.job.optuna_port}[/bold blue]"
            )
        return super().execute()


class DockerDistributedExecutor(DistributedExecutor):
    """
    EXPERIMENTAL:
    DockerDistributedExecutor is an executor that runs distributed jobs inside Docker containers.

    This executor extends the DistributedExecutor to provide Docker support, allowing the user to run
    distributed jobs in isolated Docker environments with GPU support.

    Exposes the following environment variables to the user script:
        - MASTER_ADDR: The address of the master node.
        - MASTER_PORT: The port on which the master node is listening.
        - WORLD_SIZE: The total number of processes participating in the job.
        - NODE_RANK: The rank of the current node.
    """

    def __init__(self, job: Job):
        super().__init__(job)

    def get_command(self, rank: int, env_vars: Optional[Dict[str, str]] = None):
        """
        Constructs the command to run the job with the torch distributed environment variables set.

        This method sets up the necessary environment variables for a distributed torch run, including
        MASTER_ADDR, MASTER_PORT, WORLD_SIZE, and NODE_RANK. It then appends the user-provided command
        to these environment variables.

        Args:
            rank (int): The rank of the current node.

        Returns:
            str: The full command to run the job with the necessary environment variables.
        """
        head_node = self.cluster.head_node
        ip = head_node.private_ip or head_node.public_ip

        world_size = 0
        for node in self.cluster.worker_nodes + [self.cluster.head_node]:
            world_size += node.num_gpus

        formatted_env_vars = " ".join(f"-e {k}={v}" for k, v in env_vars.items())

        return (
            "docker run --rm"
            "--gpus all --runtime=nvidia "
            "--network host "
            f"-v {self.remote_dir}:{self.remote_dir} "
            f"-e MASTER_ADDR={ip} "
            f"-e MASTER_PORT={self.port} "
            f"-e WORLD_SIZE={world_size} "
            f"-e NODE_RANK={rank} "
            f"-e LOCAL_WORLD_SIZE={self.cluster.worker_nodes[rank].num_gpus} "
            f"{formatted_env_vars} "
            f"{self.job.docker_image} "
        )

    def _prepare_command(self, rank: int):
        return f"{self.get_command(rank)} -- {self.job.command}"


class JobExecutionManager:
    @staticmethod
    def submit_job(job: Job):
        executor = job.get_executor()
        try:
            executor.execute()
            console.print(
                f"[bold green]Job {job.id} submitted successfully[/bold green]"
            )
        except Exception as e:
            console.print(
                f"[bold red]Error submitting job {job.id}:[/bold red] {str(e)}"
            )
            executor.cleanup()

    @staticmethod
    def cancel_job(job: Job):
        executor = job.get_executor()
        try:
            executor.cleanup()
            console.print(
                f"[bold green]Job {job.id} cancelled successfully[/bold green]"
            )
        except Exception as e:
            console.print(
                f"[bold red]Error cancelling job {job.id}:[/bold red] {str(e)}"
            )
