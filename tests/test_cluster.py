import pytest
from pathlib import Path
from typer.testing import CliRunner
from rich.console import Console

from torch_submit.commands.cluster import app, config
from torch_submit.config import Node

runner = CliRunner()
console = Console()

@pytest.fixture
def mock_cluster(tmp_path):
    """Create a mock cluster configuration for testing."""
    head_node = Node(
        public_ip="1.2.3.4",
        private_ip="10.0.0.1",
        num_gpus=2,
        nproc=4,
        ssh_user="test",
        ssh_pub_key_path=str(tmp_path / "test_key.pub"),
        ssh_port=22,
        ansible_playbook=None
    )
    worker_nodes = [
        Node(
            public_ip="1.2.3.5",
            private_ip="10.0.0.2",
            num_gpus=4,
            nproc=8,
            ssh_user="test",
            ssh_pub_key_path=str(tmp_path / "test_key.pub"),
            ssh_port=22,
            ansible_playbook=None
        )
    ]
    config.add_cluster("test-cluster", head_node, worker_nodes)
    return "test-cluster"

def test_provision_cluster(tmp_path, mock_cluster):
    """Test the cluster provision command."""
    # Create test playbook
    playbook = tmp_path / "test.yml"
    playbook.write_text("""
    - hosts: all
      tasks:
        - name: Test task
          debug:
            msg: "Test message"
    """)

    # Test provision command with both head and worker playbooks
    result = runner.invoke(app, [
        "provision",
        mock_cluster,
        "--head-playbook", str(playbook),
        "--worker-playbook", str(playbook)
    ])
    assert result.exit_code == 0

    # Verify cluster configuration was updated
    cluster = config.get_cluster(mock_cluster)
    assert cluster.head_node.ansible_playbook == str(playbook)
    assert cluster.worker_nodes[0].ansible_playbook == str(playbook)

def test_provision_cluster_not_found():
    """Test provision command with non-existent cluster."""
    result = runner.invoke(app, [
        "provision",
        "nonexistent-cluster",
        "--head-playbook", "test.yml"
    ])
    assert result.exit_code == 1
    assert "not found" in result.stdout

def test_provision_cluster_head_only(tmp_path, mock_cluster):
    """Test provision command with head node only."""
    playbook = tmp_path / "head.yml"
    playbook.write_text("""
    - hosts: all
      tasks:
        - name: Head node task
          debug:
            msg: "Head node test"
    """)

    result = runner.invoke(app, [
        "provision",
        mock_cluster,
        "--head-playbook", str(playbook)
    ])
    assert result.exit_code == 0

    cluster = config.get_cluster(mock_cluster)
    assert cluster.head_node.ansible_playbook == str(playbook)
    assert cluster.worker_nodes[0].ansible_playbook is None
