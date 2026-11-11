from fetchers.openedcareer import fetch_jobs
from filters import filter_jobs
from notifier import build_digest, send_email
from seen import job_key, load_seen, new_jobs, save_seen

seen = load_seen()
jobs = fetch_jobs(100)
matched = filter_jobs(jobs)
fresh = new_jobs(matched, seen)

print(f"{len(fresh)} new jobs ({len(matched)} matched of {len(jobs)} fetched)")

if fresh:
    subject, body = build_digest(fresh)
    send_email(subject, body)
    seen.update(job_key(job) for job in fresh)
    save_seen(seen)