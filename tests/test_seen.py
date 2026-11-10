from datetime import datetime

from models import Job
from seen import job_key, load_seen, new_jobs, save_seen


def make_job(job_id, source="test"):
    return Job(
        source=source,
        job_id=job_id,
        title="Some Job",
        url="https://example.com/job",
        posted=datetime(2026, 11, 10),
    )


def test_job_key_includes_source():
    assert job_key(make_job("5", source="a")) == "a:5"


def test_load_seen_missing_file_returns_empty_set(tmp_path):
    assert load_seen(tmp_path / "seen.json") == set()


def test_save_then_load_round_trip(tmp_path):
    path = tmp_path / "seen.json"
    save_seen({"a:1", "a:2"}, path)
    assert load_seen(path) == {"a:1", "a:2"}


def test_new_jobs_skips_seen():
    jobs = [make_job("1"), make_job("2")]
    result = new_jobs(jobs, {"test:1"})
    assert [j.job_id for j in result] == ["2"]


def test_same_id_different_source_is_new():
    jobs = [make_job("1", source="b")]
    assert new_jobs(jobs, {"a:1"}) == jobs