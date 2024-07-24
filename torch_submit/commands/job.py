import os
import random
import uuid
from typing import List, Optional

import typer
import yaml
from rich.console import Console
from rich.table import Table

from ..config import Config
from ..connection import NodeConnection
from ..executor import (
    BaseExecutor,
    WorkingDirectoryArchiver,
)
from ..job import JobManager
from ..types import Executor, Job, JobStatus
from ..utils import generate_friendly_name

app = typer.Typer()
console = Console()
config = Config()
job_manager = JobManager()
config = Config()


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
    tail: bool = typer.Option(False, help="Tail the logs after submitting the job"),
    executor: Executor = typer.Option(Executor.TORCHRUN, help="Executor to use"),
    docker_image: Optional[str] = typer.Option(None, help="Docker image to use"),
    database: Optional[str] = typer.Option(None, help="Database to use"),
    runtime_env: Optional[str] = typer.Option(
        None, help="Runtime environment yaml file to use"
    ),
):
    """
    Submit a new job to a specified cluster.

    Args:
        cluster (str): Name of the cluster to use.
        name (Optional[str]): Job name (optional, will be auto-generated if not provided).
        working_dir (str): Path to working directory.
        max_restarts (int): Maximum number of restarts for the job.
        num_gpus (Optional[int]): Number of GPUs to use per node (optional, defaults to all available).
        command (List[str]): The command to run, e.g. 'python main.py'.
        tail (bool): Tail the logs after submitting the job.
        executor (Executor): Executor to use.
        docker_image (Optional[str]): Docker image to use.
        database (Optional[str]): Database to use.
        runtime_env (Optional[str]): Runtime environment yaml file to use.
    """
    if executor == Executor.OPTUNA:
        if not database:
            console.print(
                "[bold red]Error:[/bold red] Database is required for optuna executor"
            )
            raise typer.Exit(code=1)
        try:
            config.get_db(database)
        except ValueError:
            console.print(f"Could not find database {database}")
            raise typer.Exit(code=1)

    try:
        cluster_info = config.get_cluster(cluster)
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
    archiver = WorkingDirectoryArchiver(job_id=job_id, job_name=name)

    if runtime_env:
        console.print(
            f"Loading runtime environment variables from: [bold green]{runtime_env}[/bold green]"
        )
        with open(runtime_env, "r") as f:
            runtime_env_vars = yaml.load(f, Loader=yaml.FullLoader)
        assert all(
            isinstance(value, str) for value in runtime_env_vars.values()
        ), "All values in runtime_env must be strings"
    else:
        runtime_env_vars = None

    console.print("Archiving working directory...")
    archived_dir = archiver.archive(working_dir)
    console.print(
        f"Working directory archived to: [bold green]{archived_dir}[/bold green]"
    )

    nodes = [cluster_info.head_node] + cluster_info.worker_nodes
    job = Job(
        id=job_id,
        name=name,
        status=JobStatus.SUBMITTED,
        working_dir=archived_dir,
        nodes=nodes,
        cluster=cluster,
        command=" ".join(command),
        max_restarts=max_restarts,
        num_gpus=num_gpus,
        executor=executor,
        docker_image=docker_image,
        database=database,
        optuna_port=random.randint(8000, 9000) if executor == Executor.OPTUNA else None,
    )
    console.print("Submitting job...")
    job_manager.add_job(job)

    job_executor = job.get_executor()
    pids = job_executor.execute(runtime_env_vars)

    if all(pid is None for pid in pids.values()):
        job_manager.update_job_status(job_id, JobStatus.CRASHED)
        console.print(f"Job [bold red]{job_id}[/bold red] failed to start.")
        for node in nodes:
            with NodeConnection(node) as c:
                c.run(f"pkill -TERM -P {pids[node]}", hide=True)
        raise typer.Exit(code=1)

    job_manager.update_job_status(job_id, JobStatus.RUNNING)
    job_manager.update_job_pids(job_id, pids)

    console.print(f"Job submitted with name: [bold green]{name}[/bold green]")
    console.print(f"Job ID: [bold blue]{job_id}[/bold blue]")
    console.print(f"Working directory: [bold blue]{working_dir}[/bold blue]")
    console.print(f"Command: [bold yellow]{' '.join(command)}[/bold yellow]")
    console.print(f"Max restarts: [bold cyan]{max_restarts}[/bold cyan]")
    console.print(
        f"GPUs per node: [bold magenta]{num_gpus or 'All available'}[/bold magenta]"
    )

    if tail:
        console.print("Tailing logs...")
        with NodeConnection(nodes[0]) as c:
            c.run(f"tail -f /tmp/torch_submit_job_{job.id}/output.log")


@app.command("logs")
def print_logs(
    job_id: str = typer.Argument(..., help="Job ID or name"),
    tail: bool = typer.Option(False, help="Tail the logs"),
):
    """
    Tail the logs of a specific job.

    Args:
        job_id (str): Job ID or name.
        tail (bool): Tail the logs.
    """
    job_manager = JobManager()
    job = job_manager.get_job(job_id)
    if job:
        console.print(f"Tailing logs for job [bold green]{job_id}[/bold green]")
        console.print("Press [bold red]Ctrl+C[/bold red] to stop")
        with NodeConnection(job.nodes[0]) as c:
            if tail:
                c.run(f"tail -f /tmp/torch_submit_job_{job.id}/output.log")
            else:
                result = c.run(f"cat /tmp/torch_submit_job_{job.id}/output.log")
                console.print(result.stdout)
    else:
        console.print(
            f"Job with ID [bold red]{job_id}[/bold red] not found", style="bold red"
        )


@app.command("list")
def list_jobs():
    """
    List all submitted jobs.
    """
    job_manager = JobManager()
    jobs = job_manager.get_all_jobs_with_status()

    table = Table()
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
            "stopping": "bold yellow",
            "stopped": "bold cyan",
        }.get(job.status, "bold white")

        table.add_row(
            job.id,
            job.name,
            f"[{status_style}]{job.status}[/{status_style}]",
            job.cluster,
            str(len(job.nodes)),
        )
    console.print(table)


@app.command("stop")
def stop_job(job_id: str = typer.Argument(..., help="Job ID or name")):
    """
    Stop a running job.

    Args:
        job_id (str): Job ID or name.
    """
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
            with NodeConnection(node) as c:
                c.run(f"pkill -TERM -P {pid}", warn=True)

        if job.optuna_port:
            with NodeConnection(job.nodes[0]) as c:
                c.run(f"pkill -TERM -f 'optuna-dashboard --port {job.optuna_port}'", warn=True)

        job_manager.update_job_status(job_id, JobStatus.STOPPING)
        console.print(f"Job [bold green]{job_id}[/bold green] is stopping")
    except Exception as e:
        console.print(f"[bold red]Error stopping job:[/bold red] {str(e)}")
        raise typer.Exit(code=1)


@app.command("restart")
def restart_job(job_id: str = typer.Argument(..., help="Job ID or name")):
    """
    Restart a stopped job.

    Args:
        job_id (str): Job ID or name.
    """
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
        cluster = config.get_cluster(job.cluster)
        script_name = job.command.split()[-1]
        script_path = os.path.join(f"/tmp/torch_submit_job_{job.id}", script_name)

        # Check if the job is already running on any node
        for node in [cluster.head_node] + cluster.worker_nodes:
            with NodeConnection(node) as c:
                result = c.run(f"pgrep -f '{script_path}'", warn=True)
                if result.ok:
                    console.print(
                        f"Job [bold yellow]{job_id}[/bold yellow] is already running on node {node_ip}"
                    )
                    raise typer.Exit(code=1)

        # If not running, restart the job
        executor = job.get_executor()
        pids = executor.execute()

        job_manager.update_job_status(job_id, JobStatus.RUNNING)
        job_manager.update_job_pids(job_id, pids)
        console.print(f"Job [bold green]{job_id}[/bold green] has been restarted")
    except Exception as e:
        console.print(f"[bold red]Error restarting job:[/bold red] {str(e)}")
        raise typer.Exit(code=1)


@app.command("delete")
def delete_job(
    job_id: str = typer.Argument(
        ..., help="Job ID or name to delete or 'all' to delete all jobs"
    ),
):
    """
    Delete a job.

    Args:
        job_id (str): Job ID or name to delete or 'all' to delete all jobs.
    """
    job_manager = JobManager()
    jobs = job_manager.get_all_jobs_with_status()

    if not job_id == "all":
        jobs = [job for job in jobs if job.id == job_id]

    # Prepare a list of job IDs to be deleted
    job_ids_to_delete = [job.id for job in jobs]

    # If no jobs found, exit
    if not job_ids_to_delete:
        console.print("No jobs found to delete.")
        raise typer.Exit(code=1)

    # Show confirmation prompt
    if job_id == "all":
        message = f"Are you sure you want to delete all {len(job_ids_to_delete)} jobs?"
    else:
        message = f"Are you sure you want to delete job {job_id}?"

    if not typer.confirm(message):
        console.print("Operation cancelled.")
        raise typer.Exit(code=0)

    # Stop the job if it is still running
    for job in jobs:
        if job.status not in ["finished", "crashed", "stopped"]:
            try:
                stop_job(job.id)
            except typer.Exit:
                console.print(f"Failed to stop job [bold yellow]{job.id}[/bold yellow]")

    # Clean-up the job from remote (executor.cleanup)
    for job in jobs:
        try:
            executor = BaseExecutor(job)
            executor.cleanup()
        except Exception:
            pass

    for job in jobs:
        job_manager.delete_job(job.id)

    if job_id == "all":
        console.print(
            f"[bold green]Successfully deleted all {len(job_ids_to_delete)} jobs.[/bold green]"
        )
    else:
        console.print(f"[bold green]Successfully deleted job {job_id}.[/bold green]")
    console.print("All specified jobs have been stopped and removed from the system.")
