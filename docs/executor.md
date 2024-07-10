# Executor

[Torch-submit Index](./README.md#torch-submit-index) / Executor

> Auto-generated documentation for [executor](../torch_submit/executor.py) module.

- [Executor](#executor)
  - [JobExecutionManager](#jobexecutionmanager)
    - [JobExecutionManager.cancel_job](#jobexecutionmanagercancel_job)
    - [JobExecutionManager.submit_job](#jobexecutionmanagersubmit_job)
  - [RemoteExecutor](#remoteexecutor)
    - [RemoteExecutor().cleanup](#remoteexecutor()cleanup)
    - [RemoteExecutor().execute](#remoteexecutor()execute)
  - [WorkingDirectoryArchiver](#workingdirectoryarchiver)
    - [WorkingDirectoryArchiver().archive](#workingdirectoryarchiver()archive)

## JobExecutionManager

[Show source in executor.py:169](../torch_submit/executor.py#L169)

#### Signature

```python
class JobExecutionManager: ...
```

### JobExecutionManager.cancel_job

[Show source in executor.py:184](../torch_submit/executor.py#L184)

#### Signature

```python
@staticmethod
def cancel_job(job: Job): ...
```

#### See also

- [Job](./job.md#job)

### JobExecutionManager.submit_job

[Show source in executor.py:170](../torch_submit/executor.py#L170)

#### Signature

```python
@staticmethod
def submit_job(job: Job): ...
```

#### See also

- [Job](./job.md#job)



## RemoteExecutor

[Show source in executor.py:72](../torch_submit/executor.py#L72)

#### Signature

```python
class RemoteExecutor:
    def __init__(self, job: Job): ...
```

#### See also

- [Job](./job.md#job)

### RemoteExecutor().cleanup

[Show source in executor.py:158](../torch_submit/executor.py#L158)

#### Signature

```python
def cleanup(self): ...
```

### RemoteExecutor().execute

[Show source in executor.py:78](../torch_submit/executor.py#L78)

#### Signature

```python
def execute(self) -> Dict[Node, int]: ...
```

#### See also

- [Node](./cluster_config.md#node)



## WorkingDirectoryArchiver

[Show source in executor.py:19](../torch_submit/executor.py#L19)

#### Signature

```python
class WorkingDirectoryArchiver:
    def __init__(self, job_id: str, job_name: str): ...
```

### WorkingDirectoryArchiver().archive

[Show source in executor.py:27](../torch_submit/executor.py#L27)

#### Signature

```python
def archive(self, working_dir: str) -> str: ...
```