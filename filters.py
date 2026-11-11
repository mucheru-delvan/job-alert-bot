import re

KEYWORDS = [
    "backend", "back-end", "python", "django", "software",
    "developer", "engineer", "it support", "devops", "data",
    "cloud", "api", "ict", "technical support",
]

EXCLUDE = [
    "collector", "collectors", "supplier", "protection",
    "sales", "civil", "mechanical",
]


def contains_word(text, words):
    for word in words:
        pattern = r"\b" + re.escape(word) + r"\b"
        if re.search(pattern, text):
            return True
    return False


def matches(job, keywords=KEYWORDS, exclude=EXCLUDE):
    title = job.title.lower()
    return contains_word(title, keywords) and not contains_word(title, exclude)


def filter_jobs(jobs, keywords=KEYWORDS, exclude=EXCLUDE):
    return [job for job in jobs if matches(job, keywords, exclude)]