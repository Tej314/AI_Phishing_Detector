# preprocess.py

import pandas as pd
import re
import tldextract
from bs4 import BeautifulSoup
import email
from email import policy
from pathlib import Path


# --- URL Feature Extractor ---
def extract_url_features(url):
    url = url.strip().lower()

    features = {
        "url": url,
        "url_length": len(url),
        "num_dots": url.count("."),
        "has_ip": bool(re.match(r"http[s]?://\d+\.\d+\.\d+\.\d+", url)),
        "tld": tldextract.extract(url).suffix,
        "num_subdomains": len(tldextract.extract(url).subdomain.split(".")),
    }
    return features


# --- Email Preprocessing ---
def clean_email_body(body):
    if pd.isna(body):
        return ""
    # Remove HTML
    body = BeautifulSoup(body, "html.parser").get_text()
    # Lowercase + strip
    body = body.lower().strip()
    # Remove long whitespace
    body = re.sub(r"\s+", " ", body)
    return body


def extract_email_features(raw_email):
    """
    Accepts raw email text, extracts headers + body features
    """
    try:
        msg = email.message_from_string(raw_email, policy=policy.default)
        subject = msg["subject"] or ""
        from_addr = msg["from"] or ""
        reply_to = msg["reply-to"] or ""

        # Body extraction
        if msg.is_multipart():
            body = ""
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body += part.get_content()
        else:
            body = msg.get_content()

        body = clean_email_body(body)

        features = {
            "subject": subject.lower(),
            "from_domain": from_addr.split("@")[-1] if "@" in from_addr else from_addr,
            "reply_mismatch": int(reply_to and reply_to.split("@")[-1] != from_addr.split("@")[-1]),
            "body_length": len(body),
            "num_links": len(re.findall(r"http[s]?://\S+", body)),
            "keywords_flag": int(any(word in body for word in ["verify", "account", "urgent", "login"])),
            "body_clean": body
        }
        return features

    except Exception as e:
        return {
            "subject": "",
            "from_domain": "",
            "reply_mismatch": 0,
            "body_length": 0,
            "num_links": 0,
            "keywords_flag": 0,
            "body_clean": ""
        }


# --- Pipeline ---
def process_urls(input_file="phish_database.csv", output_file="phish_urls_features.csv"):
    df = pd.read_csv(input_file)
    feature_rows = [extract_url_features(u) for u in df["url"]]
    features_df = pd.DataFrame(feature_rows)
    features_df["label"] = "phish"
    features_df.to_csv(output_file, index=False)
    print(f"Saved URL features → {output_file}")


def process_emails(input_file="legit_dataset.csv", output_file="legit_emails_features.csv"):
    df = pd.read_csv(input_file)

    feature_rows = []
    for text in df["body"]:   # adjust column name if needed
        feature_rows.append(extract_email_features(text))

    features_df = pd.DataFrame(feature_rows)
    features_df["label"] = "legit"
    features_df.to_csv(output_file, index=False)
    print(f"Saved Email features → {output_file}")


if __name__ == "__main__":
    process_urls()
    process_emails()
