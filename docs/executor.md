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

[Show source in executor.py:114](../torch_submit/executor.py#L114)

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

[Show source in executor.py:179](../torch_submit/executor.py#L179)

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

[Show source in executor.py:232](../torch_submit/executor.py#L232)

Clean up the remote directories on all nodes.

This method removes the remote directory created for the job on each node.
If the cleanup fails on any node, a warning message is printed.

#### Signature

```python
def cleanup(self): ...
```

### BaseExecutor().execute

[Show source in executor.py:146](../torch_submit/executor.py#L146)

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

[Show source in executor.py:133](../torch_submit/executor.py#L133)

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

[Show source in executor.py:249](../torch_submit/executor.py#L249)

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

[Show source in executor.py:269](../torch_submit/executor.py#L269)

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

[Show source in executor.py:427](../torch_submit/executor.py#L427)

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

[Show source in executor.py:445](../torch_submit/executor.py#L445)

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

[Show source in executor.py:486](../torch_submit/executor.py#L486)

#### Signature

```python
class JobExecutionManager: ...
```

### JobExecutionManager.cancel_job

[Show source in executor.py:501](../torch_submit/executor.py#L501)

#### Signature

```python
@staticmethod
def cancel_job(job: Job): ...
```

#### See also

- [Job](./types.md#job)

### JobExecutionManager.submit_job

[Show source in executor.py:487](../torch_submit/executor.py#L487)

#### Signature

```python
@staticmethod
def submit_job(job: Job): ...
```

#### See also

- [Job](./types.md#job)



## OptunaExecutor

[Show source in executor.py:367](../torch_submit/executor.py#L367)

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

[Show source in executor.py:404](../torch_submit/executor.py#L404)

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

[Show source in executor.py:386](../torch_submit/executor.py#L386)

#### Signature

```python
def get_command(self, rank: int, env_vars: Optional[Dict[str, str]] = None): ...
```



## TorchrunExecutor

[Show source in executor.py:302](../torch_submit/executor.py#L302)

#### Signature

```python
class TorchrunExecutor(BaseExecutor):
    def __init__(self, job: Job): ...
```

#### See also

- [BaseExecutor](#baseexecutor)
- [Job](./types.md#job)

### TorchrunExecutor().get_command

[Show source in executor.py:307](../torch_submit/executor.py#L307)

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

A class to handle archiving of working directories for jobs.

This class creates a zip archive of the specified working directory, including job metadata
and excluding files specified in a .gitignore file.

#### Attributes

- `job_id` *str* - The ID of the job.
- `job_name` *str* - The name of the job.
- `output_dir` *str* - The directory where the archive will be saved.

#### Signature

```python
class WorkingDirectoryArchiver:
    def __init__(self, job_id: str, job_name: str): ...
```

### WorkingDirectoryArchiver().archive

[Show source in executor.py:48](../torch_submit/executor.py#L48)

Create a zip archive of the specified working directory.

This method reads the .gitignore file in the working directory to determine which files
to exclude from the archive. It also includes job metadata in the archive.

#### Arguments

- `working_dir` *str* - The path to the working directory to be archived.

#### Returns

- `str` - The path to the created zip archive.

#### Signature

```python
def archive(self, working_dir: str) -> str: ...
```