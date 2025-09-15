import pandas as pd
import random
import re

def generate_variants(url):
    """
    Create tricky variants of phishing URLs:
    - Misspellings
    - Fake TLDs
    - Random capitalization
    """
    variants = []

    # Common misspellings (replace "login" → "logln" etc.)
    misspellings = {
        "login": ["logln", "log1n"],
        "secure": ["secvre", "secur3"],
        "account": ["acc0unt", "acc0uht"],
        "verify": ["ver1fy", "verlfy"]
    }

    # Apply misspellings
    for word, wrongs in misspellings.items():
        if word in url:
            for wrong in wrongs:
                variants.append(url.replace(word, wrong))

    # Fake TLD swap (.com → .co, .net → .org, etc.)
    tlds = [".com", ".net", ".org", ".co", ".xyz", ".top"]
    for tld in tlds:
        if url.endswith(tld):
            variants.append(url.replace(tld, random.choice(tlds)))

    # Random capitalization
    if "http" in url:
        rand_caps = "".join(c.upper() if random.random() > 0.5 else c for c in url)
        variants.append(rand_caps)

    return variants


def expand_dataset(input_csv="phish_database.csv", output_csv="phish_database_expanded.csv"):
    df = pd.read_csv(input_csv)

    expanded_data = []
    for url in df["url"]:
        expanded_data.append(url)
        expanded_data.extend(generate_variants(url))

    expanded_df = pd.DataFrame({"url": expanded_data, "label": "phish"})
    expanded_df.to_csv(output_csv, index=False)
    print(f"Expanded phishing dataset saved as {output_csv}")


if __name__ == "__main__":
    expand_dataset()
