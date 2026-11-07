import html
from datetime import datetime

import requests

from models import Job

API_URL = "https://openedcareer.com/wp-json/wp/v2/job_listing"


def parse_jobs(items):
    jobs = []
    for item in items:
        jobs.append(
            Job(
                source="openedcareer",
                job_id=str(item["id"]),
                title=html.unescape(item["title"]["rendered"]),
                url=item["link"],
                posted=datetime.fromisoformat(item["date"]),
            )
        )
    return jobs


def fetch_jobs(limit=30):
    params = {
        "per_page": limit,
        "orderby": "date",
        "order": "desc",
        "_fields": "id,date,title,link",
    }
    response = requests.get(API_URL, params=params, timeout=15)
    response.raise_for_status()
    return parse_jobs(response.json())
