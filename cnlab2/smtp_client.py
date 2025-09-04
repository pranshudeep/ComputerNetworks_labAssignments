#!/usr/bin/env python3
import smtplib
import logging
from email.message import EmailMessage
import getpass

logging.basicConfig(filename="smtp_client.log", level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

host_input = input("SMTP host (press Enter for smtp.gmail.com): ").strip()
SMTP_HOST = host_input or "smtp.gmail.com"
port_input = input("SMTP port (press Enter for 587): ").strip()
SMTP_PORT = int(port_input or "587")
SMTP_USER = input("SMTP username (your email): ").strip()
SMTP_PASS = getpass.getpass("SMTP password (will not be echoed): ")
FROM = SMTP_USER
to_input = input("Recipient email (comma-separated if many): ").strip()
TO = [x.strip() for x in to_input.split(",") if x.strip()] or [SMTP_USER]
SUBJECT = input("Subject (press Enter for default): ").strip() or "CN Lab Assignment 2 - test email"
BODY = input("Body (press Enter to use a friendly default): ").strip() or ("Hi there!\n\nThis is a test message sent by smtp_client.py to verify SMTP functionality.\n\nCheers,\nYour friendly script")

def send_mail():
    msg = EmailMessage()
    msg["From"] = FROM
    msg["To"] = ", ".join(TO)
    msg["Subject"] = SUBJECT
    msg.set_content(BODY)

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=30) as smtp:
            smtp.ehlo()
            if SMTP_PORT == 587:
                smtp.starttls()
                smtp.ehlo()
            smtp.login(SMTP_USER, SMTP_PASS)
            smtp.send_message(msg)
            logging.info("Email sent to %s via %s:%s", TO, SMTP_HOST, SMTP_PORT)
            print("Email sent successfully to", ", ".join(TO))
    except Exception as e:
        logging.exception("Failed to send email")
        print("Failed to send email:", e)

if __name__ == "__main__":
    print("SMTP client ready.")
    if not SMTP_USER or not SMTP_PASS:
        print("Username or password missing; please restart and provide credentials.")
    else:
        send_mail()
