# Utils

[Torch-submit Index](./README.md#torch-submit-index) / Utils

> Auto-generated documentation for [utils](../torch_submit/utils.py) module.

- [Utils](#utils)
  - [generate_friendly_name](#generate_friendly_name)
  - [get_job_metadata](#get_job_metadata)

## generate_friendly_name

[Show source in utils.py:6](../torch_submit/utils.py#L6)

Generate a friendly, human-readable name for a job.

This function creates a name by combining a random adjective, a random animal noun,
and a random 4-digit number. The name format is 'adjective-noun-number'.

#### Returns

A friendly name string in the format 'adjective-noun-number'.

#### Examples

```python
>>> generate_friendly_name()
'happy-panda-3721'
```

#### Signature

```python
def generate_friendly_name() -> str: ...
```



## get_job_metadata

[Show source in utils.py:58](../torch_submit/utils.py#L58)

Retrieve job metadata from the '.torch/job.json' file.

This function attempts to read and parse the job metadata stored in the
'.torch/job.json' file in the current working directory.

#### Returns

A dictionary containing job metadata if the file exists and can be parsed
successfully, or None if the file is not found.

#### Raises

- `json.JSONDecodeError` - If the file exists but contains invalid JSON.

#### Examples

```python
>>> metadata = get_job_metadata()
>>> if metadata:
...     print(f"Job ID: {metadata.get('id')}")
... else:
...     print("No job metadata found.")
```

#### Signature

```python
def get_job_metadata() -> Optional[Dict[str, str]]: ...
```