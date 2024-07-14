import os
import sqlite3
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List, Optional

from .cluster_config import Node
from .connection import NodeConnection
from .types import Job, JobStatus


class JobManager:
    def __init__(
        self, db_path: str = os.path.expanduser("~/.cache/torch-submit/jobs.db")
    ):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(db_path)
        self.create_table()
        self.migrate_table()

    def create_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id TEXT PRIMARY KEY,
                name TEXT,
                status TEXT,
                working_dir TEXT,
                nodes TEXT,
                cluster TEXT,
                command TEXT,
                max_restarts INTEGER DEFAULT 0,
                num_gpus INTEGER DEFAULT NULL,
                pids TEXT DEFAULT NULL,
                executor TEXT DEFAULT NULL
            )
        """)

    def add_job(self, job: Job):
        self.conn.execute(
            """
            INSERT INTO jobs (id, name, status, working_dir, nodes, cluster, command, max_restarts, num_gpus, pids, executor)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            job.to_db(),
        )
        self.conn.commit()

    def get_job(self, job_id_or_name: str) -> Optional[Job]:
        # Try to get by id first
        cursor = self.conn.execute("SELECT * FROM jobs WHERE id = ?", (job_id_or_name,))
        row = cursor.fetchone()
        if not row:
            # If not found by id, try to get by name
            cursor = self.conn.execute(
                "SELECT * FROM jobs WHERE name = ?", (job_id_or_name,)
            )
            row = cursor.fetchone()

        if not row:
            return None
        return Job.from_db(row)

    def list_jobs(self) -> List[Job]:
        cursor = self.conn.execute("SELECT * FROM jobs")
        return [Job.from_db(row) for row in cursor.fetchall()]

    def check_job_status(self, job: Job) -> str:
        if job.status in [JobStatus.STOPPED, JobStatus.FINISHED, JobStatus.CRASHED]:
            return job.status

        if job.status in [JobStatus.SUBMITTED, JobStatus.RUNNING, JobStatus.STOPPING]:
            node_statuses = []

            def check_node_status(node):
                try:
                    with NodeConnection(node) as c:
                        result = c.run(
                            f"ps -p {job.pids[node]}",
                            warn=True,
                            hide=True,
                        )

                        if result.ok and job.status in [
                            JobStatus.SUBMITTED,
                            JobStatus.RUNNING,
                        ]:
                            return JobStatus.RUNNING
                        elif result.ok and job.status == JobStatus.STOPPING:
                            return JobStatus.STOPPING
                        elif not result.ok and job.status == JobStatus.STOPPING:
                            return JobStatus.STOPPED
                        elif not result.ok:
                            exit_code_result = c.run(
                                f"cat {self.remote_dir}/exit_code.log",
                                warn=True,
                                hide=True,
                            )
                            if (
                                exit_code_result.ok
                                and exit_code_result.stdout.strip() == "0"
                            ):
                                return JobStatus.FINISHED
                            else:
                                return JobStatus.CRASHED
                        else:
                            raise RuntimeError(
                                f"Unknown job status: {job.status} for node {node}, {result.stdout}"
                            )

                except Exception:
                    return JobStatus.UNKNOWN

            with ThreadPoolExecutor() as executor:
                node_statuses = list(executor.map(check_node_status, job.nodes))

            # Aggregate job status across all nodes
            if all(status == JobStatus.RUNNING for status in node_statuses):
                return JobStatus.RUNNING
            elif all(status == JobStatus.STOPPED for status in node_statuses):
                return JobStatus.STOPPED
            elif all(status == JobStatus.FINISHED for status in node_statuses):
                return JobStatus.FINISHED
            elif any(status == JobStatus.CRASHED for status in node_statuses):
                return JobStatus.CRASHED
            elif any(status == JobStatus.STOPPING for status in node_statuses):
                return JobStatus.STOPPING
            else:
                return JobStatus.UNKNOWN

        raise RuntimeError(f"Unknown job status: {job.status}")

    def get_all_jobs_with_status(self) -> List[Job]:
        jobs = self.list_jobs()
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.check_job_status, job) for job in jobs]
            for job, future in zip(jobs, futures):
                try:
                    new_status = future.result()
                    if new_status != job.status:
                        self.update_job_status(job.id, new_status)
                        job.status = new_status
                except Exception as exc:
                    print(f"Job {job.id} generated an exception: {exc}")
        return jobs

    def update_job_status(self, job_id: str, status: JobStatus):
        if not isinstance(status, JobStatus):
            raise ValueError(f"Invalid job status: {status}")
        self.conn.execute(
            "UPDATE jobs SET status = ? WHERE id = ?", (status.value, job_id)
        )
        self.conn.commit()

    def update_job_pids(self, job_id: str, pids: Dict[Node, int]):
        self.conn.execute(
            "UPDATE jobs SET pids = ? WHERE id = ?",
            (
                ",".join([f"{node.public_ip}:{pid}" for node, pid in pids.items()]),
                job_id,
            ),
        )
        self.conn.commit()

    def delete_job(self, job_id: str):
        self.conn.execute("DELETE FROM jobs WHERE id = ?", (job_id,))
        self.conn.commit()

    def delete_all_jobs(self):
        self.conn.execute("DELETE FROM jobs")
        self.conn.commit()

    def close(self):
        self.conn.close()

    def migrate_table(self):
        # Add any necessary migration steps here
        pass
