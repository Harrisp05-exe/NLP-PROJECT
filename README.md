# SMS Spam Detector

A simple, end-to-end SMS spam detection project: clean data → train &
compare ML models → interactive Streamlit app for live predictions.

## Project structure

```
sms_spam_project/
├── data/
│   ├── spam.csv            # raw dataset (UCI SMS Spam Collection)
│   └── cleaned_spam.csv    # produced by clean.py
├── models/
│   ├── vectorizer.joblib   # fitted TF-IDF vectorizer (produced by train.py)
│   ├── best_model.joblib   # best-performing trained classifier
│   └── metrics.json        # metrics for all models compared
├── clean.py                 # Step 1: data cleaning / preprocessing
├── train.py                  # Step 2: feature extraction + model training/comparison
├── app.py                    # Step 3: Streamlit app for live predictions
├── requirements.txt
└── README.md
```

## Setup

```bash
pip install -r requirements.txt
python -c "import nltk; nltk.download('stopwords')"
```

## Usage

### 1. Clean the data
```bash
python clean.py
```
Reads `data/spam.csv`, removes duplicates/nulls, normalizes text
(lowercasing, stopword removal, stemming), and writes
`data/cleaned_spam.csv`.

### 2. Train & compare models
```bash
python train.py
```
Builds TF-IDF features, trains Naive Bayes, Logistic Regression, Linear
SVM, and Random Forest, evaluates each on a held-out test set, and saves
the best model (by F1-score on the spam class) plus the vectorizer to
`models/`.

Current results on this dataset:

| Model               | Accuracy | Precision | Recall | F1    |
|----------------------|----------|-----------|--------|-------|
| Naive Bayes          | 0.975    | 1.000     | 0.802  | 0.890 |
| Logistic Regression  | 0.963    | 0.990     | 0.718  | 0.832 |
| **Linear SVM (best)**| **0.988**| **0.976** | **0.931** | **0.953** |
| Random Forest        | 0.979    | 0.974     | 0.855  | 0.911 |

### 3. Run the app
```bash
streamlit run app.py
```
Opens a browser UI where you can type/paste an SMS and get an instant
Spam / Ham prediction with a confidence score.

## Notes

- Dataset: [UCI SMS Spam Collection](https://archive.ics.uci.edu/dataset/228/sms+spam+collection),
  5,572 labeled messages (ham/spam).
- `clean.py`'s `clean_text()` function is imported directly by `app.py`,
  so the exact same preprocessing is applied at both training and
  inference time — this consistency is important for the model to
  work correctly on new input.
- To retrain with different settings (e.g. more TF-IDF features, a new
  model), just edit `train.py` and re-run it; `app.py` will
  automatically pick up the new saved model.
