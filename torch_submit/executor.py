import os
import random
import zipfile

from fabric import Connection
from invoke import UnexpectedExit
from rich.console import Console

from .cluster_config import ClusterConfig
from .job import Job

console = Console()


class WorkingDirectoryArchiver:
    @staticmethod
    def archive(working_dir: str, output_dir: str) -> str:
        archive_name = f"{os.path.basename(working_dir)}.zip"
        archive_path = os.path.join(output_dir, archive_name)

        with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(working_dir):
                # Skip __pycache__ directories
                dirs[:] = [d for d in dirs if d != "__pycache__"]
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, working_dir)
                    zipf.write(file_path, arcname)

        return archive_path


class RemoteExecutor:
    def __init__(self, job: Job):
        self.job = job
        self.remote_dir = f"/tmp/torch_submit_job_{self.job.id}"
        self.cluster_config = ClusterConfig()

    def execute(self):
        cluster = self.cluster_config.get_cluster(self.job.cluster)
        nnodes = len(cluster.worker_nodes) + 1  # including head node
        
        # Determine nproc_per_node
        if self.job.num_gpus is not None:
            nproc_per_node = self.job.num_gpus
        elif cluster.head_node.num_gpus is not None:
            nproc_per_node = cluster.head_node.num_gpus
        else:
            nproc_per_node = 1  # Default to 1 if no GPU information is available
        
        if len(cluster.worker_nodes) == 0:
            rdzv_endpoint = "localhost:0"
        else:
            head_node = cluster.head_node
            ip = head_node.private_ip or head_node.public_ip
            port = random.randint(29400, 29499)
            rdzv_endpoint = f"{ip}:{port}"

        torchrun_command = (
            f"torchrun "
            f"--nnodes={nnodes} "
            f"--nproc-per-node={nproc_per_node} "
            f"--rdzv-backend=c10d "
            f"--rdzv-endpoint={rdzv_endpoint} "
            f"--rdzv-id={self.job.id} "
            f"--max-restarts={self.job.max_restarts} "
            "--no-python"
        )

        pids = {}
        for i, node in enumerate([cluster.head_node] + cluster.worker_nodes):
            node_ip = node.private_ip or node.public_ip
            try:
                with Connection(node_ip) as conn:
                    self._setup_remote_env(conn)
                    if i == 0:  # Head node
                        self._copy_working_dir(conn)
                    pid = self._run_job(conn, torchrun_command, i)
                    pids[node_ip] = pid
            except Exception as e:
                print(f"Error executing job on node {node_ip}: {str(e)}")
                pids[node_ip] = None
        return pids

    def _run_job(self, conn: Connection, torchrun_command: str, node_rank: int):
        console.print(
            f"[bold blue]Running job on {conn.host} (rank {node_rank})...[/bold blue]"
        )
        full_command = (
            f"cd {self.remote_dir} && "
            f"nohup {torchrun_command} --node-rank={node_rank} "
            f"{self.job.command}"
        )
        conn.run(f"{full_command} > {self.remote_dir}/output.log 2>&1 & echo $! > {self.remote_dir}/job.pid", disown=True)
        # Parse the PID from the job.pid file
        result = conn.run(f"cat {self.remote_dir}/job.pid", hide=True)
        pid = int(result.stdout.strip())
        return pid

    def _setup_remote_env(self, conn: Connection):
        conn.run(f"mkdir -p {self.remote_dir}")

    def _copy_working_dir(self, conn: Connection):
        remote_zip_path = f"{self.remote_dir}/working_dir.zip"
        console.print(f"[bold blue]Copying working directory to {conn.host}...[/bold blue]")
        conn.put(self.job.working_dir, remote_zip_path)
        
        console.print(f"[bold blue]Unzipping working directory on {conn.host}...[/bold blue]")
        conn.run(f"unzip -q -o {remote_zip_path} -d {self.remote_dir}")
        console.print("[bold green]Working directory successfully synced.[/bold green]")

    def cleanup(self):
        for node in self.job.nodes:
            try:
                with Connection(node) as conn:
                    conn.run(f"rm -rf {self.remote_dir}")
            except UnexpectedExit:
                console.print(
                    f"[bold yellow]Warning: Could not clean up {self.remote_dir} on {node}[/bold yellow]"
                )


class JobExecutionManager:
    @staticmethod
    def submit_job(job: Job):
        executor = RemoteExecutor(job)
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
        executor = RemoteExecutor(job)
        try:
            executor.cleanup()
            console.print(
                f"[bold green]Job {job.id} cancelled successfully[/bold green]"
            )
        except Exception as e:
            console.print(
                f"[bold red]Error cancelling job {job.id}:[/bold red] {str(e)}"
            )
