"""
train.py
--------
Loads the cleaned dataset, builds TF-IDF features, trains several
classifiers, compares them, and saves the models + vectorizer to disk
for use by the Streamlit app.

Models compared:
  - Multinomial Naive Bayes
  - Logistic Regression
  - Linear SVM
  - Random Forest
"""

import json
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
)

DATA_PATH = "data/cleaned_spam.csv"
MODEL_PATH = "models/best_model.joblib"
ALL_MODELS_PATH = "models/all_models.joblib"
VECTORIZER_PATH = "models/vectorizer.joblib"
METRICS_PATH = "models/metrics.json"

RANDOM_STATE = 42


def load_data():
    df = pd.read_csv(DATA_PATH, encoding="utf-8")
    df = df.dropna(subset=["clean_text"])
    return df


def get_models():
    return {
        "Linear SVM": LinearSVC(random_state=RANDOM_STATE),
        "Naive Bayes": MultinomialNB(),
        "Random Forest": RandomForestClassifier(
            n_estimators=100, random_state=RANDOM_STATE, n_jobs=-1
        ),
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=RANDOM_STATE),
    }


def evaluate(model, X_test, y_test):
    preds = model.predict(X_test)
    return {
        "accuracy": accuracy_score(y_test, preds),
        "precision": precision_score(y_test, preds, zero_division=0),
        "recall": recall_score(y_test, preds, zero_division=0),
        "f1": f1_score(y_test, preds, zero_division=0),
        "confusion_matrix": confusion_matrix(y_test, preds).tolist(),
        "report": classification_report(y_test, preds, target_names=["ham", "spam"], zero_division=0),
    }


def main():
    print("Loading cleaned data...")
    df = load_data()
    X = df["clean_text"]
    y = df["target"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
    )
    print(f"Train size: {len(X_train)}, Test size: {len(X_test)}")

    print("Vectorizing text with TF-IDF...")
    # ngram_range (1, 2) captures individual Hindi words as well as 2-word collocations
    vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    results = {}
    trained_models = {}

    for name, model in get_models().items():
        print(f"\nTraining {name}...")
        model.fit(X_train_vec, y_train)
        metrics = evaluate(model, X_test_vec, y_test)
        results[name] = metrics
        trained_models[name] = model
        print(
            f"  accuracy={metrics['accuracy']:.4f}  "
            f"precision={metrics['precision']:.4f}  "
            f"recall={metrics['recall']:.4f}  "
            f"f1={metrics['f1']:.4f}"
        )

    # Pick best model by F1 on the spam class
    best_name = max(results, key=lambda n: results[n]["f1"])
    best_model = trained_models[best_name]
    print(f"\nBest model: {best_name} (F1={results[best_name]['f1']:.4f})")
    print("\nClassification report for best model:")
    print(results[best_name]["report"])

    # Save vectorizer + best model + all models dictionary
    joblib.dump(vectorizer, VECTORIZER_PATH)
    joblib.dump(best_model, MODEL_PATH)
    joblib.dump(trained_models, ALL_MODELS_PATH)
    print(f"\nSaved vectorizer -> {VECTORIZER_PATH}")
    print(f"Saved best model ({best_name}) -> {MODEL_PATH}")
    print(f"Saved all models dictionary -> {ALL_MODELS_PATH}")

    # Save metrics summary
    summary = {
        name: {
            "accuracy": m["accuracy"],
            "precision": m["precision"],
            "recall": m["recall"],
            "f1": m["f1"],
            "confusion_matrix": m["confusion_matrix"],
        }
        for name, m in results.items()
    }
    summary["best_model"] = best_name
    with open(METRICS_PATH, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(f"Saved metrics summary -> {METRICS_PATH}")


if __name__ == "__main__":
    main()
