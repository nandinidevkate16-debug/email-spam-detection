# ============================================================
# SPAM EMAIL/SMS DETECTION — ENHANCED FULL PIPELINE
# ============================================================

import re
import string
import pandas as pd
import numpy as np
import joblib
import nltk
from nltk.stem import WordNetLemmatizer

# ---- Step 0: Ensure NLTK Resources are Downloaded ----
for resource in ['wordnet', 'omw-1.4', 'punkt']:
    try:
        nltk.download(resource, quiet=True)
    except Exception:
        pass

lemmatizer = WordNetLemmatizer()

# ---- Step 1 & 2: Collect + Load Dataset ----
import os
tsv_path = "sms.tsv" if os.path.exists("sms.tsv") else "https://raw.githubusercontent.com/justmarkham/pycon-2016-tutorial/master/data/sms.tsv"
df = pd.read_csv(tsv_path, sep='\t', header=None, names=['label', 'message'])

print("Shape:", df.shape)
print(df.head())

# ---- Step 3: EDA ----
print("\nClass counts:\n", df['label'].value_counts())
print("\nMissing values:\n", df.isnull().sum())
print("\nDuplicates:", df.duplicated().sum())
df = df.drop_duplicates()

# ---- Step 4: Enhanced Preprocessing with Lemmatization ----
def clean_text(text):
    text = text.lower()
    text = re.sub(f"[{re.escape(string.punctuation)}]", "", text)
    tokens = text.split()
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in tokens]
    cleaned = " ".join(lemmatized_tokens)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned

print("\nPreprocessing messages with NLTK Lemmatization...")
df['clean_message'] = df['message'].apply(clean_text)

# Encode labels: spam=1, ham=0
df['label_num'] = df['label'].map({'ham': 0, 'spam': 1})

# ---- Step 5 & 6: Train/Test Split & Feature Extraction (Prevents Data Leakage) ----
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

X = df['clean_message']
y = df['label_num']

X_train_raw, X_test_raw, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Fit vectorizer only on train data
vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
X_train = vectorizer.fit_transform(X_train_raw)
X_test = vectorizer.transform(X_test_raw)

print(f"\nTrain size: {X_train.shape[0]} | Test size: {X_test.shape[0]}")

# ---- Step 7 & 8: Multi-Model Training & Evaluation ----
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                              f1_score, confusion_matrix, classification_report)

models = {
    "Multinomial Naive Bayes": MultinomialNB(),
    "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
    "Linear Support Vector (SVM)": LinearSVC(random_state=42)
}

results = []
best_model_name = None
best_f1 = -1
best_model = None

print("\n" + "="*60)
print(f"{'MODEL COMPARISON':^60}")
print("="*60)

for name, model_obj in models.items():
    model_obj.fit(X_train, y_train)
    y_pred = model_obj.predict(X_test)
    
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    
    results.append({
        "Model": name,
        "Accuracy": acc,
        "Precision": prec,
        "Recall": rec,
        "F1-Score": f1
    })
    
    if f1 > best_f1:
        best_f1 = f1
        best_model_name = name
        best_model = model_obj

results_df = pd.DataFrame(results)
print(results_df.to_string(index=False))
print("="*60)
print(f"\n[BEST MODEL SELECTED]: {best_model_name} (F1-Score: {best_f1:.4f})")

# Full Evaluation Report for Best Model
best_y_pred = best_model.predict(X_test)
print(f"\n--- DETAILED REPORT ({best_model_name.upper()}) ---")
print("Confusion Matrix:\n", confusion_matrix(y_test, best_y_pred))
print("\nClassification Report:\n", classification_report(y_test, best_y_pred, target_names=['ham', 'spam']))

# ---- Step 9: Predict New Messages ----
def predict_message(msg, model_to_use=best_model):
    cleaned = clean_text(msg)
    vec = vectorizer.transform([cleaned])
    pred = model_to_use.predict(vec)[0]
    
    confidence = None
    if hasattr(model_to_use, "predict_proba"):
        probs = model_to_use.predict_proba(vec)[0]
        confidence = probs[pred]
    elif hasattr(model_to_use, "decision_function"):
        score = model_to_use.decision_function(vec)[0]
        confidence = 1 / (1 + np.exp(-abs(score)))
        
    label = "SPAM" if pred == 1 else "HAM (Not Spam)"
    return label, confidence

sample_messages = [
    "Congratulations! You've WON a free iPhone, click here to claim now!!!",
    "Hey, are we still meeting for lunch tomorrow?",
    "URGENT! Your mobile number has won a £2000 prize. Call 09061701461 to claim.",
    "Can you send me the report when you get a chance?"
]

print("\n--- PREDICTIONS ON NEW MESSAGES ---")
for m in sample_messages:
    lbl, conf = predict_message(m)
    conf_str = f" (Confidence: {conf*100:.1f}%)" if conf else ""
    print(f"'{m}'\n  -> Result: {lbl}{conf_str}\n")

# ---- Step 10: Save Best Model & Vectorizer ----
joblib.dump(best_model, 'spam_model.pkl')
joblib.dump(vectorizer, 'tfidf_vectorizer.pkl')
print(f"Saved {best_model_name} as 'spam_model.pkl' and vectorizer as 'tfidf_vectorizer.pkl'.")