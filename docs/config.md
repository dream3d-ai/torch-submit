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
    - [Database().uri](#database()uri)
  - [DatabaseType](#databasetype)
    - [DatabaseType().connection_string](#databasetype()connection_string)
  - [Node](#node)
    - [Node.from_db](#nodefrom_db)
    - [Node().to_db](#node()to_db)

## Cluster

[Show source in config.py:56](../torch_submit/config.py#L56)

#### Signature

```python
class Cluster: ...
```



## Config

[Show source in config.py:127](../torch_submit/config.py#L127)

#### Signature

```python
class Config:
    def __init__(self): ...
```

### Config().add_cluster

[Show source in config.py:190](../torch_submit/config.py#L190)

#### Signature

```python
def add_cluster(self, name: str, head_node: Node, worker_nodes: List[Node]): ...
```

#### See also

- [Node](#node)

### Config().add_db

[Show source in config.py:230](../torch_submit/config.py#L230)

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

[Show source in config.py:207](../torch_submit/config.py#L207)

#### Signature

```python
def add_worker_node(self, cluster_name: str, worker_node: Node): ...
```

#### See also

- [Node](#node)

### Config().get_cluster

[Show source in config.py:199](../torch_submit/config.py#L199)

#### Signature

```python
def get_cluster(self, cluster_name: str) -> Cluster: ...
```

#### See also

- [Cluster](#cluster)

### Config().get_db

[Show source in config.py:250](../torch_submit/config.py#L250)

#### Signature

```python
def get_db(self, db_name: str) -> Database: ...
```

#### See also

- [Database](#database)

### Config().list_clusters

[Show source in config.py:204](../torch_submit/config.py#L204)

#### Signature

```python
def list_clusters(self) -> List[str]: ...
```

### Config().list_dbs

[Show source in config.py:255](../torch_submit/config.py#L255)

#### Signature

```python
def list_dbs(self) -> List[str]: ...
```

### Config().load_config

[Show source in config.py:134](../torch_submit/config.py#L134)

#### Signature

```python
def load_config(self): ...
```

### Config().remove_cluster

[Show source in config.py:194](../torch_submit/config.py#L194)

#### Signature

```python
def remove_cluster(self, name: str): ...
```

### Config().remove_db

[Show source in config.py:245](../torch_submit/config.py#L245)

#### Signature

```python
def remove_db(self, name: str): ...
```

### Config().remove_worker_node

[Show source in config.py:213](../torch_submit/config.py#L213)

#### Signature

```python
def remove_worker_node(self, cluster_name: str, worker_node_ip: str): ...
```

### Config().save_config

[Show source in config.py:150](../torch_submit/config.py#L150)

#### Signature

```python
def save_config(self): ...
```

### Config().update_cluster

[Show source in config.py:223](../torch_submit/config.py#L223)

#### Signature

```python
def update_cluster(self, name: str, head_node: Node, worker_nodes: List[Node]): ...
```

#### See also

- [Node](#node)

### Config().update_db

[Show source in config.py:258](../torch_submit/config.py#L258)

#### Signature

```python
def update_db(
    self, type: str, name: str, address: str, port: int, username: str, password: str
): ...
```



## Database

[Show source in config.py:76](../torch_submit/config.py#L76)

#### Signature

```python
class Database: ...
```

### Database.from_db

[Show source in config.py:87](../torch_submit/config.py#L87)

#### Signature

```python
@classmethod
def from_db(cls, row: str): ...
```

### Database().to_db

[Show source in config.py:102](../torch_submit/config.py#L102)

#### Signature

```python
def to_db(self): ...
```

### Database().uri

[Show source in config.py:98](../torch_submit/config.py#L98)

#### Signature

```python
@property
def uri(self): ...
```



## DatabaseType

[Show source in config.py:61](../torch_submit/config.py#L61)

#### Signature

```python
class DatabaseType(str, Enum): ...
```

### DatabaseType().connection_string

[Show source in config.py:65](../torch_submit/config.py#L65)

#### Signature

```python
@property
def connection_string(self): ...
```



## Node

[Show source in config.py:11](../torch_submit/config.py#L11)

#### Signature

```python
class Node: ...
```

### Node.from_db

[Show source in config.py:26](../torch_submit/config.py#L26)

#### Signature

```python
@classmethod
def from_db(cls, row: str): ...
```

### Node().to_db

[Show source in config.py:40](../torch_submit/config.py#L40)

#### Signature

```python
def to_db(self): ...
```