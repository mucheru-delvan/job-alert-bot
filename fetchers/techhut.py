from datetime import UTC, datetime, timedelta

import requests

from models import Job

DATA_URL = "https://thetechhut.co/data/jobs-board.json"
KEEP_REGIONS = {"Kenya", "Remote"}
MAX_AGE_DAYS = 45
HEADERS = {
    "User-Agent": "job-alert-bot (personal project; github.com/mucheru-delvan/job-alert-bot)"
}


def parse_date(value):
    if not value:
        return None
    posted = datetime.fromisoformat(value)
    if posted.tzinfo is not None:
        posted = posted.astimezone(UTC).replace(tzinfo=None)
    return posted


def parse_jobs(items, keep_regions=KEEP_REGIONS, max_age_days=MAX_AGE_DAYS, now=None):
    
    now = now or datetime.now(UTC).replace(tzinfo=None)
    cutoff = now - timedelta(days=max_age_days)
    jobs = []
    for item in items:
        if not (item.get("id") and item.get("title") and item.get("url")):
            continue
        posted = parse_date(item.get("date"))
        if posted is None or posted < cutoff:
            continue
        jobs.append(
            Job(
                source="techhut",
                job_id=str(item["id"]),
                title=item["title"].strip(),
                url=item["url"],
                posted=posted,
                company=item.get("company", ""),
                location=item.get("location", ""),
            )
        )
    return jobs


def fetch_jobs():
    response = requests.get(DATA_URL, headers=HEADERS, timeout=30)
    response.raise_for_status()
    return parse_jobs(response.json()["jobs"])