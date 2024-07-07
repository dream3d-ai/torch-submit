import typer
from fabric import Connection
from rich.console import Console

from ..job import JobManager

app = typer.Typer()
console = Console()


@app.command("tail")
def tail_logs(job_id: str):
    """Tail the logs of a specific job."""
    job_manager = JobManager()
    job = job_manager.get_job(job_id)
    if job:
        console.print(f"Tailing logs for job [bold green]{job_id}[/bold green]")
        console.print("Press [bold red]Ctrl+C[/bold red] to stop")
        with console.status("Connecting to remote node..."):
            with Connection(job.nodes[0]) as c:
                c.run(f"tail -f /tmp/job_{job.id}/logs/output.log")
    else:
        console.print(
            f"Job with ID [bold red]{job_id}[/bold red] not found", style="bold red"
        )
