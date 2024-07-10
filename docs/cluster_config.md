# ClusterConfig

[Torch-submit Index](./README.md#torch-submit-index) / ClusterConfig

> Auto-generated documentation for [cluster_config](../torch_submit/cluster_config.py) module.

- [ClusterConfig](#clusterconfig)
  - [Cluster](#cluster)
  - [ClusterConfig](#clusterconfig-1)
    - [ClusterConfig().add_cluster](#clusterconfig()add_cluster)
    - [ClusterConfig().add_worker_node](#clusterconfig()add_worker_node)
    - [ClusterConfig().get_cluster](#clusterconfig()get_cluster)
    - [ClusterConfig().list_clusters](#clusterconfig()list_clusters)
    - [ClusterConfig().load_config](#clusterconfig()load_config)
    - [ClusterConfig().remove_cluster](#clusterconfig()remove_cluster)
    - [ClusterConfig().remove_worker_node](#clusterconfig()remove_worker_node)
    - [ClusterConfig().save_config](#clusterconfig()save_config)
    - [ClusterConfig().update_cluster](#clusterconfig()update_cluster)
  - [Node](#node)

## Cluster

[Show source in cluster_config.py:27](../torch_submit/cluster_config.py#L27)

#### Signature

```python
class Cluster: ...
```



## ClusterConfig

[Show source in cluster_config.py:32](../torch_submit/cluster_config.py#L32)

#### Signature

```python
class ClusterConfig:
    def __init__(self): ...
```

### ClusterConfig().add_cluster

[Show source in cluster_config.py:78](../torch_submit/cluster_config.py#L78)

#### Signature

```python
def add_cluster(self, name: str, head_node: Node, worker_nodes: List[Node]): ...
```

#### See also

- [Node](#node)

### ClusterConfig().add_worker_node

[Show source in cluster_config.py:95](../torch_submit/cluster_config.py#L95)

#### Signature

```python
def add_worker_node(self, cluster_name: str, worker_node: Node): ...
```

#### See also

- [Node](#node)

### ClusterConfig().get_cluster

[Show source in cluster_config.py:87](../torch_submit/cluster_config.py#L87)

#### Signature

```python
def get_cluster(self, cluster_name: str) -> Cluster: ...
```

#### See also

- [Cluster](#cluster)

### ClusterConfig().list_clusters

[Show source in cluster_config.py:92](../torch_submit/cluster_config.py#L92)

#### Signature

```python
def list_clusters(self) -> List[str]: ...
```

### ClusterConfig().load_config

[Show source in cluster_config.py:38](../torch_submit/cluster_config.py#L38)

#### Signature

```python
def load_config(self): ...
```

### ClusterConfig().remove_cluster

[Show source in cluster_config.py:82](../torch_submit/cluster_config.py#L82)

#### Signature

```python
def remove_cluster(self, name: str): ...
```

### ClusterConfig().remove_worker_node

[Show source in cluster_config.py:101](../torch_submit/cluster_config.py#L101)

#### Signature

```python
def remove_worker_node(self, cluster_name: str, worker_node_ip: str): ...
```

### ClusterConfig().save_config

[Show source in cluster_config.py:50](../torch_submit/cluster_config.py#L50)

#### Signature

```python
def save_config(self): ...
```

### ClusterConfig().update_cluster

[Show source in cluster_config.py:111](../torch_submit/cluster_config.py#L111)

#### Signature

```python
def update_cluster(self, name: str, head_node: Node, worker_nodes: List[Node]): ...
```

#### See also

- [Node](#node)



## Node

[Show source in cluster_config.py:9](../torch_submit/cluster_config.py#L9)

#### Signature

```python
class Node: ...
```