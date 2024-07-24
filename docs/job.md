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

Manages job-related operations and database interactions.

#### Signature

```python
class JobManager:
    def __init__(
        self, db_path: str = os.path.expanduser("~/.cache/torch-submit/jobs.db")
    ): ...
```

### JobManager().add_job

[Show source in job.py:49](../torch_submit/job.py#L49)

Add a new job to the database.

#### Arguments

- [Job](#job) *Job* - The job to be added.

#### Signature

```python
def add_job(self, job: Job): ...
```

#### See also

- [Job](./types.md#job)

### JobManager().check_job_status

[Show source in job.py:96](../torch_submit/job.py#L96)

Check the current status of a job.

#### Arguments

- [Job](#job) *Job* - The job to check.

#### Returns

- `str` - The current status of the job.

#### Raises

- `RuntimeError` - If an unknown job status is encountered.

#### Signature

```python
def check_job_status(self, job: Job) -> str: ...
```

#### See also

- [Job](./types.md#job)

### JobManager().close

[Show source in job.py:239](../torch_submit/job.py#L239)

Close the database connection.

#### Signature

```python
def close(self): ...
```

### JobManager().create_table

[Show source in job.py:30](../torch_submit/job.py#L30)

Create the jobs table if it doesn't exist.

#### Signature

```python
def create_table(self): ...
```

### JobManager().delete_all_jobs

[Show source in job.py:234](../torch_submit/job.py#L234)

Delete all jobs from the database.

#### Signature

```python
def delete_all_jobs(self): ...
```

### JobManager().delete_job

[Show source in job.py:225](../torch_submit/job.py#L225)

Delete a job from the database.

#### Arguments

- `job_id` *str* - The ID of the job to delete.

#### Signature

```python
def delete_job(self, job_id: str): ...
```

### JobManager().get_all_jobs_with_status

[Show source in job.py:173](../torch_submit/job.py#L173)

Retrieve all jobs and update their statuses.

#### Returns

- `List[Job]` - A list of all jobs with updated statuses.

#### Signature

```python
def get_all_jobs_with_status(self) -> List[Job]: ...
```

#### See also

- [Job](./types.md#job)

### JobManager().get_job

[Show source in job.py:64](../torch_submit/job.py#L64)

Retrieve a job by its ID or name.

#### Arguments

- `job_id_or_name` *str* - The ID or name of the job.

#### Returns

- `Optional[Job]` - The retrieved job, or None if not found.

#### Signature

```python
def get_job(self, job_id_or_name: str) -> Optional[Job]: ...
```

#### See also

- [Job](./types.md#job)

### JobManager().list_jobs

[Show source in job.py:87](../torch_submit/job.py#L87)

Retrieve all jobs from the database.

#### Returns

- `List[Job]` - A list of all jobs.

#### Signature

```python
def list_jobs(self) -> List[Job]: ...
```

#### See also

- [Job](./types.md#job)

### JobManager().migrate_table

[Show source in job.py:243](../torch_submit/job.py#L243)

Perform any necessary database migrations.

#### Signature

```python
def migrate_table(self): ...
```

### JobManager().update_job_pids

[Show source in job.py:209](../torch_submit/job.py#L209)

Update the process IDs for a job in the database.

#### Arguments

- `job_id` *str* - The ID of the job to update.
pids (Dict[Node, int]): A dictionary mapping nodes to process IDs.

#### Signature

```python
def update_job_pids(self, job_id: str, pids: Dict[Node, int]): ...
```

#### See also

- [Node](./config.md#node)

### JobManager().update_job_status

[Show source in job.py:192](../torch_submit/job.py#L192)

Update the status of a job in the database.

#### Arguments

- `job_id` *str* - The ID of the job to update.
- `status` *JobStatus* - The new status of the job.

#### Raises

- `ValueError` - If an invalid job status is provided.

#### Signature

```python
def update_job_status(self, job_id: str, status: JobStatus): ...
```

#### See also

- [JobStatus](./types.md#jobstatus)