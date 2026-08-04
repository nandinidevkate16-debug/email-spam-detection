# 🛡️ AI Email & SMS Spam Detector

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.60-red.svg)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.9.0-orange.svg)
![Accuracy](https://img.shields.io/badge/Accuracy-97.7%25-brightgreen.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

An end-to-end Machine Learning web application that automatically classifies incoming Email and SMS text messages as **Spam** (unwanted / malicious / promotional) or **Ham** (legitimate). Built with **Python**, **Scikit-Learn**, **NLTK**, **TF-IDF Vectorization**, and an interactive modern dark-mode dashboard powered by **Streamlit**.

---

## 🌟 Key Features

- 🚀 **High Accuracy Machine Learning Engine:** Utilizes Linear Support Vector Classification (SVC) trained on TF-IDF features, achieving **~97.7% accuracy** and an **F1-Score of ~0.904**.
- 🔤 **NLTK Lemmatization & Preprocessing:** Advanced NLP pipeline featuring lowercase normalization, punctuation stripping, tokenization, and WordNet lemmatization.
- 🎨 **Modern Streamlit Dashboard:** Custom dark-themed user interface with real-time analysis, visual status cards, and model certainty progress bars.
- ⚡ **Preset Sample Selector:** Quick-test sample buttons for common message types (Free Promos, Bank Alerts, Work Documents, Lunch Meetings).
- ⚙️ **End-to-End Pipeline & Reproducibility:** Automated dataset downloader, full training pipeline script (`spam_detection.py`), and saved model artifacts (`spam_model.pkl`, `tfidf_vectorizer.pkl`).

---

## 📊 Dataset & Pipeline Overview

### 1. Dataset
- **Source:** SMS Spam Collection Dataset (`sms.tsv`)
- **Total Records:** 5,572 messages (86.6% Ham, 13.4% Spam)
- **Preprocessing:** De-duplication, punctuation removal, NLTK Lemmatization.

### 2. Feature Extraction & Modeling
- **Vectorization:** TF-IDF (Term Frequency - Inverse Document Frequency) with up to 5,000 max features and $1\text{--}2$ word n-gram ranges.
- **Model Evaluation:** Multiple algorithms were trained and benchmarked (Multinomial Naive Bayes, Linear SVC, Logistic Regression). Linear SVC yielded the highest overall performance metrics.

```
Raw Text Message 
      │
      ▼
┌───────────────────────────────┐
│  Text Preprocessing           │
│  • Lowercasing                │
│  • Punctuation Removal        │
│  • NLTK Lemmatization         │
└──────────────┬────────────────┘
               │
               ▼
┌───────────────────────────────┐
│  TF-IDF Vectorizer            │
│  (5,000 N-Gram Features)      │
└──────────────┬────────────────┘
               │
               ▼
┌───────────────────────────────┐
│  Linear SVC Classifier        │
│  (Trained Model Inference)    │
└──────────────┬────────────────┘
               │
               ▼
┌───────────────────────────────┐
│  Prediction & Certainty Score │
│  (Spam 🚨 vs Ham ✅)          │
└───────────────────────────────┘
```

---

## 📁 Project Structure

```text
Email_Spam_detection/
│
├── app.py                   # Streamlit Web Application interface
├── spam_detection.py        # ML pipeline script (EDA, Training, Evaluation, Model Saving)
├── download_data.py         # Helper script to download SMS Spam Collection dataset
├── requirements.txt         # Project Python dependencies
├── Instructions.md          # Workflow documentation
├── sms.tsv                  # Dataset file (5,572 labeled messages)
├── spam_model.pkl           # Trained Linear SVC Machine Learning model
└── tfidf_vectorizer.pkl     # Fitted TF-IDF Vectorizer
```

---

## 🛠️ Installation & Quickstart

### Prerequisites
- **Python 3.10+** installed on your system.

### 1. Clone or Open the Project Directory
```bash
cd Email_Spam_detection
```

### 2. Set Up a Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

> [!NOTE]
> `requirements.txt` specifies `nltk<3.10` to ensure optimal compatibility with virtual environment directory setups.

### 4. (Optional) Download Data & Train Model
The repository already includes pre-trained `spam_model.pkl` and `tfidf_vectorizer.pkl`. If you wish to re-train the model from scratch:

```bash
# Download dataset (if not present)
python download_data.py

# Train and save ML model artifacts
python spam_detection.py
```

### 5. Run the Streamlit Application

If running from an activated virtual environment:
```bash
streamlit run app.py
```

Or run directly using the virtual environment executable path:

**Windows (PowerShell / CMD):**
```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

**macOS / Linux:**
```bash
./.venv/bin/python -m streamlit run app.py
```

Open your browser and navigate to `http://localhost:8501`.

---

## 💡 Troubleshooting

<details>
<summary><b>1. <code>streamlit : The term 'streamlit' is not recognized</code></b></summary>

This error occurs when `streamlit` is installed inside `.venv` but the virtual environment is not activated in your current shell terminal.

**Solution:**
Use explicit path execution:
```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```
or activate your virtual environment before running:
```powershell
.\.venv\Scripts\Activate.ps1
streamlit run app.py
```
</details>

<details>
<summary><b>2. Missing Model Files Error</b></summary>

If the app displays *`Model files (spam_model.pkl, tfidf_vectorizer.pkl) not found!`*:
Run `python spam_detection.py` in your terminal to train and generate the `.pkl` files.
</details>

---

## 📜 License

This project is open-source under the [MIT License](LICENSE).
