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

#### Signature

```python
@app.command("create")
def create_cluster(): ...
```



## edit_cluster

[Show source in cluster.py:113](../../torch_submit/commands/cluster.py#L113)

Edit an existing cluster configuration.

#### Signature

```python
@app.command("edit")
def edit_cluster(name: str): ...
```



## list_clusters

[Show source in cluster.py:72](../../torch_submit/commands/cluster.py#L72)

List all available clusters.

#### Signature

```python
@app.command("list")
def list_clusters(): ...
```



## remove_cluster

[Show source in cluster.py:103](../../torch_submit/commands/cluster.py#L103)

Remove a cluster configuration.

#### Signature

```python
@app.command("remove")
def remove_cluster(name: str): ...
```