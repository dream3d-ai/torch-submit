import os
import sqlite3
import uuid
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .cluster_config import Node
from .connection import NodeConnection


@dataclass
class Job:
    id: str
    name: str
    status: str
    working_dir: str
    nodes: List[Node]
    cluster: str
    command: str
    max_restarts: int = 0
    num_gpus: Optional[int] = None
    pids: Dict[str, int] = field(default_factory=dict)

    @classmethod
    def from_db(cls, row: Tuple) -> "Job":
        return cls(
            id=row[0],
            name=row[1],
            status=row[2],
            working_dir=row[3],
            nodes=[Node.from_db(node) for node in row[4].split(",")],
            cluster=row[5],
            command=row[6],
        )

    def to_db(self) -> Tuple:
        return (
            self.id,
            self.name,
            self.status,
            self.working_dir,
            ",".join([node.to_db() for node in self.nodes]),
            self.cluster,
            self.command,
            self.max_restarts,
            self.num_gpus,
            ",".join([f"{k}:{v}" for k, v in self.pids.items()]),
        )


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
                pids TEXT DEFAULT NULL
            )
        """)

    def add_job(self, job: Job):
        self.conn.execute(
            """
            INSERT INTO jobs (id, name, status, working_dir, nodes, cluster, command, max_restarts, num_gpus, pids)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            job.to_db(),
        )
        self.conn.commit()

    def get_job(self, job_id: str) -> Optional[Job]:
        cursor = self.conn.execute("SELECT * FROM jobs WHERE id = ?", (job_id,))
        row = cursor.fetchone()
        if not row:
            return None
        return Job.from_db(row)

    def list_jobs(self) -> List[Job]:
        cursor = self.conn.execute("SELECT * FROM jobs")
        return [Job.from_db(row) for row in cursor.fetchall()]

    def check_job_status(self, job: Job) -> str:
        if job.status in ["stopped", "crashed"]:
            return job.status

        if job.status in ["submitted", "running", "started", "stopping"]:
            for node, pid in job.pids.items():
                try:
                    with NodeConnection(node, connect_timeout=5) as c:
                        result = c.run(
                            f"ps -p {pid}",
                            warn=True,
                            hide=True,
                        )
                        if result.ok and job.status == "submitted":
                            return "running"
                        elif result.ok and job.status == "stopping":
                            return "stopping"
                        elif not result.ok and job.status == "running":
                            return "crashed"
                        elif not result.ok and job.status == "stopping":
                            return "stopped"
                except Exception:
                    # If we can't connect to a node, we'll continue to the next one
                    continue

            # If we've checked all nodes and found no running processes
            return "crashed"

        return job.status  # Return the current status if it's not one we're updating

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

    def update_job_status(self, job_id: str, status: str):
        self.conn.execute("UPDATE jobs SET status = ? WHERE id = ?", (status, job_id))
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


def create_job(name: str, working_dir: str, nodes: List[str], cluster: str) -> Job:
    return Job(
        id=str(uuid.uuid4()),
        name=name,
        status="submitted",
        working_dir=working_dir,
        nodes=nodes,
        cluster=cluster,
        command="",
    )
