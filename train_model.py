import pandas as pd
import string
import re
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report
)
from imblearn.over_sampling import SMOTE

# Load dataset
df = pd.read_csv("combined_dataset.csv")

# Combine subject + body into one text column
df["text"] = df["subject"].fillna("") + " " + df["body"].fillna("")

# Preprocess text
def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+", "URL", text)  # replace links
    text = text.translate(str.maketrans("", "", string.punctuation))  # remove punctuation
    return text

df["clean_text"] = df["text"].apply(clean_text)

# Split data
X = df["clean_text"]
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Vectorize with TF-IDF
vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Apply SMOTE to balance the training data
smote = SMOTE(random_state=42)
X_train_balanced, y_train_balanced = smote.fit_resample(X_train_tfidf, y_train)

print("Before SMOTE:", dict(pd.Series(y_train).value_counts()))
print("After SMOTE:", dict(pd.Series(y_train_balanced).value_counts()))

# Train classifier
model = LogisticRegression(max_iter=1000)
model.fit(X_train_balanced, y_train_balanced)

# Predictions
y_pred = model.predict(X_test_tfidf)

# Evaluation
print("\n=== Model Evaluation ===")
print(f"Accuracy:  {accuracy_score(y_test, y_pred):.4f}")
print(f"Precision: {precision_score(y_test, y_pred, pos_label='phish'):.4f}")
print(f"Recall:    {recall_score(y_test, y_pred, pos_label='phish'):.4f}")
print(f"F1 Score:  {f1_score(y_test, y_pred, pos_label='phish'):.4f}")
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Save model + vectorizer
joblib.dump(model, "phish_model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")
print("Model and vectorizer saved.")
