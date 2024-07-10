# Job

[Torch-submit Index](./README.md#torch-submit-index) / Job

> Auto-generated documentation for [job](../torch_submit/job.py) module.

- [Job](#job)
  - [Job](#job-1)
  - [JobManager](#jobmanager)
    - [JobManager().add_job](#jobmanager()add_job)
    - [JobManager().check_job_status](#jobmanager()check_job_status)
    - [JobManager().close](#jobmanager()close)
    - [JobManager().create_table](#jobmanager()create_table)
    - [JobManager().delete_job](#jobmanager()delete_job)
    - [JobManager().get_all_jobs_with_status](#jobmanager()get_all_jobs_with_status)
    - [JobManager().get_job](#jobmanager()get_job)
    - [JobManager().list_jobs](#jobmanager()list_jobs)
    - [JobManager().migrate_table](#jobmanager()migrate_table)
    - [JobManager().update_job_pids](#jobmanager()update_job_pids)
    - [JobManager().update_job_status](#jobmanager()update_job_status)
  - [create_job](#create_job)

## Job

[Show source in job.py:12](../torch_submit/job.py#L12)

#### Signature

```python
class Job: ...
```



## JobManager

[Show source in job.py:25](../torch_submit/job.py#L25)

#### Signature

```python
class JobManager:
    def __init__(
        self, db_path: str = os.path.expanduser("~/.cache/torch-submit/jobs.db")
    ): ...
```

### JobManager().add_job

[Show source in job.py:50](../torch_submit/job.py#L50)

#### Signature

```python
def add_job(self, job: Job): ...
```

#### See also

- [Job](#job)

### JobManager().check_job_status

[Show source in job.py:120](../torch_submit/job.py#L120)

#### Signature

```python
def check_job_status(self, job: Job, cluster_config: ClusterConfig) -> str: ...
```

#### See also

- [ClusterConfig](./cluster_config.md#clusterconfig)
- [Job](#job)

### JobManager().close

[Show source in job.py:177](../torch_submit/job.py#L177)

#### Signature

```python
def close(self): ...
```

### JobManager().create_table

[Show source in job.py:34](../torch_submit/job.py#L34)

#### Signature

```python
def create_table(self): ...
```

### JobManager().delete_job

[Show source in job.py:173](../torch_submit/job.py#L173)

#### Signature

```python
def delete_job(self, job_id: str): ...
```

### JobManager().get_all_jobs_with_status

[Show source in job.py:150](../torch_submit/job.py#L150)

#### Signature

```python
def get_all_jobs_with_status(self, cluster_config: ClusterConfig) -> List[Job]: ...
```

#### See also

- [ClusterConfig](./cluster_config.md#clusterconfig)
- [Job](#job)

### JobManager().get_job

[Show source in job.py:76](../torch_submit/job.py#L76)

#### Signature

```python
def get_job(self, job_id: str) -> Optional[Job]: ...
```

#### See also

- [Job](#job)

### JobManager().list_jobs

[Show source in job.py:98](../torch_submit/job.py#L98)

#### Signature

```python
def list_jobs(self) -> List[Job]: ...
```

#### See also

- [Job](#job)

### JobManager().migrate_table

[Show source in job.py:180](../torch_submit/job.py#L180)

#### Signature

```python
def migrate_table(self): ...
```

### JobManager().update_job_pids

[Show source in job.py:163](../torch_submit/job.py#L163)

#### Signature

```python
def update_job_pids(self, job_id: str, pids: Dict[Node, int]): ...
```

#### See also

- [Node](./cluster_config.md#node)

### JobManager().update_job_status

[Show source in job.py:159](../torch_submit/job.py#L159)

#### Signature

```python
def update_job_status(self, job_id: str, status: str): ...
```



## create_job

[Show source in job.py:185](../torch_submit/job.py#L185)

#### Signature

```python
def create_job(name: str, working_dir: str, nodes: List[str], cluster: str) -> Job: ...
```

#### See also

- [Job](#job)