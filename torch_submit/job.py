import os
import sqlite3
import uuid
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Job:
    id: str
    name: str
    status: str
    working_dir: str
    nodes: List[str]
    cluster: str


class JobManager:
    def __init__(
        self, db_path: str = os.path.expanduser("~/.cache/torch-submit/jobs.db")
    ):
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id TEXT PRIMARY KEY,
                name TEXT,
                status TEXT,
                working_dir TEXT,
                nodes TEXT,
                cluster TEXT
            )
        """)

    def add_job(self, job: Job):
        self.conn.execute(
            """
            INSERT INTO jobs (id, name, status, working_dir, nodes, cluster)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            (
                job.id,
                job.name,
                job.status,
                job.working_dir,
                ",".join(job.nodes),
                job.cluster,
            ),
        )
        self.conn.commit()

    def get_job(self, job_id: str) -> Optional[Job]:
        cursor = self.conn.execute("SELECT * FROM jobs WHERE id = ?", (job_id,))
        row = cursor.fetchone()
        if row:
            return Job(
                id=row[0],
                name=row[1],
                status=row[2],
                working_dir=row[3],
                nodes=row[4].split(","),
                cluster=row[5],
            )
        return None

    def list_jobs(self) -> List[Job]:
        cursor = self.conn.execute("SELECT * FROM jobs")
        return [
            Job(
                id=row[0],
                name=row[1],
                status=row[2],
                working_dir=row[3],
                nodes=row[4].split(","),
                cluster=row[5],
            )
            for row in cursor.fetchall()
        ]

    def update_job_status(self, job_id: str, status: str):
        self.conn.execute("UPDATE jobs SET status = ? WHERE id = ?", (status, job_id))
        self.conn.commit()

    def delete_job(self, job_id: str):
        self.conn.execute("DELETE FROM jobs WHERE id = ?", (job_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()


def create_job(name: str, working_dir: str, nodes: List[str], cluster: str) -> Job:
    return Job(
        id=str(uuid.uuid4()),
        name=name,
        status="submitted",
        working_dir=working_dir,
        nodes=nodes,
        cluster=cluster,
    )
