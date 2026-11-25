from datetime import datetime

from fetchers.techhut import parse_jobs

NOW = datetime(2026, 11, 21, 12, 0)

SAMPLE = {
    "id": "sf-capitec-1450871433",
    "title": "Data Analyst II ",
    "company": "Capitec",
    "location": "Stellenbosch, South Africa",
    "url": "https://careers.capitecbank.co.za/job/Stellenbosch-Data-Analyst-II/1450871433/",
    "date": "2026-11-21",
    "region": "Rest of Africa",
}


def test_parse_keeps_matching_region():
    job = parse_jobs([SAMPLE], keep_regions={"Rest of Africa"}, now=NOW)[0]
    assert job.source == "techhut"
    assert job.job_id == "sf-capitec-1450871433"
    assert job.title == "Data Analyst II"
    assert job.company == "Capitec"
    assert job.posted.day == 21


def test_parse_drops_other_regions():
    assert parse_jobs([SAMPLE], keep_regions={"Kenya"}, now=NOW) == []


def test_parse_drops_old_jobs():
    old = {**SAMPLE, "date": "2024-03-18T07:08:27.744Z"}
    assert parse_jobs([old], keep_regions={"Rest of Africa"}, now=NOW) == []


def test_parse_drops_jobs_without_date():
    undated = {k: v for k, v in SAMPLE.items() if k != "date"}
    assert parse_jobs([undated], keep_regions={"Rest of Africa"}, now=NOW) == []


def test_parse_converts_timezone_offsets_to_utc():
    item = {**SAMPLE, "date": "2026-11-17T00:14:13-05:00"}
    job = parse_jobs([item], keep_regions={"Rest of Africa"}, now=NOW)[0]
    assert job.posted == datetime(2026, 11, 17, 5, 14, 13)


def test_parse_skips_records_missing_required_fields():
    broken = {k: v for k, v in SAMPLE.items() if k != "url"}
    assert parse_jobs([broken], keep_regions={"Rest of Africa"}, now=NOW) == []