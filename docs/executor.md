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
    - [WorkingDirectoryArchiver.archive](#workingdirectoryarchiverarchive)

## JobExecutionManager

[Show source in executor.py:123](../torch_submit/executor.py#L123)

#### Signature

```python
class JobExecutionManager: ...
```

### JobExecutionManager.cancel_job

[Show source in executor.py:138](../torch_submit/executor.py#L138)

#### Signature

```python
@staticmethod
def cancel_job(job: Job): ...
```

#### See also

- [Job](./job.md#job)

### JobExecutionManager.submit_job

[Show source in executor.py:124](../torch_submit/executor.py#L124)

#### Signature

```python
@staticmethod
def submit_job(job: Job): ...
```

#### See also

- [Job](./job.md#job)



## RemoteExecutor

[Show source in executor.py:33](../torch_submit/executor.py#L33)

#### Signature

```python
class RemoteExecutor:
    def __init__(self, job: Job): ...
```

#### See also

- [Job](./job.md#job)

### RemoteExecutor().cleanup

[Show source in executor.py:112](../torch_submit/executor.py#L112)

#### Signature

```python
def cleanup(self): ...
```

### RemoteExecutor().execute

[Show source in executor.py:39](../torch_submit/executor.py#L39)

#### Signature

```python
def execute(self): ...
```



## WorkingDirectoryArchiver

[Show source in executor.py:15](../torch_submit/executor.py#L15)

#### Signature

```python
class WorkingDirectoryArchiver: ...
```

### WorkingDirectoryArchiver.archive

[Show source in executor.py:16](../torch_submit/executor.py#L16)

#### Signature

```python
@staticmethod
def archive(working_dir: str, output_dir: str) -> str: ...
```