# Types

[Torch-submit Index](./README.md#torch-submit-index) / Types

> Auto-generated documentation for [types](../torch_submit/types.py) module.

- [Types](#types)
  - [Executor](#executor)
  - [Job](#job)
    - [Job.from_db](#jobfrom_db)
    - [Job().get_executor](#job()get_executor)
    - [Job().to_db](#job()to_db)
  - [JobStatus](#jobstatus)

## Executor

[Show source in types.py:8](../torch_submit/types.py#L8)

#### Signature

```python
class Executor(str, Enum): ...
```



## Job

[Show source in types.py:25](../torch_submit/types.py#L25)

#### Signature

```python
class Job: ...
```

### Job.from_db

[Show source in types.py:38](../torch_submit/types.py#L38)

#### Signature

```python
@classmethod
def from_db(cls, row: Tuple) -> "Job": ...
```

### Job().get_executor

[Show source in types.py:78](../torch_submit/types.py#L78)

#### Signature

```python
def get_executor(self): ...
```

### Job().to_db

[Show source in types.py:63](../torch_submit/types.py#L63)

#### Signature

```python
def to_db(self) -> Tuple: ...
```



## JobStatus

[Show source in types.py:14](../torch_submit/types.py#L14)

#### Signature

```python
class JobStatus(str, Enum): ...
```