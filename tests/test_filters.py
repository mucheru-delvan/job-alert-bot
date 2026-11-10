from datetime import datetime

from filters import filter_jobs, matches
from models import Job


def make_job(title):
    return Job(
        source="test",
        job_id="1",
        title=title,
        url="https://example.com/job",
        posted=datetime(2026, 11, 10),
    )


def test_matches_keyword_case_insensitive():
    assert matches(make_job("Senior PYTHON Developer"))


def test_no_match_returns_false():
    assert not matches(make_job("Waiter at CJ's"))


def test_whole_word_only():
    assert not matches(make_job("International Sales Lead"), keywords=["intern"])


def test_hyphenated_keyword():
    assert matches(make_job("Back-end Engineer"))


def test_filter_jobs_keeps_only_matches():
    jobs = [make_job("Python Developer"), make_job("Waiter"), make_job("DevOps Engineer")]
    result = filter_jobs(jobs)
    assert [j.title for j in result] == ["Python Developer", "DevOps Engineer"]

def test_excluded_word_blocks_match():
    assert not matches(make_job("Data Collectors at Jhpiego"))


def test_exclude_can_be_overridden():
    assert matches(make_job("Data Collectors"), exclude=[])


def test_exclude_is_whole_word_too():
    assert matches(make_job("Software Engineer, Salesforce"), exclude=["sales"])