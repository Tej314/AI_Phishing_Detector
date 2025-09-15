# combine_dataset.py

import pandas as pd

# Load datasets
phish = pd.read_csv("phish_database.csv")
legit = pd.read_csv("legit_dataset.csv")

# Normalize legit dataset to have subject/body
legit = legit.rename(columns={"email_text": "body"})
legit["subject"] = None
legit["label"] = "legit"

# Add phishing label
phish["label"] = "phish"

# Combine
combined = pd.concat([legit[["subject", "body", "label"]],
                      phish[["subject", "body", "label"]]],
                     ignore_index=True)

# --- NEW STEP: drop duplicates ---
before = len(combined)
combined = combined.drop_duplicates()
after = len(combined)
print(f"Removed {before - after} duplicate rows")

# Save
combined.to_csv("combined_dataset.csv", index=False)
print("Combined dataset saved as combined_dataset.csv")
