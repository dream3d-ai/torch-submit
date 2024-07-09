# Job

[Torch-submit Index](../README.md#torch-submit-index) / [Commands](./index.md#commands) / Job

> Auto-generated documentation for [commands.job](../../torch_submit/commands/job.py) module.

- [Job](#job)
  - [list_jobs](#list_jobs)
  - [print_logs](#print_logs)
  - [restart_job](#restart_job)
  - [stop_job](#stop_job)
  - [submit](#submit)

## list_jobs

[Show source in job.py:120](../../torch_submit/commands/job.py#L120)

List all submitted jobs.

#### Signature

```python
@app.command("list")
def list_jobs(): ...
```



## print_logs

[Show source in job.py:100](../../torch_submit/commands/job.py#L100)

Tail the logs of a specific job.

#### Signature

```python
@app.command("logs")
def print_logs(job_id: str, tail: bool = typer.Option(False, help="Tail the logs")): ...
```



## restart_job

[Show source in job.py:177](../../torch_submit/commands/job.py#L177)

Restart a stopped job.

#### Signature

```python
@app.command("restart")
def restart_job(job_id: str): ...
```



## stop_job

[Show source in job.py:152](../../torch_submit/commands/job.py#L152)

Stop a running job.

#### Signature

```python
@app.command("stop")
def stop_job(job_id: str): ...
```



## submit

[Show source in job.py:21](../../torch_submit/commands/job.py#L21)

Submit a new job to a specified cluster.

#### Signature

```python
@app.command("submit")
def submit(
    cluster: str = typer.Option(..., help="Name of the cluster to use"),
    name: Optional[str] = typer.Option(
        None, help="Job name (optional, will be auto-generated if not provided)"
    ),
    working_dir: str = typer.Option("./", help="Path to working directory"),
    max_restarts: int = typer.Option(0, help="Maximum number of restarts for the job"),
    num_gpus: Optional[int] = typer.Option(
        None, help="Number of GPUs to use per node (optional, defaults to all available)"
    ),
    command: List[str] = typer.Argument(
        ..., help="The command to run, e.g. 'python main.py'"
    ),
    tail: bool = typer.Option(False, help="Tail the logs after submitting the job"),
): ...
```