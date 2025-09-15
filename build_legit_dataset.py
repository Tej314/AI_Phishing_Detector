import os

BASE_PATH = "/home/tej-vora/phishing_detector/maildir"

all_employees_emails = []

# Loop through some employees ([:3] for testing, remove later)
employees = os.listdir(BASE_PATH)
print("First 10 employees:", employees[:10])

for employee in employees[:3]:
    employee_path = os.path.join(BASE_PATH, employee)
    if not os.path.isdir(employee_path):
        continue

    print(f"\nEmployee: {employee}")
    folders = os.listdir(employee_path)
    print(f"Folders for {employee}: {folders}")

    for folder in folders:
        folder_path = os.path.join(employee_path, folder)
        if not os.path.isdir(folder_path):
            continue

        emails = []
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                with open(file_path, "r", encoding="latin-1") as f:
                    content = f.read()

                # --- PARSING ---
                parts = content.split("\n\n", 1)
                headers = parts[0]
                body = parts[1] if len(parts) > 1 else ""

                subject = ""
                for line in headers.split("\n"):
                    if line.lower().startswith("subject:"):
                        subject = line[len("subject:"):].strip()
                        break

                combined_text = subject + "\n" + body
                emails.append(combined_text)
                all_employees_emails.append(combined_text)

            except Exception as e:
                print(f"Error reading {file_path}: {e}")

        print(f"Collected {len(emails)} parsed emails from {folder_path}")
        if emails:
            print("Sample parsed preview:\n", emails[0][:300], "\n---")

print(f"\n Total parsed across employees: {len(all_employees_emails)}")
if all_employees_emails:
    print("First global parsed preview:\n", all_employees_emails[0][:500])

import csv

csv_path = "/home/tej-vora/phishing_detector/legit_dataset.csv"

with open(csv_path, mode="w", newline="", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)

    writer.writerow(["email_text"])
    for email_text in all_employees_emails:
        writer.writerow([email_text])

print(f"\n Saved {len(all_employees_emails)} emails to {csv_path}")
