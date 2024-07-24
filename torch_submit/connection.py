from fabric import Connection

from .config import Node


class NodeConnection:
    """A context manager for handling SSH connections to a node."""

    def __init__(self, node: Node):
        """Initialize the NodeConnection with a Node object.

        Args:
            node (Node): The Node object representing the remote machine.
        """
        self.node = node

    def __enter__(self):
        """Establish an SSH connection to the node.

        Returns:
            Connection: The established SSH connection.
        """
        connect_kwargs = None
        if self.node.ssh_pub_key_path:
            connect_kwargs = {
                "key_filename": self.node.ssh_pub_key_path,
            }

        self.connection = Connection(
            self.node.public_ip, user=self.node.ssh_user, connect_kwargs=connect_kwargs
        )
        self.connection.open()
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close the SSH connection when exiting the context.

        Args:
            exc_type: The type of the exception that caused the context to be exited.
            exc_val: The instance of the exception that caused the context to be exited.
            exc_tb: A traceback object encapsulating the call stack at the point where the exception occurred.
        """
        self.connection.close()
