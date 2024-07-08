import os
import uuid
from typing import List, Optional

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
    cluster: str = typer.Option(..., help="Name of the cluster to use"),
    name: Optional[str] = typer.Option(
        None, help="Job name (optional, will be auto-generated if not provided)"
    ),
    working_dir: str = typer.Option("./", help="Path to working directory"),
    max_restarts: int = typer.Option(0, help="Maximum number of restarts for the job"),
    num_gpus: Optional[int] = typer.Option(
        None,
        help="Number of GPUs to use per node (optional, defaults to all available)",
    ),
    command: List[str] = typer.Argument(
        ..., help="The command to run, e.g. 'python main.py'"
    ),
):
    """Submit a new job to a specified cluster."""
    try:
        cluster_info = cluster_config.get_cluster(cluster)
    except ValueError as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        raise typer.Exit(code=1)

    if num_gpus is not None and num_gpus > cluster_info.head_node.num_gpus:
        console.print(
            f"[bold red]Error:[/bold red] Requested GPUs ({num_gpus}) exceeds available GPUs on head node ({cluster_info.head_node.num_gpus})"
        )
        raise typer.Exit(code=1)

    if name is None:
        name = generate_friendly_name()

    working_dir = os.path.abspath(working_dir)

    job_id = str(uuid.uuid4())
    console.print("Archiving working directory...")
    archiver = WorkingDirectoryArchiver()
    output_dir = os.path.expanduser(f"~/.cache/torch-submit/jobs/{job_id}")
    os.makedirs(output_dir, exist_ok=True)
    archived_dir = archiver.archive(working_dir, output_dir=output_dir)
    console.print(
        f"Working directory archived to: [bold green]{archived_dir}[/bold green]"
    )

    nodes = [cluster_info.head_node] + cluster_info.worker_nodes
    job = Job(
        id=job_id,
        name=name,
        status="submitted",
        working_dir=archived_dir,
        nodes=[node.private_ip or node.public_ip for node in nodes],
        cluster=cluster,
        command=" ".join(command),
        max_restarts=max_restarts,
        num_gpus=num_gpus,
    )
    console.print("Submitting job...")
    job_manager.add_job(job)

    executor = RemoteExecutor(job)
    pids = executor.execute()
    job_manager.update_job_pids(job_id, pids)

    console.print(f"Job submitted with name: [bold green]{name}[/bold green]")
    console.print(f"Job ID: [bold blue]{job_id}[/bold blue]")
    console.print(f"Working directory: [bold blue]{working_dir}[/bold blue]")
    console.print(f"Command: [bold yellow]{' '.join(command)}[/bold yellow]")
    console.print(f"Max restarts: [bold cyan]{max_restarts}[/bold cyan]")
    console.print(
        f"GPUs per node: [bold magenta]{num_gpus or 'All available'}[/bold magenta]"
    )


@app.command("logs")
def tail_logs(job_id: str):
    """Tail the logs of a specific job."""
    job_manager = JobManager()
    job = job_manager.get_job(job_id)
    if job:
        console.print(f"Tailing logs for job [bold green]{job_id}[/bold green]")
        console.print("Press [bold red]Ctrl+C[/bold red] to stop")
        with Connection(job.nodes[0]) as c:
            c.run(f"tail -f /tmp/torch_submit_job_{job.id}/output.log")
    else:
        console.print(
            f"Job with ID [bold red]{job_id}[/bold red] not found", style="bold red"
        )


@app.command("list")
def list_jobs():
    """List all submitted jobs."""
    job_manager = JobManager()
    jobs = job_manager.get_all_jobs_with_status(cluster_config)

    table = Table(title="Job List", box=box.ROUNDED)
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Name", style="magenta")
    table.add_column("Status", style="green")
    table.add_column("Cluster", style="yellow")
    table.add_column("Nodes", style="blue")

    for job in jobs:
        status_style = {
            "started": "bold yellow",
            "running": "bold green",
            "crashed": "bold red",
            "stopping": "bold orange",
            "stopped": "bold cyan",
        }.get(job.status, "")

        table.add_row(
            job.id,
            job.name,
            f"[{status_style}]{job.status}[/{status_style}]",
            job.cluster,
            str(len(job.nodes)),
        )
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
        for node, pid in job.pids.items():
            with Connection(node) as c:
                c.run(f"pkill -TERM -P {pid}", warn=True)

        job_manager.update_job_status(job_id, "stopping")
        console.print(f"Job [bold green]{job_id}[/bold green] is stopping")
    except Exception as e:
        console.print(f"[bold red]Error stopping job:[/bold red] {str(e)}")
        raise typer.Exit(code=1)


@app.command("restart")
def restart_job(job_id: str):
    """Restart a stopped job."""
    job = job_manager.get_job(job_id)
    if not job:
        console.print(
            f"Job with ID [bold red]{job_id}[/bold red] not found", style="bold red"
        )
        raise typer.Exit(code=1)

    if job.status != "stopped":
        console.print(
            f"Job [bold yellow]{job_id}[/bold yellow] is not stopped. Current status: {job.status}"
        )
        raise typer.Exit(code=1)

    console.print(f"Restarting job [bold yellow]{job_id}[/bold yellow]")

    try:
        cluster = cluster_config.get_cluster(job.cluster)
        script_name = job.command.split()[-1]
        script_path = os.path.join(f"/tmp/torch_submit_job_{job.id}", script_name)

        # Check if the job is already running on any node
        for node in [cluster.head_node] + cluster.worker_nodes:
            node_ip = node.private_ip or node.public_ip
            with Connection(node_ip) as c:
                result = c.run(f"pgrep -f '{script_path}'", warn=True)
                if result.ok:
                    console.print(
                        f"Job [bold yellow]{job_id}[/bold yellow] is already running on node {node_ip}"
                    )
                    raise typer.Exit(code=1)

        # If not running, restart the job
        executor = RemoteExecutor(job)
        pids = executor.execute()

        job_manager.update_job_status(job_id, "running")
        job_manager.update_job_pids(job_id, pids)
        console.print(f"Job [bold green]{job_id}[/bold green] has been restarted")
    except Exception as e:
        console.print(f"[bold red]Error restarting job:[/bold red] {str(e)}")
        raise typer.Exit(code=1)
