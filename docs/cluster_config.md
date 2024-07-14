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
    - [Node.from_db](#nodefrom_db)
    - [Node().to_db](#node()to_db)

## Cluster

[Show source in cluster_config.py:52](../torch_submit/cluster_config.py#L52)

#### Signature

```python
class Cluster: ...
```



## ClusterConfig

[Show source in cluster_config.py:57](../torch_submit/cluster_config.py#L57)

#### Signature

```python
class ClusterConfig:
    def __init__(self): ...
```

### ClusterConfig().add_cluster

[Show source in cluster_config.py:103](../torch_submit/cluster_config.py#L103)

#### Signature

```python
def add_cluster(self, name: str, head_node: Node, worker_nodes: List[Node]): ...
```

#### See also

- [Node](#node)

### ClusterConfig().add_worker_node

[Show source in cluster_config.py:120](../torch_submit/cluster_config.py#L120)

#### Signature

```python
def add_worker_node(self, cluster_name: str, worker_node: Node): ...
```

#### See also

- [Node](#node)

### ClusterConfig().get_cluster

[Show source in cluster_config.py:112](../torch_submit/cluster_config.py#L112)

#### Signature

```python
def get_cluster(self, cluster_name: str) -> Cluster: ...
```

#### See also

- [Cluster](#cluster)

### ClusterConfig().list_clusters

[Show source in cluster_config.py:117](../torch_submit/cluster_config.py#L117)

#### Signature

```python
def list_clusters(self) -> List[str]: ...
```

### ClusterConfig().load_config

[Show source in cluster_config.py:63](../torch_submit/cluster_config.py#L63)

#### Signature

```python
def load_config(self): ...
```

### ClusterConfig().remove_cluster

[Show source in cluster_config.py:107](../torch_submit/cluster_config.py#L107)

#### Signature

```python
def remove_cluster(self, name: str): ...
```

### ClusterConfig().remove_worker_node

[Show source in cluster_config.py:126](../torch_submit/cluster_config.py#L126)

#### Signature

```python
def remove_worker_node(self, cluster_name: str, worker_node_ip: str): ...
```

### ClusterConfig().save_config

[Show source in cluster_config.py:75](../torch_submit/cluster_config.py#L75)

#### Signature

```python
def save_config(self): ...
```

### ClusterConfig().update_cluster

[Show source in cluster_config.py:136](../torch_submit/cluster_config.py#L136)

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

### Node.from_db

[Show source in cluster_config.py:22](../torch_submit/cluster_config.py#L22)

#### Signature

```python
@classmethod
def from_db(cls, row: str): ...
```

### Node().to_db

[Show source in cluster_config.py:36](../torch_submit/cluster_config.py#L36)

#### Signature

```python
def to_db(self): ...
```