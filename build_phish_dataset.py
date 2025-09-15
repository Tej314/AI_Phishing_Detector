#!/usr/bin/env python3
# build_phish_dataset.py
import csv
import requests
import os

OPENPHISH_URL = "https://openphish.com/feed.txt"
CSV_OUT = "phish_database.csv"
MAX_SAMPLES = 2000  # change to whatever you want

def fetch_openphish_urls():
    try:
        resp = requests.get(OPENPHISH_URL, timeout=10)
        resp.raise_for_status()
        urls = [line.strip() for line in resp.text.splitlines() if line.strip() and line.startswith("http")]
        print(f"🌐 Fetched {len(urls)} URLs from OpenPhish (online).")
        return urls
    except Exception as e:
        print(f"⚠️ Failed to fetch OpenPhish online: {e}")
        # fallback to local file if present
        if os.path.exists("phish_urls.txt"):
            with open("phish_urls.txt", "r", encoding="utf-8") as f:
                urls = [line.strip() for line in f if line.strip() and line.startswith("http")]
            print(f"📂 Loaded {len(urls)} URLs from phish_urls.txt (offline fallback).")
            return urls
        else:
            print("❌ No offline fallback file (phish_urls.txt) found. Exiting.")
            return []

def build_phish_csv(urls, out_csv=CSV_OUT, limit=MAX_SAMPLES):
    rows = []
    for url in urls[:limit]:
        subject = "Important: Verify Your Account"
        body = f"Dear user,\n\nYour account has been flagged for suspicious activity. Please verify immediately at {url}\n\nThank you."
        rows.append({"subject": subject, "body": body})

    if not rows:
        print("⚠️ No phishing samples to write.")
        return

    with open(out_csv, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["subject", "body"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"✅ Wrote {len(rows)} phishing samples to {out_csv}")

if __name__ == "__main__":
    urls = fetch_openphish_urls()
    if urls:
        build_phish_csv(urls)
