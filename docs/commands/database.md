# Database

[Torch-submit Index](../README.md#torch-submit-index) / [Commands](./index.md#commands) / Database

> Auto-generated documentation for [commands.database](../../torch_submit/commands/database.py) module.

- [Database](#database)
  - [create_database](#create_database)
  - [edit_database](#edit_database)
  - [list_databases](#list_databases)
  - [remove_database](#remove_database)

## create_database

[Show source in database.py:13](../../torch_submit/commands/database.py#L13)

Interactively create a new database configuration.

#### Signature

```python
@app.command("create")
def create_database(): ...
```



## edit_database

[Show source in database.py:66](../../torch_submit/commands/database.py#L66)

Edit an existing database configuration.

#### Signature

```python
@app.command("edit")
def edit_database(name: str): ...
```



## list_databases

[Show source in database.py:29](../../torch_submit/commands/database.py#L29)

List all available databases.

#### Signature

```python
@app.command("list")
def list_databases(): ...
```



## remove_database

[Show source in database.py:56](../../torch_submit/commands/database.py#L56)

Remove a database configuration.

#### Signature

```python
@app.command("remove")
def remove_database(name: str): ...
```