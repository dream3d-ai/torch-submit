import typer

from .commands import cluster, job

app = typer.Typer()

app.add_typer(cluster.app, name="cluster")
app.add_typer(job.app, name="job")

if __name__ == "__main__":
    app()
