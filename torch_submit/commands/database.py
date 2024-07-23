import typer
from rich import box
from rich.console import Console
from rich.prompt import Confirm, Prompt
from rich.table import Table

from ..db_config import DatabaseConfig, DatabaseType

app = typer.Typer()
console = Console()
db_config = DatabaseConfig()

@app.command("create")
def create_database():
    """Interactively create a new database configuration."""
    name = Prompt.ask("Enter database name")

    # Database address and port
    type = Prompt.ask("Enter database type (mysql, postgres)", default=DatabaseType.POSTGRES.value)
    address = Prompt.ask("Enter database address")
    port = int(Prompt.ask("Enter database port", default="5432"))
    username = Prompt.ask("Enter database username")
    password = Prompt.ask("Enter database password (optional)", password=True, default="")

    db_config.add_db(type, name, address, port, username, password)
    console.print(f"Database [bold green]{name}[/bold green] created successfully.")


@app.command("list")
def list_databases():
    """List all available databases."""
    databases = db_config.list_dbs()

    table = Table(title="Available Databases", box=box.ROUNDED)
    table.add_column("Database Name", style="cyan")
    table.add_column("Type", style="magenta")
    table.add_column("Address", style="green")
    table.add_column("Port", style="yellow")
    table.add_column("Username", style="yellow")
    table.add_column("Password", style="red")

    for db_name in databases:
        database = db_config.get_db(db_name)
        table.add_row(
            db_name,
            database.type.value,
            database.address,
            str(database.port),
            database.username,
            "****" if database.password else "Not set",
        )

    console.print(table)


@app.command("remove")
def remove_database(name: str):
    """Remove a database configuration."""
    if Confirm.ask(f"Are you sure you want to remove database '{name}'?"):
        db_config.remove_db(name)
        console.print(f"Database [bold red]{name}[/bold red] removed.")
    else:
        console.print("Database removal cancelled.")


@app.command("edit")
def edit_database(name: str):
    """Edit an existing database configuration."""
    try:
        database = db_config.get_db(name)
    except ValueError:
        console.print(f"[bold red]Error:[/bold red] Database '{name}' not found.")
        raise typer.Exit(code=1)

    console.print(f"Editing database: [bold green]{name}[/bold green]")

    # Edit database address and port
    type = Prompt.ask("Enter database type (mysql, postgres)", default=database.type.value)
    address = Prompt.ask("Enter database address", default=database.address)
    port = Prompt.ask("Enter database port", default=database.port, type=int)
    username = Prompt.ask("Enter database username", default=database.username)
    password = Prompt.ask("Enter database password (optional)", password=True, default=database.password)

    # Update the database configuration
    db_config.update_db(type, name, address, port, username, password)
    console.print(f"Database [bold green]{name}[/bold green] updated successfully.")