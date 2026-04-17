#!/usr/bin/env python3
"""Send an email via Gmail SMTP using an App Password.

Reads credentials from env vars GMAIL_APP_PASSWORD and GMAIL_SEND_FROM.
Body is read from --body-file (plain text). Subject and recipients via args.

Usage:
  scripts/send_email.py \
      --to rcarrol6@nd.edu --to klinhj24@wfu.edu \
      --subject "Agent Pattern Scan ..." \
      --body-file log/2026-04-17.md
"""
import argparse
import os
import smtplib
import sys
from email.message import EmailMessage


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--to", action="append", required=True)
    parser.add_argument("--subject", required=True)
    parser.add_argument("--body-file", required=True)
    args = parser.parse_args()

    password = os.environ.get("GMAIL_APP_PASSWORD")
    sender = os.environ.get("GMAIL_SEND_FROM")
    if not password or not sender:
        print("Missing GMAIL_APP_PASSWORD or GMAIL_SEND_FROM in env.", file=sys.stderr)
        return 2

    with open(args.body_file, encoding="utf-8") as f:
        body = f.read()

    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = ", ".join(args.to)
    msg["Subject"] = args.subject
    msg.set_content(body)

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.login(sender, password.replace(" ", ""))
        smtp.send_message(msg)

    print(f"sent to {', '.join(args.to)} from {sender}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
