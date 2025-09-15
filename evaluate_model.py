# evaluate_model.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix,
    roc_curve, auc, precision_recall_curve
)
import joblib

# --- Step 1: Load model + vectorizer ---
model = joblib.load("phish_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

# --- Step 2: Load dataset ---
df = pd.read_csv("combined_dataset.csv")
df["text"] = (df["subject"].fillna("") + " " + df["body"].fillna(""))

X = vectorizer.transform(df["text"])
y = df["label"]

# --- Step 3: Stratified k-fold CV predictions ---
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
y_pred = cross_val_predict(model, X, y, cv=skf)
y_proba = cross_val_predict(model, X, y, cv=skf, method="predict_proba")[:, 1]  # prob for "phish"

# --- Step 4: Print metrics ---
print("=== Cross-Validation Results (5-fold) ===")
print("Accuracy: ", accuracy_score(y, y_pred))
print("Precision:", precision_score(y, y_pred, pos_label="phish"))
print("Recall:   ", recall_score(y, y_pred, pos_label="phish"))
print("F1 Score: ", f1_score(y, y_pred, pos_label="phish"))

print("\nClassification Report:")
print(classification_report(y, y_pred))

print("Confusion Matrix:")
cm = confusion_matrix(y, y_pred, labels=["legit", "phish"])
print(cm)

# --- Confusion Matrix Heatmap ---
plt.figure(figsize=(6, 4))
sns.heatmap(
    cm, annot=True, fmt="d", cmap="Blues",
    xticklabels=["legit", "phish"],
    yticklabels=["legit", "phish"]
)
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix Heatmap")
plt.tight_layout()
plt.savefig("confusion_matrix.png")
plt.close()
print("Confusion matrix heatmap saved as 'confusion_matrix.png'")


# --- Step 5: ROC Curve ---
fpr, tpr, _ = roc_curve(y.map({"legit": 0, "phish": 1}), y_proba)
roc_auc = auc(fpr, tpr)

plt.figure()
plt.plot(fpr, tpr, label=f"ROC curve (AUC = {roc_auc:.2f})")
plt.plot([0, 1], [0, 1], "k--")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve")
plt.legend(loc="lower right")
plt.savefig("roc_curve.png")
plt.close()

# --- Step 6: Precision-Recall Curve ---
prec, rec, _ = precision_recall_curve(y.map({"legit": 0, "phish": 1}), y_proba)
plt.figure()
plt.plot(rec, prec, label="Precision-Recall curve")
plt.xlabel("Recall")
plt.ylabel("Precision")
plt.title("Precision-Recall Curve")
plt.legend(loc="lower left")
plt.savefig("pr_curve.png")
plt.close()

print("\nROC and PR curves saved as 'roc_curve.png' and 'pr_curve.png'")
