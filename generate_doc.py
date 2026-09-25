import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'''
        <w:tcMar {nsdecls("w")}>
            <w:top w:w="{top}" w:type="dxa"/>
            <w:bottom w:w="{bottom}" w:type="dxa"/>
            <w:left w:w="{left}" w:type="dxa"/>
            <w:right w:w="{right}" w:type="dxa"/>
        </w:tcMar>
    ''')
    tcPr.append(tcMar)

def create_document():
    doc = Document()

    # Set Margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Styles
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(51, 51, 51)

    # Document Header / Title
    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_run = title.add_run("SMS Spam Detection System")
    title_run.font.name = 'Calibri'
    title_run.font.size = Pt(26)
    title_run.font.bold = True
    title_run.font.color.rgb = RGBColor(24, 76, 120)

    subtitle = doc.add_paragraph()
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    subtitle_run = subtitle.add_run("Comprehensive Technical Documentation & Architecture Report")
    subtitle_run.font.size = Pt(14)
    subtitle_run.font.italic = True
    subtitle_run.font.color.rgb = RGBColor(100, 110, 125)

    doc.add_paragraph() # Spacing

    # Metadata Card (Table)
    meta_table = doc.add_table(rows=4, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        ("Project Name:", "SMS Spam Detector (NLP Machine Learning Pipeline)"),
        ("Technology Stack:", "Python 3, Scikit-Learn, NLTK, Pandas, Streamlit, Joblib"),
        ("Model Deployed:", "Linear Support Vector Classifier (LinearSVC) with TF-IDF"),
        ("Dataset:", "UCI SMS Spam Collection (5,572 messages)"),
    ]
    for i, (k, v) in enumerate(meta_data):
        row = meta_table.rows[i]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(2.0)
        c1.width = Inches(4.5)
        
        p0 = c0.paragraphs[0]
        r0 = p0.add_run(k)
        r0.bold = True
        r0.font.color.rgb = RGBColor(24, 76, 120)

        p1 = c1.paragraphs[0]
        p1.add_run(v)

        set_cell_background(c0, "F0F4F8")
        set_cell_background(c1, "F8FAFC")
        set_cell_margins(c0, 80, 80, 120, 120)
        set_cell_margins(c1, 80, 80, 120, 120)

    doc.add_paragraph() # Spacing

    # Section 1: Executive Summary
    h1 = doc.add_heading("1. Executive Summary", level=1)
    h1.style.font.color.rgb = RGBColor(24, 76, 120)
    p = doc.add_paragraph(
        "Short Message Service (SMS) spam poses ongoing security, privacy, and productivity concerns for mobile device users. "
        "Unsolicited messages often contain phishing attempts, financial fraud schemes, and aggressive promotional links. "
        "This project implements an end-to-end Natural Language Processing (NLP) and Machine Learning system that accurately "
        "classifies incoming SMS text messages as either legitimate ('ham') or unsolicited ('spam')."
    )
    p = doc.add_paragraph(
        "The project encompasses a complete machine learning lifecycle, starting from raw data ingestion and text normalization, "
        "through stratified TF-IDF feature extraction, multi-model evaluation and benchmark selection, to a responsive real-time "
        "web user interface built with Streamlit."
    )

    # Section 2: Project Architecture
    h1 = doc.add_heading("2. System Architecture & Workflow", level=1)
    h1.style.font.color.rgb = RGBColor(24, 76, 120)

    p = doc.add_paragraph("The pipeline operates through four discrete, decoupled stages:")
    
    stages = [
        ("Phase 1: Ingestion & Cleaning (clean.py)", "Parses raw dataset, addresses encoding anomalies, deduplicates records, strips noise (URLs, emails, punctuation, digits), removes English stopwords, and applies Porter stemming."),
        ("Phase 2: Feature Engineering & Training (train.py)", "Performs stratified train/test splitting, extracts 3,000 TF-IDF n-gram features, trains four distinct machine learning classifiers, and evaluates them on held-out test data."),
        ("Phase 3: Model Persistence (models/)", "Identifies the highest-performing model based on positive-class F1-score and serializes the model weights, vocabulary vectorizer, and test performance metrics."),
        ("Phase 4: Serving & Interface (app.py)", "Provides an interactive web dashboard using Streamlit for immediate inference, confidence scoring, model metric transparency, and text cleaning inspection.")
    ]
    for title, desc in stages:
        bp = doc.add_paragraph(style='List Bullet')
        r_title = bp.add_run(f"{title}: ")
        r_title.bold = True
        bp.add_run(desc)

    doc.add_paragraph()

    # Section 3: Directory Structure
    h1 = doc.add_heading("3. Repository Structure", level=1)
    h1.style.font.color.rgb = RGBColor(24, 76, 120)

    dir_table = doc.add_table(rows=9, cols=2)
    dir_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    dir_content = [
        ("File / Directory", "Description"),
        ("data/spam.csv", "Raw benchmark dataset containing 5,572 labeled messages (UCI/Kaggle)."),
        ("data/cleaned_spam.csv", "Preprocessed dataset produced by clean.py ready for feature extraction."),
        ("clean.py", "Data preprocessing script and reusable clean_text() pipeline."),
        ("train.py", "Script for TF-IDF feature extraction, model benchmarking, and artifact export."),
        ("app.py", "Streamlit web application providing real-time spam prediction."),
        ("models/best_model.joblib", "Serialized high-performing classification model (LinearSVC)."),
        ("models/vectorizer.joblib", "Fitted Scikit-Learn TfidfVectorizer (vocabulary of 3,000 features)."),
        ("models/metrics.json", "Evaluation metrics across all four evaluated algorithms.")
    ]
    for i, (path, desc) in enumerate(dir_content):
        row = dir_table.rows[i]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(2.2)
        c1.width = Inches(4.3)
        p0, p1 = c0.paragraphs[0], c1.paragraphs[0]
        if i == 0:
            r0 = p0.add_run(path)
            r1 = p1.add_run(desc)
            r0.bold = r1.bold = True
            r0.font.color.rgb = r1.font.color.rgb = RGBColor(255, 255, 255)
            set_cell_background(c0, "184C78")
            set_cell_background(c1, "184C78")
        else:
            p0.add_run(path).bold = True
            p1.add_run(desc)
            bg = "F4F6F9" if i % 2 == 1 else "FFFFFF"
            set_cell_background(c0, bg)
            set_cell_background(c1, bg)
        set_cell_margins(c0, 60, 60, 100, 100)
        set_cell_margins(c1, 60, 60, 100, 100)

    doc.add_paragraph()

    # Section 4: Detailed Component Breakdown
    h1 = doc.add_heading("4. Detailed Technical Implementation", level=1)
    h1.style.font.color.rgb = RGBColor(24, 76, 120)

    # 4.1 Data Cleaning & Preprocessing
    h2 = doc.add_heading("4.1 Preprocessing Pipeline (clean.py)", level=2)
    h2.style.font.color.rgb = RGBColor(40, 100, 150)
    p = doc.add_paragraph(
        "Raw text data contains considerable noise that hinders machine learning algorithms. The clean.py script "
        "implements a systematic cleaning procedure:"
    )
    clean_steps = [
        ("Encoding & Schema Rectification: ", "The original dataset contains latin-1 encoded characters and redundant empty columns (Unnamed: 2, 3, 4). The loader isolates the label and message columns exclusively."),
        ("Deduplication & Null Handling: ", "Drops invalid records and duplicate messages to prevent data leakage between train and test sets."),
        ("Text Normalization (clean_text): ", "Converts all characters to lowercase to preserve lexical uniformity."),
        ("Regular Expression Filtering: ", "Removes hyperlinked URLs (http://, https://, www) and email addresses using targeted regex patterns."),
        ("Non-Alphabetical Stripping: ", "Removes special characters, punctuation, and numerals ([^a-z\\s]), isolating word tokens."),
        ("Stopword Removal: ", "Filters out high-frequency syntactic stopwords using NLTK's English stopword corpus (e.g., 'the', 'is', 'at')."),
        ("Stemming: ", "Applies the Porter Stemmer algorithm to reduce word inflections to their morphological root (e.g., 'freezing', 'freezes' -> 'freez').")
    ]
    for s_title, s_desc in clean_steps:
        bp = doc.add_paragraph(style='List Bullet')
        r = bp.add_run(s_title)
        r.bold = True
        bp.add_run(s_desc)

    p_note = doc.add_paragraph()
    r_note = p_note.add_run("Architectural Highlight: ")
    r_note.bold = True
    r_note.font.color.rgb = RGBColor(180, 90, 20)
    p_note.add_run(
        "The clean_text() function is directly imported into app.py during live inference. "
        "This shared codebase eliminates 'training-serving skew'—ensuring that user inputs undergo the exact "
        "same transformation applied to the training dataset."
    )

    # 4.2 Feature Engineering & Model Training
    h2 = doc.add_heading("4.2 Feature Engineering & Training (train.py)", level=2)
    h2.style.font.color.rgb = RGBColor(40, 100, 150)
    
    p = doc.add_paragraph(
        "Text messages are variable-length strings of characters, requiring transformation into structured numerical matrices:"
    )

    points = [
        ("Stratified Split: ", "The dataset displays notable class imbalance (~87% ham vs. ~13% spam). A stratified 80/20 train/test split (random_state=42) guarantees identical class proportions across both subsets."),
        ("TF-IDF Vectorization: ", "Term Frequency-Inverse Document Frequency calculates the statistical relevance of words. The vectorizer is capped at the top 3,000 most informative features (max_features=3000), penalizing universally common terms while magnifying terms uniquely indicative of spam (e.g., 'claim', 'urgent', 'prize')."),
        ("Model Benchmarking: ", "Four distinct algorithmic families were trained and evaluated on identical test splits:")
    ]
    for p_title, p_desc in points:
        bp = doc.add_paragraph(style='List Bullet')
        bp.add_run(p_title).bold = True
        bp.add_run(p_desc)

    models_info = [
        ("Multinomial Naive Bayes (MultinomialNB)", "Applies Bayes' theorem with the assumption of strong independence between features. Very fast and effective for discrete word counts."),
        ("Logistic Regression (LogisticRegression)", "A generalized linear classification model estimating log-odds of a message being spam."),
        ("Linear Support Vector Machine (LinearSVC)", "Identifies the optimal hyper-plane with the maximum margin separating spam and ham vectors in high-dimensional space."),
        ("Random Forest (RandomForestClassifier)", "Ensemble method combining 200 bootstrapped decision trees to reduce prediction variance.")
    ]
    for m_name, m_desc in models_info:
        bp = doc.add_paragraph(style='List Bullet 2')
        bp.add_run(f"{m_name}: ").bold = True
        bp.add_run(m_desc)

    # Section 5: Model Evaluation & Benchmark Results
    h1 = doc.add_heading("5. Model Evaluation & Benchmark Results", level=1)
    h1.style.font.color.rgb = RGBColor(24, 76, 120)

    p = doc.add_paragraph(
        "Because of class imbalance, accuracy alone is misleading (a trivial model predicting all messages as 'ham' "
        "would achieve ~87% accuracy). The evaluation focuses on Precision, Recall, and the F1-Score of the positive (Spam) class:"
    )

    # Benchmark Table
    bench_table = doc.add_table(rows=5, cols=5)
    bench_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    bench_data = [
        ("Model", "Accuracy", "Precision (Spam)", "Recall (Spam)", "F1-Score (Spam)"),
        ("Linear SVM (Best)", "98.84%", "97.60%", "93.13%", "0.953"),
        ("Random Forest", "97.87%", "97.39%", "85.50%", "0.911"),
        ("Naive Bayes", "97.48%", "100.00%", "80.15%", "0.890"),
        ("Logistic Regression", "96.32%", "98.95%", "71.76%", "0.832")
    ]
    for i, row_data in enumerate(bench_data):
        row = bench_table.rows[i]
        for j, val in enumerate(row_data):
            cell = row.cells[j]
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if j > 0 else WD_ALIGN_PARAGRAPH.LEFT
            run = p.add_run(val)
            if i == 0:
                run.bold = True
                run.font.color.rgb = RGBColor(255, 255, 255)
                set_cell_background(cell, "184C78")
            elif i == 1:
                run.bold = True
                set_cell_background(cell, "EBF3FA")
            else:
                bg = "F9FAFB" if i % 2 == 1 else "FFFFFF"
                set_cell_background(cell, bg)
            set_cell_margins(cell, 60, 60, 80, 80)

    doc.add_paragraph()

    p_svm = doc.add_paragraph()
    r_svm = p_svm.add_run("Selection Rationale: ")
    r_svm.bold = True
    p_svm.add_run(
        "Linear SVM achieved the highest F1-Score (0.953) and Recall (93.13%) with exceptional Precision (97.60%). "
        "In high-dimensional sparse TF-IDF spaces (3,000 dimensions), text representations are frequently linearly "
        "separable, allowing Linear SVM to construct robust separation margins without overfitting."
    )

    # Section 6: Streamlit Application
    h1 = doc.add_heading("6. Web Interface & Real-Time Inference (app.py)", level=1)
    h1.style.font.color.rgb = RGBColor(24, 76, 120)

    p = doc.add_paragraph(
        "The project provides a production-style user interface built with Streamlit, enabling interactive testing and inspection:"
    )

    ui_features = [
        ("Cached Resource Loading: ", "Utilizes @st.cache_resource to load best_model.joblib, vectorizer.joblib, and metrics.json into memory once, ensuring sub-second inference latency."),
        ("Dynamic Confidence Calculation: ", "For models supporting decision margins (LinearSVC), applies a sigmoid transformation (1 / (1 + exp(-score))) to map arbitrary hyper-plane distances into calibrated probability estimates."),
        ("Interactive Diagnostics: ", "Includes a 'Show cleaned text' toggle that visualizes token extraction, stopword filtering, and stemming results for debugging and educational demonstration."),
        ("Sidebar Performance Dashboard: ", "Exposes the active model's benchmark accuracy, precision, recall, and F1-score directly to end users, fostering algorithmic transparency.")
    ]
    for uf_title, uf_desc in ui_features:
        bp = doc.add_paragraph(style='List Bullet')
        bp.add_run(uf_title).bold = True
        bp.add_run(uf_desc)

    doc.add_paragraph()

    # Section 7: Execution Guide
    h1 = doc.add_heading("7. Installation & Execution Guide", level=1)
    h1.style.font.color.rgb = RGBColor(24, 76, 120)

    steps = [
        ("Step 1: Install Dependencies", "pip install -r requirements.txt"),
        ("Step 2: Download NLTK Stopwords", "python -c \"import nltk; nltk.download('stopwords')\""),
        ("Step 3: Run Data Preprocessing", "python clean.py"),
        ("Step 4: Train & Compare Models", "python train.py"),
        ("Step 5: Launch Streamlit Web App", "streamlit run app.py")
    ]
    for s_title, s_cmd in steps:
        h3 = doc.add_heading(s_title, level=3)
        h3.style.font.color.rgb = RGBColor(40, 100, 150)
        p_cmd = doc.add_paragraph()
        run_cmd = p_cmd.add_run(f"    {s_cmd}")
        run_cmd.font.name = 'Consolas'
        run_cmd.font.size = Pt(10)
        run_cmd.font.color.rgb = RGBColor(30, 41, 59)

    doc.add_paragraph()

    # Section 8: Recommendations & Enhancements
    h1 = doc.add_heading("8. Future Enhancements & Recommendations", level=1)
    h1.style.font.color.rgb = RGBColor(24, 76, 120)

    enhancements = [
        ("Feature Union with Engineered Metadata: ", "clean.py already computes char_count, word_count, digit_count, and has_url. Integrating these numerical signals alongside TF-IDF via Scikit-Learn's ColumnTransformer could further boost detection on short, URL-heavy messages."),
        ("N-Gram Range Expansion: ", "Upgrading TF-IDF to support bi-grams (ngram_range=(1, 2)) would capture contextual token pairs such as 'claim prize', 'urgent call', or 'gift card'."),
        ("Transformer-Based Models: ", "Benchmarking modern transfer learning approaches (e.g., DistilBERT or RoBERTa) to capture deep contextual semantics beyond bag-of-words assumptions.")
    ]
    for e_title, e_desc in enhancements:
        bp = doc.add_paragraph(style='List Bullet')
        bp.add_run(e_title).bold = True
        bp.add_run(e_desc)

    # Save document
    output_path = r"c:\NLP PROJECT\SMS_Spam_Detection_Project_Documentation.docx"
    doc.save(output_path)
    print(f"Document successfully created at: {output_path}")

if __name__ == "__main__":
    create_document()

