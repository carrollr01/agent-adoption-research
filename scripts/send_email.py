#!/usr/bin/env python3
"""Send an email via Gmail SMTP using an App Password.

Reads credentials from env vars GMAIL_APP_PASSWORD and GMAIL_SEND_FROM.

Two input modes:
  --email-file PATH   First non-blank line is the subject, remainder is the body.
  --subject / --body-file   Pass them separately.

Usage:
  scripts/send_email.py --to a@x --to b@y --email-file log/2026-04-17.email.txt
"""
import argparse
import os
import smtplib
import sys
from email.message import EmailMessage


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--to", action="append", required=True)
    parser.add_argument("--subject")
    parser.add_argument("--body-file")
    parser.add_argument("--email-file", help="First line = subject, rest = body")
    args = parser.parse_args()

    password = os.environ.get("GMAIL_APP_PASSWORD")
    sender = os.environ.get("GMAIL_SEND_FROM")
    if not password or not sender:
        print("Missing GMAIL_APP_PASSWORD or GMAIL_SEND_FROM in env.", file=sys.stderr)
        return 2

    if args.email_file:
        with open(args.email_file, encoding="utf-8") as f:
            raw = f.read().lstrip("\n")
        subject, _, body = raw.partition("\n")
        subject = subject.strip()
        body = body.lstrip("\n")
    elif args.subject and args.body_file:
        subject = args.subject
        with open(args.body_file, encoding="utf-8") as f:
            body = f.read()
    else:
        print("Provide --email-file OR both --subject and --body-file.", file=sys.stderr)
        return 2

    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = ", ".join(args.to)
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.login(sender, password.replace(" ", ""))
        smtp.send_message(msg)

    print(f"sent to {', '.join(args.to)} from {sender}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
