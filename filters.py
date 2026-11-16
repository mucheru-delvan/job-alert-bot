import re

KEYWORDS = [
    "backend", "back-end", "python", "django", "software",
    "developer", "engineer", "it support", "devops", "data",
    "cloud", "api", "ict", "technical support",
]

PROGRAMS = [
    "intern", "interns", "internship", "internships",
    "attachment", "trainee", "trainees",
    "graduate", "graduates", "apprenticeship",
]

EXCLUDE = [
    "collector", "collectors", "supplier", "protection",
    "sales", "civil", "mechanical",
]

LOCATIONS = ["kenya", "nairobi", "africa", "remote"]


def contains_word(text, words):
    for word in words:
        pattern = r"\b" + re.escape(word) + r"\b"
        if re.search(pattern, text):
            return True
    return False


def location_ok(job, locations=LOCATIONS):
    if not job.location:
        return True
    return contains_word(job.location.lower(), locations)


def matches(job, keywords=KEYWORDS, exclude=EXCLUDE, locations=LOCATIONS, programs=PROGRAMS):
    title = job.title.lower()
    wanted = contains_word(title, keywords) or contains_word(title, programs)
    return (
        wanted
        and not contains_word(title, exclude)
        and location_ok(job, locations)
    )


def filter_jobs(jobs, keywords=KEYWORDS, exclude=EXCLUDE, locations=LOCATIONS, programs=PROGRAMS):
    return [job for job in jobs if matches(job, keywords, exclude, locations, programs)]