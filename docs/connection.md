# Connection

[Torch-submit Index](./README.md#torch-submit-index) / Connection

> Auto-generated documentation for [connection](../torch_submit/connection.py) module.

- [Connection](#connection)
  - [NodeConnection](#nodeconnection)
    - [NodeConnection().__enter__](#nodeconnection()__enter__)
    - [NodeConnection().__exit__](#nodeconnection()__exit__)

## NodeConnection

[Show source in connection.py:6](../torch_submit/connection.py#L6)

A context manager for handling SSH connections to a node.

#### Signature

```python
class NodeConnection:
    def __init__(self, node: Node): ...
```

#### See also

- [Node](./config.md#node)

### NodeConnection().__enter__

[Show source in connection.py:17](../torch_submit/connection.py#L17)

Establish an SSH connection to the node.

#### Returns

- `Connection` - The established SSH connection.

#### Signature

```python
def __enter__(self): ...
```

### NodeConnection().__exit__

[Show source in connection.py:35](../torch_submit/connection.py#L35)

Close the SSH connection when exiting the context.

#### Arguments

- `exc_type` - The type of the exception that caused the context to be exited.
- `exc_val` - The instance of the exception that caused the context to be exited.
- `exc_tb` - A traceback object encapsulating the call stack at the point where the exception occurred.

#### Signature

```python
def __exit__(self, exc_type, exc_val, exc_tb): ...
```