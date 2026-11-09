from dataclasses import dataclass
from datetime import datetime

'''A dataclass is a shortcut for a class that just holds data.
Python writes the __init__ for you, so Job(source="x", job_id="1", ...) works with no boilerplate.'''
@dataclass(frozen=True)
class Job:
    source: str
    job_id: str
    title: str
    url: str
    posted: datetime
