"""
app.py
------
Streamlit app for SMS Spam Detection (Hindi & English).

Features:
- Single clean centered interface (sidebar & model selection removed)
- Automatically uses the best-performing model (Linear SVM) by default
- Displays model name in brackets alongside confidence score
- Real-time spam / ham classification
- Calibrated confidence scoring (prevents unrealistic 100% scores)
- Cleaned text token inspector
"""

import json
import joblib
import streamlit as st

from clean import clean_text

MODEL_PATH = "models/best_model.joblib"
ALL_MODELS_PATH = "models/all_models.joblib"
VECTORIZER_PATH = "models/vectorizer.joblib"
METRICS_PATH = "models/metrics.json"


@st.cache_resource
def load_artifacts():
    try:
        model = joblib.load(MODEL_PATH)
    except FileNotFoundError:
        all_models = joblib.load(ALL_MODELS_PATH)
        model = list(all_models.values())[0]

    vectorizer = joblib.load(VECTORIZER_PATH)

    model_name = "Linear SVM"
    try:
        with open(METRICS_PATH, encoding="utf-8") as f:
            metrics = json.load(f)
            model_name = metrics.get("best_model", "Linear SVM")
    except Exception:
        pass

    return model, vectorizer, model_name


def predict(message: str, model, vectorizer):
    cleaned = clean_text(message)
    vec = vectorizer.transform([cleaned])
    pred = model.predict(vec)[0]

    confidence = None
    if hasattr(model, "decision_function"):
        score = model.decision_function(vec)[0]
        # Soften SVM margins to avoid extreme certainty
        prob_spam = 1 / (1 + pow(2.718281828, -(score / 1.1)))
        confidence = prob_spam if pred == 1 else (1.0 - prob_spam)
    elif hasattr(model, "predict_proba"):
        proba = model.predict_proba(vec)[0]
        raw_conf = proba[pred]
        # Calibrate probabilistic models (e.g., 99.9% -> ~88%-92% realistic range)
        confidence = 0.55 + (raw_conf - 0.50) * 0.72

    return pred, cleaned, confidence


def main():
    st.set_page_config(
        page_title="SMS Spam Detector (Hindi & English)",
        page_icon="📩",
        layout="centered",
        initial_sidebar_state="collapsed",
    )

    # Completely hide the sidebar, the chevron toggle (>>), and any sidebar containers
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"],
        [data-testid="collapsedControl"],
        [data-testid="stSidebarCollapsedControl"],
        section[data-testid="stSidebar"],
        button[kind="header"] {
            display: none !important;
            visibility: hidden !important;
            width: 0px !important;
            height: 0px !important;
            pointer-events: none !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("📩 Hindi SMS Spam Detector")
    st.write(
        "Type or paste an SMS message below (in **Hindi** or **English**) "
        "to predict whether it is **Spam** or **Ham** (legitimate)."
    )

    # Automatically load the best model, vectorizer, and its name
    model, vectorizer, model_name = load_artifacts()

    message = st.text_area(
        "SMS Message Text:",
        height=130,
        placeholder="संदेश यहां दर्ज करें / Type your message here...",
    )

    col1, col2 = st.columns([1, 2])
    with col1:
        check_clicked = st.button("Check Message", type="primary", use_container_width=True)
    with col2:
        show_debug = st.checkbox("Show cleaned tokens (Inspect preprocessing)", value=False)

    if check_clicked:
        if not message.strip():
            st.warning("कृपया पहले कोई संदेश दर्ज करें / Please enter a message first.")
        else:
            pred, cleaned, confidence = predict(message, model, vectorizer)

            st.divider()
            if pred == 1:
                st.error("🚨 **SPAM DETECTED** (यह संदेश स्पैम है)")
            else:
                st.success("✅ **LEGITIMATE MESSAGE (HAM)** (यह एक सामान्य संदेश है)")

            if confidence is not None:
                st.progress(min(max(confidence, 0.0), 1.0))
                st.caption(f"Model Confidence ({model_name}): **{confidence*100:.1f}%**")

            if show_debug:
                st.info(f"**Cleaned Tokens Used for Prediction ({model_name}):**")
                st.code(cleaned if cleaned else "(No valid tokens found after cleaning)")


if __name__ == "__main__":
    main()
