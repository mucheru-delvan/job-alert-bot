import re

KEYWORDS = [
    "backend", "back-end", "python", "django", "software",
    "developer", "engineer", "it support", "devops", "data",
    "cloud", "api", "ict", "technical support",
]



def matches(job, keywords=KEYWORDS):
    title = job.title.lower()
    for keyword in keywords:
        pattern = r"\b" + re.escape(keyword) + r"\b"
        if re.search(pattern, title):
            return True
    return False


def filter_jobs(jobs, keywords=KEYWORDS):
    return [job for job in jobs if matches(job, keywords)]