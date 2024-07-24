# Cluster

[Torch-submit Index](../README.md#torch-submit-index) / [Commands](./index.md#commands) / Cluster

> Auto-generated documentation for [commands.cluster](../../torch_submit/commands/cluster.py) module.

- [Cluster](#cluster)
  - [create_cluster](#create_cluster)
  - [edit_cluster](#edit_cluster)
  - [list_clusters](#list_clusters)
  - [remove_cluster](#remove_cluster)

## create_cluster

[Show source in cluster.py:14](../../torch_submit/commands/cluster.py#L14)

Interactively create a new cluster configuration.

Prompts the user for cluster details such as name, head node, and worker nodes.
Adds the new cluster configuration to the config.

#### Signature

```python
@app.command("create")
def create_cluster(): ...
```



## edit_cluster

[Show source in cluster.py:129](../../torch_submit/commands/cluster.py#L129)

Edit an existing cluster configuration.

Prompts the user for new cluster details and updates the specified cluster configuration in the config.

#### Arguments

- `name` *str* - The name of the cluster to edit.

#### Signature

```python
@app.command("edit")
def edit_cluster(name: str): ...
```



## list_clusters

[Show source in cluster.py:77](../../torch_submit/commands/cluster.py#L77)

List all available clusters.

Retrieves the list of clusters from the config and displays them in a table format.

#### Signature

```python
@app.command("list")
def list_clusters(): ...
```



## remove_cluster

[Show source in cluster.py:112](../../torch_submit/commands/cluster.py#L112)

Remove a cluster configuration.

Prompts the user for confirmation before removing the specified cluster configuration from the config.

#### Arguments

- `name` *str* - The name of the cluster to remove.

#### Signature

```python
@app.command("remove")
def remove_cluster(name: str): ...
```