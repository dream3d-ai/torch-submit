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
    - [Database().__eq__](#database()__eq__)
    - [Database().__hash__](#database()__hash__)
    - [Database().__post_init__](#database()__post_init__)
    - [Database().__str__](#database()__str__)
    - [Database.from_db](#databasefrom_db)
    - [Database().to_db](#database()to_db)
    - [Database().uri](#database()uri)
  - [DatabaseType](#databasetype)
    - [DatabaseType().connection_string](#databasetype()connection_string)
  - [Node](#node)
    - [Node().__eq__](#node()__eq__)
    - [Node().__hash__](#node()__hash__)
    - [Node().__post_init__](#node()__post_init__)
    - [Node().__str__](#node()__str__)
    - [Node.from_db](#nodefrom_db)
    - [Node().to_db](#node()to_db)

## Cluster

[Show source in config.py:99](../torch_submit/config.py#L99)

Represents a cluster of nodes.

#### Attributes

- `head_node` *Node* - The head node of the cluster.
- `worker_nodes` *List[Node]* - A list of worker nodes in the cluster.

#### Signature

```python
class Cluster: ...
```



## Config

[Show source in config.py:239](../torch_submit/config.py#L239)

Manages the configuration for clusters and databases.

This class handles loading, saving, and manipulating the configuration
for clusters and databases used in the torch-submit system.

#### Signature

```python
class Config:
    def __init__(self): ...
```

### Config().add_cluster

[Show source in config.py:311](../torch_submit/config.py#L311)

Add a new cluster to the configuration.

#### Arguments

- `name` *str* - The name of the cluster.
- `head_node` *Node* - The head node of the cluster.
- `worker_nodes` *List[Node]* - The list of worker nodes in the cluster.

#### Signature

```python
def add_cluster(self, name: str, head_node: Node, worker_nodes: List[Node]): ...
```

#### See also

- [Node](#node)

### Config().add_db

[Show source in config.py:407](../torch_submit/config.py#L407)

Add a new database to the configuration.

#### Arguments

- `type` *DatabaseType* - The type of the database.
- `name` *str* - The name of the database configuration.
- `address` *str* - The address of the database server.
- `port` *int* - The port number for the database connection.
- `username` *str* - The username for database authentication.
- `password` *str* - The password for database authentication.

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

[Show source in config.py:356](../torch_submit/config.py#L356)

Add a worker node to a cluster.

#### Arguments

- `cluster_name` *str* - The name of the cluster.
- `worker_node` *Node* - The worker node to add.

#### Raises

- `ValueError` - If the cluster is not found in the configuration.

#### Signature

```python
def add_worker_node(self, cluster_name: str, worker_node: Node): ...
```

#### See also

- [Node](#node)

### Config().get_cluster

[Show source in config.py:332](../torch_submit/config.py#L332)

Get a cluster by its name.

#### Arguments

- `cluster_name` *str* - The name of the cluster.

#### Returns

- [Cluster](#cluster) - The requested cluster.

#### Raises

- `ValueError` - If the cluster is not found in the configuration.

#### Signature

```python
def get_cluster(self, cluster_name: str) -> Cluster: ...
```

#### See also

- [Cluster](#cluster)

### Config().get_db

[Show source in config.py:442](../torch_submit/config.py#L442)

Get a database configuration by its name.

#### Arguments

- `db_name` *str* - The name of the database configuration.

#### Returns

- [Database](#database) - The requested database configuration.

#### Raises

- `ValueError` - If the database configuration is not found.

#### Signature

```python
def get_db(self, db_name: str) -> Database: ...
```

#### See also

- [Database](#database)

### Config().list_clusters

[Show source in config.py:348](../torch_submit/config.py#L348)

Get a list of all cluster names.

#### Returns

- `List[str]` - A list of cluster names.

#### Signature

```python
def list_clusters(self) -> List[str]: ...
```

### Config().list_dbs

[Show source in config.py:458](../torch_submit/config.py#L458)

Get a list of all database configuration names.

#### Returns

- `List[str]` - A list of database configuration names.

#### Signature

```python
def list_dbs(self) -> List[str]: ...
```

### Config().load_config

[Show source in config.py:253](../torch_submit/config.py#L253)

Load the configuration from the YAML file.

#### Signature

```python
def load_config(self): ...
```

### Config().remove_cluster

[Show source in config.py:322](../torch_submit/config.py#L322)

Remove a cluster from the configuration.

#### Arguments

- `name` *str* - The name of the cluster to remove.

#### Signature

```python
def remove_cluster(self, name: str): ...
```

### Config().remove_db

[Show source in config.py:432](../torch_submit/config.py#L432)

Remove a database from the configuration.

#### Arguments

- `name` *str* - The name of the database configuration to remove.

#### Signature

```python
def remove_db(self, name: str): ...
```

### Config().remove_worker_node

[Show source in config.py:371](../torch_submit/config.py#L371)

Remove a worker node from a cluster.

#### Arguments

- `cluster_name` *str* - The name of the cluster.
- `worker_node_ip` *str* - The IP address of the worker node to remove.

#### Raises

- `ValueError` - If the cluster is not found in the configuration.

#### Signature

```python
def remove_worker_node(self, cluster_name: str, worker_node_ip: str): ...
```

### Config().save_config

[Show source in config.py:270](../torch_submit/config.py#L270)

Save the current configuration to the YAML file.

#### Signature

```python
def save_config(self): ...
```

### Config().update_cluster

[Show source in config.py:390](../torch_submit/config.py#L390)

Update an existing cluster in the configuration.

#### Arguments

- `name` *str* - The name of the cluster to update.
- `head_node` *Node* - The new head node for the cluster.
- `worker_nodes` *List[Node]* - The new list of worker nodes for the cluster.

#### Raises

- `ValueError` - If the cluster is not found in the configuration.

#### Signature

```python
def update_cluster(self, name: str, head_node: Node, worker_nodes: List[Node]): ...
```

#### See also

- [Node](#node)

### Config().update_db

[Show source in config.py:466](../torch_submit/config.py#L466)

Update an existing database configuration.

#### Arguments

- `type` *str* - The type of the database.
- `name` *str* - The name of the database configuration to update.
- `address` *str* - The new address of the database server.
- `port` *int* - The new port number for the database connection.
- `username` *str* - The new username for database authentication.
- `password` *str* - The new password for database authentication.

#### Raises

- `ValueError` - If the specified database configuration is not found.

#### Signature

```python
def update_db(
    self, type: str, name: str, address: str, port: int, username: str, password: str
): ...
```



## Database

[Show source in config.py:141](../torch_submit/config.py#L141)

Represents a database configuration.

#### Attributes

- `address` *str* - The address of the database server.
- `port` *int* - The port number for the database connection.
- `username` *str* - The username for database authentication.
password (str | None): The password for database authentication, if required.
- `type` *DatabaseType* - The type of the database (e.g., PostgreSQL, MySQL).

#### Signature

```python
class Database: ...
```

### Database().__eq__

[Show source in config.py:221](../torch_submit/config.py#L221)

Check if two Database objects are equal.

#### Arguments

- `other` - Another object to compare with.

#### Returns

- `bool` - True if the objects are equal, False otherwise.

#### Signature

```python
def __eq__(self, other): ...
```

### Database().__hash__

[Show source in config.py:207](../torch_submit/config.py#L207)

Return a hash value for the Database object.

#### Returns

- `int` - A hash value based on the database attributes.

#### Signature

```python
def __hash__(self): ...
```

### Database().__post_init__

[Show source in config.py:158](../torch_submit/config.py#L158)

Initialize the Database object after creation.

#### Signature

```python
def __post_init__(self): ...
```

### Database().__str__

[Show source in config.py:199](../torch_submit/config.py#L199)

Return a string representation of the Database object.

#### Returns

- `str` - A string representation of the Database object.

#### Signature

```python
def __str__(self): ...
```

### Database.from_db

[Show source in config.py:163](../torch_submit/config.py#L163)

Create a Database object from a database row string.

#### Arguments

- `row` *str* - A string representation of the database data.

#### Returns

- [Database](#database) - A new Database object created from the row data.

#### Signature

```python
@classmethod
def from_db(cls, row: str): ...
```

### Database().to_db

[Show source in config.py:191](../torch_submit/config.py#L191)

Convert the Database object to a string representation for database storage.

#### Returns

- `str` - A string representation of the Database object.

#### Signature

```python
def to_db(self): ...
```

### Database().uri

[Show source in config.py:182](../torch_submit/config.py#L182)

Get the database URI for SQLAlchemy connection.

#### Returns

- `str` - The database URI.

#### Signature

```python
@property
def uri(self): ...
```



## DatabaseType

[Show source in config.py:111](../torch_submit/config.py#L111)

Enumeration of supported database types.

#### Attributes

- `POSTGRES` - PostgreSQL database type.
- `MYSQL` - MySQL database type.

#### Signature

```python
class DatabaseType(str, Enum): ...
```

### DatabaseType().connection_string

[Show source in config.py:122](../torch_submit/config.py#L122)

Get the SQLAlchemy connection string prefix for the database type.

#### Returns

- `str` - The connection string prefix.

#### Raises

- `ValueError` - If the database type is unknown.

#### Signature

```python
@property
def connection_string(self): ...
```



## Node

[Show source in config.py:11](../torch_submit/config.py#L11)

Represents a node in a cluster.

#### Attributes

- `public_ip` *str* - The public IP address of the node.
- `private_ip` *Optional[str]* - The private IP address of the node, if available.
- `num_gpus` *int* - The number of GPUs available on the node.
- `nproc` *int* - The number of processes that can run on the node.
- `ssh_user` *Optional[str]* - The SSH username for accessing the node, if available.
- `ssh_pub_key_path` *Optional[str]* - The path to the SSH public key file, if available.

#### Signature

```python
class Node: ...
```

### Node().__eq__

[Show source in config.py:84](../torch_submit/config.py#L84)

Check if two Node objects are equal.

#### Arguments

- `other` - Another object to compare with.

#### Returns

- `bool` - True if the objects are equal, False otherwise.

#### Signature

```python
def __eq__(self, other): ...
```

### Node().__hash__

[Show source in config.py:76](../torch_submit/config.py#L76)

Return a hash value for the Node object.

#### Returns

- `int` - A hash value based on the public IP address.

#### Signature

```python
def __hash__(self): ...
```

### Node().__post_init__

[Show source in config.py:30](../torch_submit/config.py#L30)

Initialize the Node object after creation.

#### Signature

```python
def __post_init__(self): ...
```

### Node().__str__

[Show source in config.py:68](../torch_submit/config.py#L68)

Return a string representation of the Node object.

#### Returns

- `str` - A string representation of the Node object.

#### Signature

```python
def __str__(self): ...
```

### Node.from_db

[Show source in config.py:38](../torch_submit/config.py#L38)

Create a Node object from a database row string.

#### Arguments

- `row` *str* - A string representation of the node data.

#### Returns

- [Node](#node) - A new Node object created from the row data.

#### Signature

```python
@classmethod
def from_db(cls, row: str): ...
```

### Node().to_db

[Show source in config.py:60](../torch_submit/config.py#L60)

Convert the Node object to a string representation for database storage.

#### Returns

- `str` - A string representation of the Node object.

#### Signature

```python
def to_db(self): ...
```