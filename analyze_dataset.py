# analyze_dataset.py
import pandas as pd

# --- Step 1: Load dataset ---
df = pd.read_csv("combined_dataset.csv")

print(f"Total rows: {len(df)}")
print(f"Columns: {df.columns.tolist()}")

# --- Step 2: Check balance of phishing vs legit ---
if 'label' in df.columns:
    print("\nLabel distribution:")
    print(df['label'].value_counts())

# --- Step 3: Uniqueness check ---
unique_rows = df.drop_duplicates().shape[0]
print(f"\nUnique rows: {unique_rows}")

# --- Step 4: Analyze phishing templates ---
if 'subject' in df.columns:
    template_counts = df['subject'].value_counts().reset_index()
    template_counts.columns = ['subject', 'count']
    print("\nMost common subjects:")
    print(template_counts.head(10))
