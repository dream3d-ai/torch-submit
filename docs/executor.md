# Executor

[Torch-submit Index](./README.md#torch-submit-index) / Executor

> Auto-generated documentation for [executor](../torch_submit/executor.py) module.

- [Executor](#executor)
  - [BaseExecutor](#baseexecutor)
    - [BaseExecutor()._run_job](#baseexecutor()_run_job)
    - [BaseExecutor().cleanup](#baseexecutor()cleanup)
    - [BaseExecutor().execute](#baseexecutor()execute)
    - [BaseExecutor().get_command](#baseexecutor()get_command)
  - [DistributedExecutor](#distributedexecutor)
    - [DistributedExecutor().get_command](#distributedexecutor()get_command)
  - [DockerDistributedExecutor](#dockerdistributedexecutor)
    - [DockerDistributedExecutor().get_command](#dockerdistributedexecutor()get_command)
  - [JobExecutionManager](#jobexecutionmanager)
    - [JobExecutionManager.cancel_job](#jobexecutionmanagercancel_job)
    - [JobExecutionManager.submit_job](#jobexecutionmanagersubmit_job)
  - [OptunaExecutor](#optunaexecutor)
    - [OptunaExecutor().execute](#optunaexecutor()execute)
    - [OptunaExecutor().get_command](#optunaexecutor()get_command)
  - [TorchrunExecutor](#torchrunexecutor)
    - [TorchrunExecutor().get_command](#torchrunexecutor()get_command)
  - [WorkingDirectoryArchiver](#workingdirectoryarchiver)
    - [WorkingDirectoryArchiver().archive](#workingdirectoryarchiver()archive)

## BaseExecutor

[Show source in executor.py:74](../torch_submit/executor.py#L74)

Base class for executing jobs across a cluster.

This class defines the structure for executing a job. Sub-classes must implement the get_command
method, which generates the command to be executed on each node in the cluster. The execute method
runs this command on each node, managing the setup and execution process.

#### Methods

- `get_command(rank` - int): Abstract method to create the command for the given node rank.
execute() -> Dict[Node, int]: Executes the job command on each node in the cluster and returns
                              a dictionary mapping nodes to their process IDs.

#### Signature

```python
class BaseExecutor(ABC):
    def __init__(self, job: Job): ...
```

#### See also

- [Job](./types.md#job)

### BaseExecutor()._run_job

[Show source in executor.py:139](../torch_submit/executor.py#L139)

Run the job on the specified node.

This method changes the directory to the remote directory, runs the provided torchrun command
along with the job command, and captures the process ID of the running job.

#### Arguments

- `conn` *Connection* - The connection object to the node.
- `executor_command` *str* - The command with which to run the user-provided script.
- `node_rank` *int* - The rank of the node in the cluster.

#### Returns

- `int` - The process ID of the running job.

#### Signature

```python
def _run_job(
    self, conn: Connection, node_rank: int, env_vars: Optional[Dict[str, str]] = None
): ...
```

### BaseExecutor().cleanup

[Show source in executor.py:192](../torch_submit/executor.py#L192)

Clean up the remote directories on all nodes.

This method removes the remote directory created for the job on each node.
If the cleanup fails on any node, a warning message is printed.

#### Signature

```python
def cleanup(self): ...
```

### BaseExecutor().execute

[Show source in executor.py:106](../torch_submit/executor.py#L106)

Execute the job command on each node in the cluster.

This method sets up the remote environment, copies the working directory,
and runs the job command on each node in the cluster. It manages the setup
and execution process, handling any exceptions that occur during execution.

#### Returns

- `Dict[Node,` *int]* - A dictionary mapping nodes to their process IDs.

#### Signature

```python
def execute(self, env_vars: Optional[Dict[str, str]] = None) -> Dict[Node, int]: ...
```

#### See also

- [Node](./config.md#node)

### BaseExecutor().get_command

[Show source in executor.py:93](../torch_submit/executor.py#L93)

Generate the command to be executed on the given node rank.

#### Arguments

- `rank` *int* - The rank of the node in the cluster.

#### Returns

- `str` - The command to be executed on the node.

#### Signature

```python
@abstractmethod
def get_command(self, rank: int, env_vars: Optional[Dict[str, str]] = None): ...
```



## DistributedExecutor

[Show source in executor.py:209](../torch_submit/executor.py#L209)

The DistributedExecutor is responsible for setting up the environment for running
distributed PyTorch jobs. It ensures that the necessary environment variables are set
for the torch distributed environment, including MASTER_ADDR, MASTER_PORT, WORLD_SIZE,
and NODE_RANK. These variables are essential for coordinating the distributed training
process across multiple nodes and GPUs.

Exposes the following environment variables to the user script:
    - MASTER_ADDR: The address of the master node.
    - MASTER_PORT: The port on which the master node is listening.
    - WORLD_SIZE: The total number of processes participating in the job.
    - NODE_RANK: The rank of the current node.
    - LOCAL_WORLD_SIZE: The number of processes on the current node.

#### Signature

```python
class DistributedExecutor(BaseExecutor):
    def __init__(self, job: Job): ...
```

#### See also

- [BaseExecutor](#baseexecutor)
- [Job](./types.md#job)

### DistributedExecutor().get_command

[Show source in executor.py:229](../torch_submit/executor.py#L229)

Constructs the command to run the job with the torch distributed environment variables set.

This method sets up the necessary environment variables for a distributed torch run, including
MASTER_ADDR, MASTER_PORT, WORLD_SIZE, and NODE_RANK. It then appends the user-provided command
to these environment variables.

#### Arguments

- `rank` *int* - The rank of the current node.

#### Returns

- `str` - The full command to run the job with the necessary environment variables.

#### Signature

```python
def get_command(self, rank: int, env_vars: Optional[Dict[str, str]] = None): ...
```



## DockerDistributedExecutor

[Show source in executor.py:382](../torch_submit/executor.py#L382)

EXPERIMENTAL:
DockerDistributedExecutor is an executor that runs distributed jobs inside Docker containers.

This executor extends the DistributedExecutor to provide Docker support, allowing the user to run
distributed jobs in isolated Docker environments with GPU support.

Exposes the following environment variables to the user script:
    - MASTER_ADDR: The address of the master node.
    - MASTER_PORT: The port on which the master node is listening.
    - WORLD_SIZE: The total number of processes participating in the job.
    - NODE_RANK: The rank of the current node.

#### Signature

```python
class DockerDistributedExecutor(DistributedExecutor):
    def __init__(self, job: Job): ...
```

#### See also

- [DistributedExecutor](#distributedexecutor)
- [Job](./types.md#job)

### DockerDistributedExecutor().get_command

[Show source in executor.py:400](../torch_submit/executor.py#L400)

Constructs the command to run the job with the torch distributed environment variables set.

This method sets up the necessary environment variables for a distributed torch run, including
MASTER_ADDR, MASTER_PORT, WORLD_SIZE, and NODE_RANK. It then appends the user-provided command
to these environment variables.

#### Arguments

- `rank` *int* - The rank of the current node.

#### Returns

- `str` - The full command to run the job with the necessary environment variables.

#### Signature

```python
def get_command(self, rank: int, env_vars: Optional[Dict[str, str]] = None): ...
```



## JobExecutionManager

[Show source in executor.py:441](../torch_submit/executor.py#L441)

#### Signature

```python
class JobExecutionManager: ...
```

### JobExecutionManager.cancel_job

[Show source in executor.py:456](../torch_submit/executor.py#L456)

#### Signature

```python
@staticmethod
def cancel_job(job: Job): ...
```

#### See also

- [Job](./types.md#job)

### JobExecutionManager.submit_job

[Show source in executor.py:442](../torch_submit/executor.py#L442)

#### Signature

```python
@staticmethod
def submit_job(job: Job): ...
```

#### See also

- [Job](./types.md#job)



## OptunaExecutor

[Show source in executor.py:327](../torch_submit/executor.py#L327)

The OptunaExecutor sets up and manages the execution of Optuna distributed optimization jobs.

The head node runs a SQLite database for Optuna and exposes it to the cluster. Each node in the cluster
runs a single Optuna process that will utilize all the GPUs available on that node.

Exposes the following environment variables to the user script:
    - MASTER_ADDR: The address of the master node.
    - MASTER_PORT: The port on which the master node is listening.
    - WORLD_SIZE: The total number of processes participating in the job.
    - NODE_RANK: The rank of the current node.
    - STUDY_NAME: The name of the Optuna study (the job name).
    - DATABASE_URI: The URI of the database.

#### Signature

```python
class OptunaExecutor(DistributedExecutor):
    def __init__(self, job: Job): ...
```

#### See also

- [DistributedExecutor](#distributedexecutor)
- [Job](./types.md#job)

### OptunaExecutor().execute

[Show source in executor.py:364](../torch_submit/executor.py#L364)

Set up the database on the head node and then run the DistributedExecutor execute method.

This method first sets up the SQLite database on the head node for Optuna. After the database
is set up, it calls the execute method of the DistributedExecutor to run the job command on
each node in the cluster.

#### Returns

- `Dict[Node,` *int]* - A dictionary mapping nodes to their process IDs.

#### Signature

```python
def execute(self) -> Dict[Node, int]: ...
```

#### See also

- [Node](./config.md#node)

### OptunaExecutor().get_command

[Show source in executor.py:346](../torch_submit/executor.py#L346)

#### Signature

```python
def get_command(self, rank: int, env_vars: Optional[Dict[str, str]] = None): ...
```



## TorchrunExecutor

[Show source in executor.py:262](../torch_submit/executor.py#L262)

#### Signature

```python
class TorchrunExecutor(BaseExecutor):
    def __init__(self, job: Job): ...
```

#### See also

- [BaseExecutor](#baseexecutor)
- [Job](./types.md#job)

### TorchrunExecutor().get_command

[Show source in executor.py:267](../torch_submit/executor.py#L267)

Constructs the command to run the job with torchrun.

This method sets up the necessary parameters for a torchrun command, including
the number of nodes, the number of processes per node, the rendezvous backend,
the rendezvous endpoint, the job ID, and the maximum number of restarts.

#### Arguments

- `rank` *int* - The rank of the current node.

#### Returns

- `str` - The full command to run the job with torchrun.

#### Signature

```python
def get_command(self, rank: int, env_vars: Optional[Dict[str, str]] = None): ...
```



## WorkingDirectoryArchiver

[Show source in executor.py:21](../torch_submit/executor.py#L21)

#### Signature

```python
class WorkingDirectoryArchiver:
    def __init__(self, job_id: str, job_name: str): ...
```

### WorkingDirectoryArchiver().archive

[Show source in executor.py:29](../torch_submit/executor.py#L29)

#### Signature

```python
def archive(self, working_dir: str) -> str: ...
```