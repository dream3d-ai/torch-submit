import os
from dataclasses import dataclass
from typing import Dict, List, Optional

import yaml


@dataclass
class Node:
    public_ip: str
    private_ip: Optional[str]
    num_gpus: int
    nproc: int


@dataclass
class Cluster:
    head_node: Node
    worker_nodes: List[Node]


class ClusterConfig:
    def __init__(self):
        self.config_path = os.path.expanduser("~/.cache/torch-submit/config.yaml")
        self.clusters: Dict[str, Cluster] = {}
        self.load_config()

    def load_config(self):
        if not os.path.exists(self.config_path):
            return

        with open(self.config_path, "r") as f:
            config = yaml.safe_load(f) or {}

        for cluster_name, cluster_data in config.get("clusters", {}).items():
            head_node = Node(**cluster_data["head_node"])
            worker_nodes = [Node(**node) for node in cluster_data["worker_nodes"]]
            self.clusters[cluster_name] = Cluster(head_node, worker_nodes)

    def save_config(self):
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        config = {"clusters": {}}
        for cluster_name, cluster in self.clusters.items():
            config["clusters"][cluster_name] = {
                "head_node": {
                    "public_ip": cluster.head_node.public_ip,
                    "private_ip": cluster.head_node.private_ip,
                    "num_gpus": cluster.head_node.num_gpus,
                    "nproc": cluster.head_node.nproc,
                },
                "worker_nodes": [
                    {
                        "public_ip": node.public_ip,
                        "private_ip": node.private_ip,
                        "num_gpus": node.num_gpus,
                        "nproc": node.nproc,
                    }
                    for node in cluster.worker_nodes
                ],
            }
        with open(self.config_path, "w") as f:
            yaml.dump(config, f)

    def add_cluster(self, name: str, head_node: Node, worker_nodes: List[Node]):
        self.clusters[name] = Cluster(head_node, worker_nodes)
        self.save_config()

    def remove_cluster(self, name: str):
        if name in self.clusters:
            del self.clusters[name]
            self.save_config()

    def get_cluster(self, cluster_name: str) -> Cluster:
        if cluster_name not in self.clusters:
            raise ValueError(f"Cluster '{cluster_name}' not found in config")
        return self.clusters[cluster_name]

    def list_clusters(self) -> List[str]:
        return list(self.clusters.keys())

    def add_worker_node(self, cluster_name: str, worker_node: Node):
        if cluster_name not in self.clusters:
            raise ValueError(f"Cluster '{cluster_name}' not found in config")
        self.clusters[cluster_name].worker_nodes.append(worker_node)
        self.save_config()

    def remove_worker_node(self, cluster_name: str, worker_node_ip: str):
        if cluster_name not in self.clusters:
            raise ValueError(f"Cluster '{cluster_name}' not found in config")
        self.clusters[cluster_name].worker_nodes = [
            node
            for node in self.clusters[cluster_name].worker_nodes
            if node.public_ip != worker_node_ip and node.private_ip != worker_node_ip
        ]
        self.save_config()

    def update_cluster(self, name: str, head_node: Node, worker_nodes: List[Node]):
        if name not in self.clusters:
            raise ValueError(f"Cluster '{name}' not found in config")
        self.clusters[name] = Cluster(head_node, worker_nodes)
        self.save_config()
