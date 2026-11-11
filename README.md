# Job Alert Bot

[![Job alerts](https://github.com/mucheru-delvan/job-alert-bot/actions/workflows/job-alerts.yml/badge.svg)](https://github.com/mucheru-delvan/job-alert-bot/actions/workflows/job-alerts.yml)

A Python bot that checks Kenyan job listings every morning and emails me only the new tech roles. I built it to stop scrolling job boards by hand during my final year at university.

![Example digest email](docs/digest.png)

## How it works

1. **Fetch:** pulls the 100 newest listings from Opened Career's public WordPress REST API.
2. **Filter:** keeps jobs whose title contains a wanted word (python, software, cloud, ict, and so on) and drops titles containing an excluded word (sales, civil, collector, and so on).
3. **Dedupe:** each job gets a key like `openedcareer:55998`, and keys already stored in `seen_jobs.json` are skipped.
4. **Notify:** sends one plain-text digest through Gmail's SMTP server, using an app password.
5. **Schedule:** a GitHub Actions workflow runs it daily at 08:00 Nairobi time, with no server to maintain.

## Design decisions

- **Parsing is separate from fetching.** `parse_jobs` takes plain data and returns `Job` objects, so tests can use fake data and never touch the network.
- **Keywords match whole words only.** A plain substring check would match "International" for "intern". A regex word boundary prevents that.
- **Jobs are marked as seen only after the email is sent.** If sending fails, nothing is saved, so the same jobs are retried on the next run instead of being lost.
- **The seen file is committed back to the repo.** Actions runs on a fresh machine every time, so the workflow commits `seen_jobs.json` after each run to remember what it already sent.
- **Keys include the source name.** When I add a second site, its job IDs can't clash with Opened Career's.
- **Secrets never touch the code.** The email address and app password come from environment variables locally and from GitHub secrets in the workflow.

## Run it locally

```
git clone https://github.com/mucheru-delvan/job-alert-bot.git
cd job-alert-bot
uv sync
```

Create a `.env` file:

```
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_APP_PASSWORD=your_16_character_app_password
```

Then run:

```
uv run --env-file .env python main.py
```

## Run the tests

```
uv run pytest
```

The tests cover the filter, the dedupe logic and the digest builder. None of them need internet.

## Run it on GitHub Actions

1. Fork or clone the repo to your own GitHub account.
2. Go to **Settings**, then **Secrets and variables**, then **Actions**.
3. Add two repository secrets: `EMAIL_ADDRESS` and `EMAIL_APP_PASSWORD` (a Gmail app password, which needs 2-Step Verification turned on).
4. The workflow runs daily at 05:00 UTC (08:00 in Nairobi). You can also start it manually from the **Actions** tab.

## Limitations and next steps

- Matching uses job titles only, so a good job with a vague title can be missed.
- There's one source so far. Next is a second site that has no feed and needs HTML scraping.
- The filter lists are edited in the code, not in a config file.

## License

MIT