from importlib.metadata import version

import typer

from .commands import cluster, database, job

app = typer.Typer()

app.add_typer(cluster.app, name="cluster")
app.add_typer(job.app, name="job")
app.add_typer(database.app, name="db")


def version_callback(value: bool):
    if value:
        print(f"torch-submit version: {version('torch-submit')}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        None,
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Show the version and exit.",
    ),
):
    pass


if __name__ == "__main__":
    app()
