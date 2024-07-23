# Job

[Torch-submit Index](./README.md#torch-submit-index) / Job

> Auto-generated documentation for [job](../torch_submit/job.py) module.

- [Job](#job)
  - [JobManager](#jobmanager)
    - [JobManager().add_job](#jobmanager()add_job)
    - [JobManager().check_job_status](#jobmanager()check_job_status)
    - [JobManager().close](#jobmanager()close)
    - [JobManager().create_table](#jobmanager()create_table)
    - [JobManager().delete_all_jobs](#jobmanager()delete_all_jobs)
    - [JobManager().delete_job](#jobmanager()delete_job)
    - [JobManager().get_all_jobs_with_status](#jobmanager()get_all_jobs_with_status)
    - [JobManager().get_job](#jobmanager()get_job)
    - [JobManager().list_jobs](#jobmanager()list_jobs)
    - [JobManager().migrate_table](#jobmanager()migrate_table)
    - [JobManager().update_job_pids](#jobmanager()update_job_pids)
    - [JobManager().update_job_status](#jobmanager()update_job_status)

## JobManager

[Show source in job.py:14](../torch_submit/job.py#L14)

#### Signature

```python
class JobManager:
    def __init__(
        self, db_path: str = os.path.expanduser("~/.cache/torch-submit/jobs.db")
    ): ...
```

### JobManager().add_job

[Show source in job.py:41](../torch_submit/job.py#L41)

#### Signature

```python
def add_job(self, job: Job): ...
```

#### See also

- [Job](./types.md#job)

### JobManager().check_job_status

[Show source in job.py:70](../torch_submit/job.py#L70)

#### Signature

```python
def check_job_status(self, job: Job) -> str: ...
```

#### See also

- [Job](./types.md#job)

### JobManager().close

[Show source in job.py:176](../torch_submit/job.py#L176)

#### Signature

```python
def close(self): ...
```

### JobManager().create_table

[Show source in job.py:23](../torch_submit/job.py#L23)

#### Signature

```python
def create_table(self): ...
```

### JobManager().delete_all_jobs

[Show source in job.py:172](../torch_submit/job.py#L172)

#### Signature

```python
def delete_all_jobs(self): ...
```

### JobManager().delete_job

[Show source in job.py:168](../torch_submit/job.py#L168)

#### Signature

```python
def delete_job(self, job_id: str): ...
```

### JobManager().get_all_jobs_with_status

[Show source in job.py:136](../torch_submit/job.py#L136)

#### Signature

```python
def get_all_jobs_with_status(self) -> List[Job]: ...
```

#### See also

- [Job](./types.md#job)

### JobManager().get_job

[Show source in job.py:51](../torch_submit/job.py#L51)

#### Signature

```python
def get_job(self, job_id_or_name: str) -> Optional[Job]: ...
```

#### See also

- [Job](./types.md#job)

### JobManager().list_jobs

[Show source in job.py:66](../torch_submit/job.py#L66)

#### Signature

```python
def list_jobs(self) -> List[Job]: ...
```

#### See also

- [Job](./types.md#job)

### JobManager().migrate_table

[Show source in job.py:179](../torch_submit/job.py#L179)

#### Signature

```python
def migrate_table(self): ...
```

### JobManager().update_job_pids

[Show source in job.py:158](../torch_submit/job.py#L158)

#### Signature

```python
def update_job_pids(self, job_id: str, pids: Dict[Node, int]): ...
```

#### See also

- [Node](./cluster_config.md#node)

### JobManager().update_job_status

[Show source in job.py:150](../torch_submit/job.py#L150)

#### Signature

```python
def update_job_status(self, job_id: str, status: JobStatus): ...
```

#### See also

- [JobStatus](./types.md#jobstatus)