import typer
from rich import box
from rich.console import Console
from rich.prompt import Confirm, Prompt
from rich.table import Table

from ..config import Config, Node

app = typer.Typer()
console = Console()
config = Config()


@app.command("create")
def create_cluster():
    """
    Interactively create a new cluster configuration.

    Prompts the user for cluster details such as name, head node, and worker nodes.
    Adds the new cluster configuration to the config.
    """
    name = Prompt.ask("Enter cluster name")

    # Head node
    head_public_ip = Prompt.ask("Enter head node public IP")
    head_private_ip = Prompt.ask("Enter head node private IP (optional)", default="")
    head_num_gpus = int(Prompt.ask("Enter number of GPUs on head node", default="0"))
    head_nproc = int(Prompt.ask("Enter number of processes for head node", default="1"))
    ssh_user = Prompt.ask("Enter SSH user for head node (optional)", default="")
    ssh_pub_key_path = Prompt.ask(
        "Enter absolute path to SSH public key file (optional)", default=""
    )

    head_node = Node(
        head_public_ip,
        head_private_ip or None,
        head_num_gpus,
        head_nproc,
        ssh_user,
        ssh_pub_key_path,
    )

    # Worker nodes
    worker_nodes = []
    while Confirm.ask("Add a worker node?", default=False):
        worker_public_ip = Prompt.ask("Enter worker node public IP")
        worker_private_ip = Prompt.ask(
            "Enter worker node private IP (optional)", default=""
        )
        worker_num_gpus = int(
            Prompt.ask("Enter number of GPUs on worker node", default="0")
        )
        worker_nproc = int(
            Prompt.ask("Enter number of processes for worker node", default="1")
        )
        worker_ssh_user = Prompt.ask(
            "Enter SSH user for head node (optional)", default=""
        )
        worker_ssh_pub_key_path = Prompt.ask(
            "Enter absolute path to SSH public key file (optional)", default=""
        )

        worker_node = Node(
            worker_public_ip,
            worker_private_ip or None,
            worker_num_gpus,
            worker_nproc,
            worker_ssh_user,
            worker_ssh_pub_key_path,
        )
        worker_nodes.append(worker_node)

    config.add_cluster(name, head_node, worker_nodes)
    console.print(f"Cluster [bold green]{name}[/bold green] created successfully.")


@app.command("list")
def list_clusters():
    """
    List all available clusters.

    Retrieves the list of clusters from the config and displays them in a table format.
    """
    clusters = config.list_clusters()

    table = Table(title="Available Clusters", box=box.ROUNDED)
    table.add_column("Cluster Name", style="cyan")
    table.add_column("Head Node", style="magenta")
    table.add_column("Worker Nodes", style="green")
    table.add_column("Total GPUs", style="yellow")
    table.add_column("Total Processes", style="blue")

    for cluster_name in clusters:
        cluster = config.get_cluster(cluster_name)
        total_gpus = cluster.head_node.num_gpus + sum(
            node.num_gpus for node in cluster.worker_nodes
        )
        total_procs = cluster.head_node.nproc + sum(
            node.nproc for node in cluster.worker_nodes
        )
        table.add_row(
            cluster_name,
            cluster.head_node.public_ip,
            str(len(cluster.worker_nodes)),
            str(total_gpus),
            str(total_procs),
        )

    console.print(table)


@app.command("remove")
def remove_cluster(name: str):
    """
    Remove a cluster configuration.

    Prompts the user for confirmation before removing the specified cluster configuration from the config.
    
    Args:
        name (str): The name of the cluster to remove.
    """
    if Confirm.ask(f"Are you sure you want to remove cluster '{name}'?"):
        config.remove_cluster(name)
        console.print(f"Cluster [bold red]{name}[/bold red] removed.")
    else:
        console.print("Cluster removal cancelled.")


@app.command("edit")
def edit_cluster(name: str):
    """
    Edit an existing cluster configuration.

    Prompts the user for new cluster details and updates the specified cluster configuration in the config.
    
    Args:
        name (str): The name of the cluster to edit.
    """
    try:
        cluster = config.get_cluster(name)
    except ValueError:
        console.print(f"[bold red]Error:[/bold red] Cluster '{name}' not found.")
        raise typer.Exit(code=1)

    console.print(f"Editing cluster: [bold green]{name}[/bold green]")

    # Edit head node
    head_node = cluster.head_node
    head_node.public_ip = typer.prompt("Head node public IP", default=head_node.public_ip)
    head_node.private_ip = typer.prompt("Head node private IP (optional)", default=head_node.private_ip  or "")
    head_node.num_gpus = typer.prompt("Number of GPUs on head node", default=head_node.num_gpus, type=int)
    head_node.nproc = typer.prompt("Number of processes on head node", default=head_node.nproc, type=int)
    head_node.ssh_user = typer.prompt("SSH user for head node (optional)", default=head_node.ssh_user or "")
    head_node.ssh_pub_key_path = typer.prompt("SSH public key path for head node (optional)", default=head_node.ssh_pub_key_path or "")

    # Edit worker nodes
    worker_nodes = []
    for i, worker in enumerate(cluster.worker_nodes):
        console.print(f"\nEditing worker node {i+1}")
        public_ip = typer.prompt("Worker node public IP", default=worker.public_ip)
        private_ip = typer.prompt("Worker node private IP (optional)", default=worker.private_ip or "")
        num_gpus = typer.prompt("Number of GPUs on worker node", default=worker.num_gpus, type=int)
        nproc = typer.prompt("Number of processes on worker node", default=worker.nproc, type=int)
        ssh_user = typer.prompt("SSH user for worker node (optional)", default=worker.ssh_user or "")
        ssh_pub_key_path = typer.prompt("SSH public key path for worker node (optional)", default=worker.ssh_pub_key_path or "")
        
        worker_node = Node(public_ip, private_ip or None, num_gpus, nproc, ssh_user, ssh_pub_key_path)
        worker_nodes.append(worker_node)

        if not typer.confirm("Add another worker node?", default=False):
            break

    # Update the cluster configuration
    config.update_cluster(name, head_node, worker_nodes)
    console.print(f"Cluster [bold green]{name}[/bold green] updated successfully.")