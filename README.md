# Torch Submit

## Introduction

Torch Submit is a lightweight, easy-to-use tool for running distributed PyTorch jobs across multiple machines. It's designed for researchers and developers who:

- Have access to a bunch of machines with IP addresses
- Want to run distributed PyTorch jobs without the hassle
- Don't have the time, energy, or resources to set up complex cluster management systems like SLURM or Kubernetes
- Find Ray unnecessarily complex for their needs

If you've ever thought, "I just want to run my PyTorch job on these machines without losing my sanity," then Torch Submit is for you.

## Features

- Simple cluster configuration: Just add your machines' IP addresses
- Easy job submission: Run your PyTorch jobs with a single command
- Interactive cluster setup: Guided process to set up your compute resources
- Job management: Submit, stop, restart, and monitor your jobs
- Log tailing: Easily view the logs of your running jobs

## Installation

```bash
pip install torch-submit
```

or from source:

```bash
pip install -e . --prefix ~/.local
```

## Quick Start

1. Set up a cluster:
   ```bash
   torch-submit cluster create
   ```
   Follow the interactive prompts to add your machines.

2. Submit a job:
   ```bash
   torch-submit job submit --name "my_job" --working-dir ./my_project --cluster my_cluster
   ```

3. List running jobs:
   ```bash
   torch-submit job list
   ```

4. Tail logs:
   ```bash
   torch-submit logs tail <job_id>
   ```

5. Stop a job:
   ```bash
   torch-submit job stop <job_id>
   ```

6. Restart a stopped job:
   ```bash
   torch-submit job restart <job_id>
   ```

## Usage

### Cluster Management

- Create a cluster: `torch-submit cluster create`
- List clusters: `torch-submit cluster list`
- Remove a cluster: `torch-submit cluster remove <cluster_name>`

### Job Management

- Submit a job: `torch-submit job submit --name <job_name> --working-dir <path> --cluster <cluster_name>`
- List jobs: `torch-submit job list`
- Stop a job: `torch-submit job stop <job_id>`
- Restart a job: `torch-submit job restart <job_id>`

### Log Management

- Tail logs: `torch-submit logs tail <job_id>`

## Configuration

Torch Submit stores cluster configurations in `~/.cache/torch-submit/config.yaml`. You can manually edit this file if needed, but it's recommended to use the CLI commands for cluster management.

## Requirements

- Python 3.7+
- PyTorch (for your actual jobs)
- SSH access to all machines in your cluster

## Contributing

We welcome contributions! Please see our Contributing Guide for more details.

## License

Torch Submit is released under the MIT License. See the LICENSE file for more details.

## Support

If you encounter any issues or have questions, please file an issue on our GitHub Issues page.

Happy distributed training!