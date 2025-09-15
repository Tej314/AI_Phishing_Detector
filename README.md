# AI Phishing Detector  

🚀 **Overview**  
This project demonstrates how artificial intelligence can be applied to cybersecurity by detecting phishing emails. Using machine learning and NLP, the system classifies emails as **phishing** or **legitimate** with high accuracy.  

---

## Features  
✅ Data ingestion from phishing feeds (OpenPhish) and legitimate sources  
✅ Preprocessing pipeline (tokenization, vectorization, feature engineering)  
✅ Machine learning model training (scikit-learn, Logistic Regression/Random Forest/etc.)  
✅ Model persistence (`.pkl` files) for reuse in applications  
✅ Evaluation scripts to measure accuracy, precision, recall, and F1-score  

---

## Tech Stack  
- Python  
- scikit-learn  
- pandas, numpy  
- matplotlib (for evaluation/visualization)  

---

## How It Works  
1. **Data Collection**: Scripts pull phishing and legit email samples.  
2. **Preprocessing**: Data cleaned, vectorized, and combined into a dataset.  
3. **Training**: ML model trained and saved (`phish_model.pkl`).  
4. **Evaluation**: Accuracy and confusion matrix results generated with `evaluate_model.py`.  
5. **Deployment Ready**: Model can be integrated into an email filter or SOC workflow.  

---

## Example Usage  
```bash
# Train a new model
python train_model.py

# Evaluate performance
python evaluate_model.py
