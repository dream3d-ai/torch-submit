import os
import zipfile

from fabric import Connection
from invoke import UnexpectedExit
from rich.console import Console
from rich.progress import Progress

from .job import Job

console = Console()


class WorkingDirectoryArchiver:
    @staticmethod
    def archive(working_dir: str, output_dir: str) -> str:
        archive_name = f"{os.path.basename(working_dir)}.zip"
        archive_path = os.path.join(output_dir, archive_name)

        with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(working_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, working_dir)
                    zipf.write(file_path, arcname)

        return archive_path


class RemoteExecutor:
    def __init__(self, job: Job):
        self.job = job
        self.remote_dir = f"/tmp/torch_submit_job_{self.job.id}"

    def execute(self):
        with Progress() as progress:
            task = progress.add_task(
                "[green]Executing job...", total=len(self.job.nodes)
            )

            for node in self.job.nodes:
                try:
                    with Connection(node) as conn:
                        self._setup_remote_env(conn)
                        self._copy_working_dir(conn)
                        self._run_job(conn)
                except Exception as e:
                    console.print(
                        f"[bold red]Error executing job on node {node}:[/bold red] {str(e)}"
                    )
                finally:
                    progress.update(task, advance=1)

    def _setup_remote_env(self, conn: Connection):
        conn.run(f"mkdir -p {self.remote_dir}")

    def _copy_working_dir(self, conn: Connection):
        remote_zip_path = f"{self.remote_dir}/working_dir.zip"
        conn.put(self.job.working_dir, remote_zip_path)
        conn.run(f"unzip -q -o {remote_zip_path} -d {self.remote_dir}")

    def _run_job(self, conn: Connection):
        # This is a placeholder. In a real scenario, you'd run your PyTorch job here.
        # You might use something like:
        # conn.run(f"cd {self.remote_dir} && python main.py")

        # For now, we'll just create a dummy log file
        conn.run(f"echo 'Job {self.job.id} started' > {self.remote_dir}/job.log")

    def cleanup(self):
        for node in self.job.nodes:
            try:
                with Connection(node) as conn:
                    conn.run(f"rm -rf {self.remote_dir}")
            except UnexpectedExit:
                console.print(
                    f"[bold yellow]Warning: Could not clean up {self.remote_dir} on {node}[/bold yellow]"
                )


class JobExecutionManager:
    @staticmethod
    def submit_job(job: Job):
        executor = RemoteExecutor(job)
        try:
            executor.execute()
            console.print(
                f"[bold green]Job {job.id} submitted successfully[/bold green]"
            )
        except Exception as e:
            console.print(
                f"[bold red]Error submitting job {job.id}:[/bold red] {str(e)}"
            )
            executor.cleanup()

    @staticmethod
    def cancel_job(job: Job):
        executor = RemoteExecutor(job)
        try:
            executor.cleanup()
            console.print(
                f"[bold green]Job {job.id} cancelled successfully[/bold green]"
            )
        except Exception as e:
            console.print(
                f"[bold red]Error cancelling job {job.id}:[/bold red] {str(e)}"
            )
