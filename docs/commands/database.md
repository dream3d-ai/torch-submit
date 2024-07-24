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

Prompts the user for database details such as name, type, address, port, username, and password.
Adds the new database configuration to the config.

#### Signature

```python
@app.command("create")
def create_database(): ...
```



## edit_database

[Show source in database.py:82](../../torch_submit/commands/database.py#L82)

Edit an existing database configuration.

Prompts the user for new database details and updates the specified database configuration in the config.

#### Arguments

- `name` *str* - The name of the database to edit.

#### Signature

```python
@app.command("edit")
def edit_database(name: str): ...
```



## list_databases

[Show source in database.py:34](../../torch_submit/commands/database.py#L34)

List all available databases.

Retrieves the list of databases from the config and displays them in a table format.

#### Signature

```python
@app.command("list")
def list_databases(): ...
```



## remove_database

[Show source in database.py:65](../../torch_submit/commands/database.py#L65)

Remove a database configuration.

Prompts the user for confirmation before removing the specified database configuration from the config.

#### Arguments

- `name` *str* - The name of the database to remove.

#### Signature

```python
@app.command("remove")
def remove_database(name: str): ...
```