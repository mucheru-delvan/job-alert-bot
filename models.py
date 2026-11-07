from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Job:
    source: str
    job_id: str
    title: str
    url: str
    posted: datetime
