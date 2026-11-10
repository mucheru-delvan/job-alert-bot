import json
from pathlib import Path

SEEN_FILE = Path("seen_jobs.json")


def job_key(job):
    return f"{job.source}:{job.job_id}"


def load_seen(path=SEEN_FILE):
    try:
        return set(json.loads(path.read_text()))
    except FileNotFoundError:
        return set()


def save_seen(seen, path=SEEN_FILE):
    path.write_text(json.dumps(sorted(seen)))


def new_jobs(jobs, seen):
    return [job for job in jobs if job_key(job) not in seen]