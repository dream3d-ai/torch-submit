import typer

from .commands import cluster, job, logs

app = typer.Typer()

app.add_typer(cluster.app, name="cluster")
app.add_typer(job.app, name="job")
app.add_typer(logs.app, name="logs")

if __name__ == "__main__":
    app()
