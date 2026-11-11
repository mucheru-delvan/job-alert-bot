import os
import smtplib
from email.message import EmailMessage


def build_digest(jobs):
    subject = f"{len(jobs)} new job(s) for you"
    lines = []
    for job in jobs:
        lines.append(f"{job.title}\n{job.url}\nPosted: {job.posted:%d %b %Y}\n")
    body = "\n".join(lines)
    return subject, body


def send_email(subject, body):
    sender = os.environ["EMAIL_ADDRESS"]
    password = os.environ["EMAIL_APP_PASSWORD"]
    recipient = os.environ.get("EMAIL_TO", sender)

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = sender
    message["To"] = recipient
    message.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.send_message(message)