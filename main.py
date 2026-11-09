from fetchers.openedcareer import fetch_jobs

#This is  a throw away test for the project
for job in fetch_jobs(5):
    print(job.posted, job.title, job.url, sep=" | ")
