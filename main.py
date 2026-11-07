from fetchers.openedcareer import fetch_jobs

for job in fetch_jobs(5):
    print(job.posted, job.title, job.url, sep=" | ")
