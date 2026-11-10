from fetchers.openedcareer import fetch_jobs
from filters import filter_jobs

jobs = fetch_jobs(30)
matched = filter_jobs(jobs)

print(f"{len(matched)} of {len(jobs)} jobs matched")
for job in matched:
    print(job.posted, job.title, job.url, sep=" | ")