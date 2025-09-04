#!/usr/bin/env python3
import requests
import logging
import sys
from datetime import datetime

GET_URL = "https://httpbin.org/get"
POST_URL = "https://httpbin.org/post"
POST_PAYLOAD = {"name": "Pranshu", "course": "Computer Networks Lab"}
TIMEOUT = 10

logging.basicConfig(filename="http_client.log", level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

def pretty_print_response(resp):
    print()
    print("URL:", resp.url)
    print("Status:", resp.status_code)
    print("Headers:")
    for k, v in resp.headers.items():
        print(f"  {k}: {v}")
    print("\nBody (truncated to 1000 chars):")
    text = resp.text or ""
    print(text[:1000] + ("..." if len(text) > 1000 else ""))

def run():
    print("→ Starting HTTP client. Making a friendly GET then POST to httpbin.org.")
    try:
        r = requests.get(GET_URL, timeout=TIMEOUT)
        logging.info("GET %s -> %s", GET_URL, r.status_code)
        pretty_print_response(r)
    except Exception as e:
        logging.exception("GET failed")
        print("GET failed:", e, file=sys.stderr)

    try:
        print("\n→ Now sending a POST with a small JSON payload.")
        r = requests.post(POST_URL, json=POST_PAYLOAD, timeout=TIMEOUT)
        logging.info("POST %s -> %s", POST_URL, r.status_code)
        pretty_print_response(r)
    except Exception as e:
        logging.exception("POST failed")
        print("POST failed:", e, file=sys.stderr)

if __name__ == "__main__":
    run()
