from datetime import datetime

from models import Job
from notifier import build_digest


def make_job(title, job_id="1"):
    return Job(
        source="test",
        job_id=job_id,
        title=title,
        url=f"https://example.com/{job_id}",
        posted=datetime(2026, 11, 10, 18, 30),
    )


def test_subject_contains_job_count():
    jobs = [make_job("A", "1"), make_job("B", "2")]
    subject, _ = build_digest(jobs)
    assert "2" in subject


def test_body_contains_title_url_and_date():
    subject, body = build_digest([make_job("Python Developer")])
    assert "Python Developer" in body
    assert "https://example.com/1" in body
    assert "Posted: 10 Nov 2026" in body


def test_body_keeps_job_order():
    jobs = [make_job("First", "1"), make_job("Second", "2")]
    _, body = build_digest(jobs)
    assert body.index("First") < body.index("Second")