# Cli

[Torch-submit Index](./README.md#torch-submit-index) / Cli

> Auto-generated documentation for [cli](../torch_submit/cli.py) module.

- [Cli](#cli)
  - [main](#main)
  - [version_callback](#version_callback)

## main

[Show source in cli.py:20](../torch_submit/cli.py#L20)

#### Signature

```python
@app.callback()
def main(
    version: bool = typer.Option(
        None,
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Show the version and exit.",
    )
): ...
```



## version_callback

[Show source in cli.py:14](../torch_submit/cli.py#L14)

#### Signature

```python
def version_callback(value: bool): ...
```