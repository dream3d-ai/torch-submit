# Config

[Torch-submit Index](./README.md#torch-submit-index) / Config

> Auto-generated documentation for [config](../torch_submit/config.py) module.

- [Config](#config)
  - [Cluster](#cluster)
  - [Config](#config-1)
    - [Config().add_cluster](#config()add_cluster)
    - [Config().add_db](#config()add_db)
    - [Config().add_worker_node](#config()add_worker_node)
    - [Config().get_cluster](#config()get_cluster)
    - [Config().get_db](#config()get_db)
    - [Config().list_clusters](#config()list_clusters)
    - [Config().list_dbs](#config()list_dbs)
    - [Config().load_config](#config()load_config)
    - [Config().remove_cluster](#config()remove_cluster)
    - [Config().remove_db](#config()remove_db)
    - [Config().remove_worker_node](#config()remove_worker_node)
    - [Config().save_config](#config()save_config)
    - [Config().update_cluster](#config()update_cluster)
    - [Config().update_db](#config()update_db)
  - [Database](#database)
    - [Database.from_db](#databasefrom_db)
    - [Database().to_db](#database()to_db)
    - [Database().to_uri](#database()to_uri)
  - [DatabaseType](#databasetype)
  - [Node](#node)
    - [Node.from_db](#nodefrom_db)
    - [Node().to_db](#node()to_db)

## Cluster

[Show source in config.py:55](../torch_submit/config.py#L55)

#### Signature

```python
class Cluster: ...
```



## Config

[Show source in config.py:118](../torch_submit/config.py#L118)

#### Signature

```python
class Config:
    def __init__(self): ...
```

### Config().add_cluster

[Show source in config.py:181](../torch_submit/config.py#L181)

#### Signature

```python
def add_cluster(self, name: str, head_node: Node, worker_nodes: List[Node]): ...
```

#### See also

- [Node](#node)

### Config().add_db

[Show source in config.py:221](../torch_submit/config.py#L221)

#### Signature

```python
def add_db(
    self,
    type: DatabaseType,
    name: str,
    address: str,
    port: int,
    username: str,
    password: str,
): ...
```

#### See also

- [DatabaseType](#databasetype)

### Config().add_worker_node

[Show source in config.py:198](../torch_submit/config.py#L198)

#### Signature

```python
def add_worker_node(self, cluster_name: str, worker_node: Node): ...
```

#### See also

- [Node](#node)

### Config().get_cluster

[Show source in config.py:190](../torch_submit/config.py#L190)

#### Signature

```python
def get_cluster(self, cluster_name: str) -> Cluster: ...
```

#### See also

- [Cluster](#cluster)

### Config().get_db

[Show source in config.py:240](../torch_submit/config.py#L240)

#### Signature

```python
def get_db(self, db_name: str) -> Database: ...
```

#### See also

- [Database](#database)

### Config().list_clusters

[Show source in config.py:195](../torch_submit/config.py#L195)

#### Signature

```python
def list_clusters(self) -> List[str]: ...
```

### Config().list_dbs

[Show source in config.py:245](../torch_submit/config.py#L245)

#### Signature

```python
def list_dbs(self) -> List[str]: ...
```

### Config().load_config

[Show source in config.py:125](../torch_submit/config.py#L125)

#### Signature

```python
def load_config(self): ...
```

### Config().remove_cluster

[Show source in config.py:185](../torch_submit/config.py#L185)

#### Signature

```python
def remove_cluster(self, name: str): ...
```

### Config().remove_db

[Show source in config.py:235](../torch_submit/config.py#L235)

#### Signature

```python
def remove_db(self, name: str): ...
```

### Config().remove_worker_node

[Show source in config.py:204](../torch_submit/config.py#L204)

#### Signature

```python
def remove_worker_node(self, cluster_name: str, worker_node_ip: str): ...
```

### Config().save_config

[Show source in config.py:141](../torch_submit/config.py#L141)

#### Signature

```python
def save_config(self): ...
```

### Config().update_cluster

[Show source in config.py:214](../torch_submit/config.py#L214)

#### Signature

```python
def update_cluster(self, name: str, head_node: Node, worker_nodes: List[Node]): ...
```

#### See also

- [Node](#node)

### Config().update_db

[Show source in config.py:248](../torch_submit/config.py#L248)

#### Signature

```python
def update_db(
    self, type: str, name: str, address: str, port: int, username: str, password: str
): ...
```



## Database

[Show source in config.py:66](../torch_submit/config.py#L66)

#### Signature

```python
class Database: ...
```

### Database.from_db

[Show source in config.py:77](../torch_submit/config.py#L77)

#### Signature

```python
@classmethod
def from_db(cls, row: str): ...
```

### Database().to_db

[Show source in config.py:93](../torch_submit/config.py#L93)

#### Signature

```python
def to_db(self): ...
```

### Database().to_uri

[Show source in config.py:88](../torch_submit/config.py#L88)

#### Signature

```python
def to_uri(self): ...
```



## DatabaseType

[Show source in config.py:60](../torch_submit/config.py#L60)

#### Signature

```python
class DatabaseType(str, Enum): ...
```



## Node

[Show source in config.py:10](../torch_submit/config.py#L10)

#### Signature

```python
class Node: ...
```

### Node.from_db

[Show source in config.py:25](../torch_submit/config.py#L25)

#### Signature

```python
@classmethod
def from_db(cls, row: str): ...
```

### Node().to_db

[Show source in config.py:39](../torch_submit/config.py#L39)

#### Signature

```python
def to_db(self): ...
```