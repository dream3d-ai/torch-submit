from fabric import Connection

from .cluster_config import Node


class NodeConnection:
    def __init__(self, node: Node):
        self.node = node

    def __enter__(self):
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
        self.connection.close()
