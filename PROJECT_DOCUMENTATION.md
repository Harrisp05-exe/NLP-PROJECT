# SMS Spam Detection System (Hindi & English)
## Comprehensive Technical Documentation & Architecture Report

---

### Executive Summary

Short Message Service (SMS) spam poses ongoing security, privacy, and financial risks for mobile phone users. In multilingual markets such as India, spam and phishing messages frequently target users in regional languages like **Hindi** and **Hinglish**, advertising fraudulent lottery winnings, instant unverified loans, and phishing URLs.

This project implements an end-to-end **Natural Language Processing (NLP)** and **Machine Learning** system capable of classifying incoming SMS messages in both **Hindi** (Devanagari script) and **English** as either legitimate (**"ham"**) or unsolicited (**"spam"**).

The system includes:
1. **Multilingual data ingestion & preprocessing** supporting Devanagari Unicode (`\u0900-\u097F`) and ASCII text.
2. **TF-IDF Bi-gram feature extraction** (5,000 features).
3. **Four trained & serialized classifiers** (Linear SVM, Naive Bayes, Random Forest, Logistic Regression).
4. **Interactive Streamlit web application** with real-time model switching dropdown and quick-test samples.

---

### System Architecture & Pipeline Workflow

```
[ Hindi SMS Dataset ] (data/hindi_sms_spam_ham_15000.csv - 15,000 messages)
       │
       ▼
 [ clean.py ] ──► Regex filtering, Unicode normalization, Stopwords, Stemming
       │
       ▼
[ Cleaned Data ] (data/cleaned_spam.csv)
       │
       ▼
 [ train.py ] ──► Stratified Train/Test Split, Bi-gram TF-IDF (5,000 features),
       │          Trains 4 ML classifiers, saves all models & best model
       ▼
[ Saved Models ] (models/all_models.joblib, best_model.joblib, vectorizer.joblib, metrics.json)
       │
       ▼
  [ app.py ]  ──► Interactive Web App with Live Model Selector & Quick-Test Buttons
```

---

### Repository Structure

| File / Path | Type | Description |
| :--- | :--- | :--- |
| `data/hindi_sms_spam_ham_15000.csv` | Dataset | 15,000 labeled Hindi SMS records (50% ham, 50% spam). |
| `data/cleaned_spam.csv` | Dataset | Preprocessed dataset ready for ML training. |
| `clean.py` | Script | Multilingual data cleaning and preprocessing pipeline. |
| `train.py` | Script | Feature engineering, model benchmarking, and artifact serialization. |
| `app.py` | Application | Streamlit web UI with live model selector dropdown. |
| `models/all_models.joblib` | Model Artifact | Dictionary containing all 4 trained classifiers for live switching. |
| `models/best_model.joblib` | Model Artifact | Highest performing model. |
| `models/vectorizer.joblib` | Model Artifact | Fitted TF-IDF Bi-gram vectorizer. |
| `models/metrics.json` | Metrics Artifact | Performance metrics across all models. |
| `SMS_Spam_Detection_Project_Documentation.docx` | Document | Formatted Microsoft Word report. |
| `PROJECT_DOCUMENTATION.md` | Document | Comprehensive Markdown documentation. |

---

### Preprocessing & NLP Features (`clean.py`)

- **Devanagari Unicode Handling**: Text is ingested using `utf-8` encoding. The regular expression pattern `[^\u0900-\u097Fa-zA-Z\s]` retains Hindi characters, English alphabets, and whitespace while stripping punctuation, digits, and noise.
- **Bilingual Stopwords**: Combines NLTK's English stopword corpus with common Hindi functional stopwords (*है, हैं, के, की, का, में, से, को, पर, और, यह, वह, भी, तो, ही, था, थे, थी, रहा, रहे, रही, हूं*).
- **Selective Stemming**: Employs Porter Stemmer for English tokens while preserving Devanagari word morphology.

---

### Multi-Model Benchmarking & Live Model Selector

The training script trains four classical machine learning algorithms:
1. **Linear Support Vector Classifier (LinearSVC)**
2. **Multinomial Naive Bayes (`MultinomialNB`)**
3. **Random Forest Classifier (`RandomForestClassifier`)**
4. **Logistic Regression (`LogisticRegression`)**

The Streamlit web interface ([`app.py`](file:///c:/NLP%20PROJECT/app.py)) includes a **sidebar dropdown** that lets users switch between any of these models in real time during live testing or presentations.

---

### Running the Application

```bash
streamlit run app.py
```
*(Access at http://localhost:8501)*
