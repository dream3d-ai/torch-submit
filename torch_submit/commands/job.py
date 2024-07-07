import os
import uuid
from typing import Optional

import typer
from fabric import Connection
from rich.console import Console
from rich.table import Table, box

from ..cluster_config import ClusterConfig
from ..executor import RemoteExecutor, WorkingDirectoryArchiver
from ..job import Job, JobManager
from ..utils import generate_friendly_name

app = typer.Typer()
console = Console()
cluster_config = ClusterConfig()
job_manager = JobManager()


@app.command("submit")
def submit(
    name: Optional[str] = typer.Option(
        None, help="Job name (optional, will be auto-generated if not provided)"
    ),
    working_dir: str = typer.Option("./", help="Path to working directory"),
    cluster: str = typer.Option(..., help="Name of the cluster to use"),
):
    """Submit a new job to a specified cluster."""
    archiver = WorkingDirectoryArchiver()

    try:
        cluster_info = cluster_config.get_cluster(cluster)
    except ValueError as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        raise typer.Exit(code=1)

    if name is None:
        name = generate_friendly_name()

    working_dir = os.path.abspath(working_dir)

    job_id = str(uuid.uuid4())
    archived_dir = archiver.archive(working_dir, "archived_jobs")

    nodes = [cluster_info.head_node] + cluster_info.worker_nodes
    job = Job(
        id=job_id,
        name=name,
        status="submitted",
        working_dir=archived_dir,
        nodes=[node.private_ip or node.public_ip for node in nodes],
        cluster=cluster,
    )
    job_manager.add_job(job)

    executor = RemoteExecutor(job)
    executor.execute()

    console.print(f"Job submitted with name: [bold green]{name}[/bold green]")
    console.print(f"Job ID: [bold blue]{job_id}[/bold blue]")
    console.print(f"Working directory: [bold blue]{working_dir}[/bold blue]")


@app.command("list")
def list_jobs():
    """List all submitted jobs."""
    jobs = job_manager.list_jobs()

    table = Table(title="Job List", box=box.ROUNDED)
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Name", style="magenta")
    table.add_column("Status", style="green")
    table.add_column("Cluster", style="yellow")
    table.add_column("Nodes", style="blue")

    for job in jobs:
        table.add_row(job.id, job.name, job.status, job.cluster, str(len(job.nodes)))

    console.print(table)


@app.command("stop")
def stop_job(job_id: str):
    """Stop a running job."""
    job_manager = JobManager()
    job = job_manager.get_job(job_id)
    if not job:
        console.print(
            f"Job with ID [bold red]{job_id}[/bold red] not found", style="bold red"
        )
        raise typer.Exit(code=1)

    console.print(f"Stopping job [bold yellow]{job_id}[/bold yellow]")

    try:
        cluster = cluster_config.get_cluster(job.cluster)
        head_node = cluster.head_node.private_ip or cluster.head_node.public_ip

        with Connection(head_node) as c:
            c.run(f"pkill -9 -f 'job_{job_id}'", warn=True)

        job_manager.update_job_status(job_id, "stopped")
        console.print(f"Job [bold green]{job_id}[/bold green] has been stopped")
    except Exception as e:
        console.print(f"[bold red]Error stopping job:[/bold red] {str(e)}")
        raise typer.Exit(code=1)
