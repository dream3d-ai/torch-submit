# Types

[Torch-submit Index](./README.md#torch-submit-index) / Types

> Auto-generated documentation for [types](../torch_submit/types.py) module.

- [Types](#types)
  - [Executor](#executor)
  - [Job](#job)
    - [Job().__post_init__](#job()__post_init__)
    - [Job().__str__](#job()__str__)
    - [Job.from_db](#jobfrom_db)
    - [Job().get_executor](#job()get_executor)
    - [Job().to_db](#job()to_db)
  - [JobStatus](#jobstatus)

## Executor

[Show source in types.py:8](../torch_submit/types.py#L8)

Enumeration of different types of executors.

#### Signature

```python
class Executor(str, Enum): ...
```



## Job

[Show source in types.py:27](../torch_submit/types.py#L27)

A class representing a job to be executed.

#### Attributes

- `id` *str* - The ID of the job.
- `name` *str* - The name of the job.
- `status` *JobStatus* - The current status of the job.
- `working_dir` *str* - The working directory for the job.
- `nodes` *List[Node]* - The list of nodes assigned to the job.
- `cluster` *str* - The cluster to which the job belongs.
- `command` *str* - The command to be executed for the job.
- `max_restarts` *int* - The maximum number of restarts allowed for the job.
- `num_gpus` *Optional[int]* - The number of GPUs allocated for the job.
pids (Dict[Node, int]): A dictionary mapping nodes to process IDs.
- [Executor](./executor.md#executor) *Executor* - The executor type for the job.
- `docker_image` *Optional[str]* - The Docker image to be used for the job.
- `database` *Optional[Database]* - The database configuration for the job.
- `optuna_port` *Optional[int]* - The port for Optuna executor.

#### Signature

```python
class Job: ...
```

### Job().__post_init__

[Show source in types.py:63](../torch_submit/types.py#L63)

Post-initialization checks for the Job class.

#### Signature

```python
def __post_init__(self): ...
```

### Job().__str__

[Show source in types.py:161](../torch_submit/types.py#L161)

Return a string representation of the Job instance.

#### Returns

- `str` - A string representation of the Job instance.

#### Signature

```python
def __str__(self): ...
```

### Job.from_db

[Show source in types.py:68](../torch_submit/types.py#L68)

Create a Job instance from a database row.

#### Arguments

- `row` *Tuple* - A tuple representing a row from the database.

#### Returns

- [Job](#job) - A Job instance created from the database row.

#### Signature

```python
@classmethod
def from_db(cls, row: Tuple) -> "Job": ...
```

### Job().get_executor

[Show source in types.py:129](../torch_submit/types.py#L129)

Get the appropriate executor instance for the job.

#### Returns

An instance of the appropriate executor class.

#### Raises

- `ValueError` - If an unknown executor type is specified or if Docker image is not supported for the executor.

#### Signature

```python
def get_executor(self): ...
```

### Job().to_db

[Show source in types.py:105](../torch_submit/types.py#L105)

Convert the Job instance to a tuple for database storage.

#### Returns

- `Tuple` - A tuple representing the Job instance for database storage.

#### Signature

```python
def to_db(self) -> Tuple: ...
```



## JobStatus

[Show source in types.py:15](../torch_submit/types.py#L15)

Enumeration of different job statuses.

#### Signature

```python
class JobStatus(str, Enum): ...
```