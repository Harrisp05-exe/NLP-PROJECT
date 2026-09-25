"""
clean.py
--------
Loads the SMS Spam dataset, cleans it, and saves a
processed version ready for feature extraction / training.
Supports English, Hindi (Devanagari), and Hinglish text.

Steps:
  1. Load raw CSV (UTF-8 / latin-1 fallback, handles various column namings).
  2. Keep only the label + message columns, rename them.
  3. Drop nulls and invalid rows.
  4. Add a binary target column (spam=1, ham=0).
  5. Clean message text: lowercase, strip URLs/emails, keep Hindi + English
     letters, remove stopwords, stem English tokens.
  6. Save cleaned dataset to data/cleaned_spam.csv
"""

import re
import string
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

RAW_PATH = "data/hindi_sms_spam_ham_15000.csv"
OUT_PATH = "data/cleaned_spam.csv"

# Hindi common stopwords
HINDI_STOPWORDS = {
    "है", "हैं", "के", "की", "का", "में", "से", "को", "पर", "और",
    "यह", "वह", "भी", "तो", "ही", "था", "थे", "थी", "रहा", "रहे",
    "रही", "हूं", "ने", "या", "कर", "लिया", "गया", "करना", "होने"
}
STOPWORDS = set(stopwords.words("english")).union(HINDI_STOPWORDS)
STEMMER = PorterStemmer()

URL_RE = re.compile(r"(https?://\S+|www\.\S+)")
EMAIL_RE = re.compile(r"\S+@\S+")
# Retain Devanagari Hindi (\u0900-\u097F), English alphabets (a-zA-Z), and whitespace
NON_ALPHA_RE = re.compile(r"[^\u0900-\u097Fa-zA-Z\s]")


def load_raw(path: str = RAW_PATH) -> pd.DataFrame:
    """Load raw dataset with UTF-8 encoding and fallback to latin-1."""
    try:
        df = pd.read_csv(path, encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(path, encoding="latin-1")

    # Rename common column aliases
    if "sms" in df.columns:
        df = df.rename(columns={"sms": "message"})
    elif "v1" in df.columns and "v2" in df.columns:
        df = df.rename(columns={"v1": "label", "v2": "message"})
    elif "Category" in df.columns and "Message" in df.columns:
        df = df.rename(columns={"Category": "label", "Message": "message"})

    if "label" not in df.columns or "message" not in df.columns:
        df = df.iloc[:, :2]
        df.columns = ["label", "message"]
    else:
        df = df[["label", "message"]]

    return df


def basic_clean(df: pd.DataFrame) -> pd.DataFrame:
    """Drop nulls, normalize labels, add binary target."""
    df = df.dropna(subset=["label", "message"]).copy()
    df["label"] = df["label"].astype(str).str.strip().str.lower()
    df = df[df["label"].isin(["ham", "spam"])]
    df["target"] = (df["label"] == "spam").astype(int)
    return df.reset_index(drop=True)


def clean_text(text: str) -> str:
    """
    Normalize a single SMS message (works for Hindi and English):
      - lowercase
      - remove URLs and emails
      - remove non-alphabetic characters (preserving Devanagari & English)
      - tokenize on whitespace
      - drop stopwords
      - stem English tokens with PorterStemmer
    """
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = URL_RE.sub(" ", text)
    text = EMAIL_RE.sub(" ", text)
    text = NON_ALPHA_RE.sub(" ", text)
    tokens = text.split()
    cleaned = []
    for tok in tokens:
        if tok in STOPWORDS:
            continue
        if len(tok) <= 1 and tok.isascii():
            continue
        if tok.isascii():
            tok = STEMMER.stem(tok)
        cleaned.append(tok)
    return " ".join(cleaned)


def add_text_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add numeric text features."""
    df["char_count"] = df["message"].astype(str).str.len()
    df["word_count"] = df["message"].astype(str).str.split().apply(len)
    df["digit_count"] = df["message"].astype(str).apply(lambda x: sum(c.isdigit() for c in x))
    df["has_url"] = df["message"].astype(str).str.contains(URL_RE.pattern, regex=True).astype(int)
    return df


def main():
    print(f"Loading dataset from {RAW_PATH}...")
    df = load_raw()
    print(f"  raw shape: {df.shape}")

    print("Basic cleaning (nulls, labels)...")
    df = basic_clean(df)
    print(f"  after basic clean: {df.shape}")
    print(df["label"].value_counts())

    print("Adding numeric text features...")
    df = add_text_features(df)

    print("Cleaning message text (Hindi/English stopwords, stemming, non-alpha)...")
    df["clean_text"] = df["message"].apply(clean_text)

    # Drop any rows that became empty after cleaning
    before = len(df)
    df = df[df["clean_text"].str.strip() != ""].reset_index(drop=True)
    print(f"  dropped {before - len(df)} rows that were empty after cleaning")

    df.to_csv(OUT_PATH, index=False, encoding="utf-8")
    print(f"Saved cleaned dataset to {OUT_PATH} -> shape {df.shape}")


if __name__ == "__main__":
    main()
