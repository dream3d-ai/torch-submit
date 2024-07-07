import typer
from rich import box
from rich.console import Console
from rich.prompt import Confirm, Prompt
from rich.table import Table

from ..cluster_config import ClusterConfig, Node

app = typer.Typer()
console = Console()
cluster_config = ClusterConfig()


@app.command("create")
def create_cluster():
    """Interactively create a new cluster configuration."""
    name = Prompt.ask("Enter cluster name")

    # Head node
    head_public_ip = Prompt.ask("Enter head node public IP")
    head_private_ip = Prompt.ask("Enter head node private IP (optional)", default="")
    head_num_gpus = int(Prompt.ask("Enter number of GPUs on head node", default="0"))
    head_nproc = int(Prompt.ask("Enter number of processes for head node", default="1"))

    head_node = Node(head_public_ip, head_private_ip or None, head_num_gpus, head_nproc)

    # Worker nodes
    worker_nodes = []
    while Confirm.ask("Add a worker node?"):
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

        worker_node = Node(
            worker_public_ip, worker_private_ip or None, worker_num_gpus, worker_nproc
        )
        worker_nodes.append(worker_node)

    cluster_config.add_cluster(name, head_node, worker_nodes)
    console.print(f"Cluster [bold green]{name}[/bold green] created successfully.")


@app.command("list")
def list_clusters():
    """List all available clusters."""
    clusters = cluster_config.list_clusters()

    table = Table(title="Available Clusters", box=box.ROUNDED)
    table.add_column("Cluster Name", style="cyan")
    table.add_column("Head Node", style="magenta")
    table.add_column("Worker Nodes", style="green")
    table.add_column("Total GPUs", style="yellow")
    table.add_column("Total Processes", style="blue")

    for cluster_name in clusters:
        cluster = cluster_config.get_cluster(cluster_name)
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
    """Remove a cluster configuration."""
    if Confirm.ask(f"Are you sure you want to remove cluster '{name}'?"):
        cluster_config.remove_cluster(name)
        console.print(f"Cluster [bold red]{name}[/bold red] removed.")
    else:
        console.print("Cluster removal cancelled.")
