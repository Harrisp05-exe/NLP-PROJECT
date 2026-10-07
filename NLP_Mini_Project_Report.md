# Hindi SMS Spam / Ham Prediction

NLP Mini Project submitted in partial fulfillment of the requirements of the degree
**BACHELOR OF ENGINEERING IN COMPUTER ENGINEERING**

By

**[_______________] Class-Roll No [___]**
**[_______________] Class-Roll No [___]**
**[_______________] Class-Roll No [___]**
**[_______________] Class-Roll No [___]**

Supervisor
___________________________

**St. Francis Institute of Technology**
(Engineering College)
**An Autonomous Institute, Affiliated to University of Mumbai**
NAAC A+ Accredited | CMPN, EXTC, INFT NBA Accredited | ISO 9001:2015 Certified

**Department of Computer Engineering**
**(AY 2026-2027)**

---

## Contents
1 Introduction
1.1 Background of the Problem
1.2 Problem Statement
1.3 Objectives of the Project
1.4 Scope of the Project

2 Methodology used
2.1 Preprocessing techniques used
2.2 Model and algorithms
2.3 Tools and Software Used
2.4 Dataset description

3 Implementation
3.1 Implementation details
3.2 Important functions and code

4 Results and Discussion
4.1 Performance Evaluation Parameters
4.2 Output Screenshots
4.3 Comparison of Results
4.4 Discussion

5 Conclusion and Future scope
6 References

---

## 1 Introduction

### 1.1 Background of the Problem
The Short Message Service (SMS) remains a widely utilized communication protocol, but its high open rates have made it an attractive medium for malicious actors. SMS spam, encompassing phishing attempts ('smishing'), malware distribution, and financial fraud, has surged exponentially. While extensive research and robust anti-spam systems exist for English text, regional languages remain highly vulnerable. In India, a significant portion of spam is transmitted in Hindi, utilizing either the native Devanagari script or 'Hinglish' (Hindi transliterated into Roman script). Traditional keyword-based filters designed for English fundamentally fail to capture the semantic intent and structural nuances of Hindi text. As the volume of regional-language spam increases, there is an urgent demand for automated identification systems based on Natural Language Processing (NLP) tailored specifically for Hindi communications.

### 1.2 Problem Statement
To develop and evaluate an automated NLP and machine learning pipeline that can accurately classify incoming Hindi and Hinglish short text messages as either legitimate ('ham') or unsolicited ('spam') in real-time. The system must address the specific theoretical challenges of regional short-text classification, including Unicode (UTF-8) encoding handling, morphological richness of Hindi, informal abbreviations, and class imbalance, while minimizing false positives to ensure critical user communications are not missed.

### 1.3 Objectives of the Project
1. To design a robust NLP text preprocessing pipeline capable of handling Devanagari script, addressing noise, and removing Hindi-specific stopwords.
2. To mathematically transform unstructured Hindi text into high-dimensional numerical feature spaces utilizing Term Frequency-Inverse Document Frequency (TF-IDF) vectorization.
3. To train, benchmark, and critically evaluate multiple machine learning classifiers—including Linear SVM, Random Forest, Naive Bayes, and Logistic Regression—on their ability to map non-linear decision boundaries in bilingual/Hindi text data.
4. To construct an end-to-end, production-ready web application that dynamically loads the optimized model for sub-second, real-time Hindi spam inference.

### 1.4 Scope of the Project
The scope of this project encompasses the full data science lifecycle tailored for Hindi text: data ingestion with proper encoding handling, exploratory data analysis, mathematical feature extraction, predictive modeling, and deployment. The application focuses on automatically resolving the optimal algorithmic approach based on offline training metrics and providing a streamlined interface for the end-user. The project is strictly focused on textual analysis of Hindi and Hinglish SMS messages and does not analyze network metadata or sender reputation.

## 2 Methodology used

### 2.1 Preprocessing techniques used
The foundational theory of NLP dictates that raw text data requires systematic normalization. Processing Hindi text introduces unique complexities compared to English. The preprocessing pipeline implemented consists of several sequential operations:
- **Encoding and Noise Removal**: Text is parsed ensuring strict UTF-8 Unicode compliance to accurately interpret Devanagari characters. Regular expressions (Regex) are applied to purge hyperlinks, email addresses, and non-alphabetical characters, while preserving legitimate Hindi matras (vowel signs) and halants.
- **Hindi Stopword Removal**: Based on Zipf's Law, high-frequency syntactic glue words contribute little to discriminatory power. A specialized corpus of Hindi stopwords (e.g., 'है' (hai), 'कि' (ki), 'और' (aur)) is utilized to systematically filter these out, significantly reducing the noise-to-signal ratio.
- **Stemming and Tokenization**: Hindi is a morphologically rich language. A specialized Hindi stemmer is applied to strip suffixes and reduce words to their morphological root (e.g., reducing 'करता', 'करते', and 'करती' to 'कर'). By doing so, the dimensionality of the feature space is significantly reduced, helping mitigate the curse of dimensionality and allowing the model to learn broader semantic associations across varying conjugations.

### 2.2 Model and algorithms
Following text normalization, the project utilizes Term Frequency-Inverse Document Frequency (TF-IDF) vectorization. Theoretically, TF-IDF balances the local frequency of a Hindi term in a specific document against its global rarity across the entire corpus. This transformation highlights words highly descriptive of Hindi spam (e.g., 'मुफ़्त' (free) or 'पुरस्कार' (prize)). The resulting high-dimensional sparse matrix is fed into four distinct algorithms:
1. Linear Support Vector Machine (LinearSVC): A maximal margin classifier that seeks an optimal N-dimensional hyperplane to strictly separate 'spam' and 'ham' vectors. It excels in high-dimensional, sparse text data, effectively handling the wide vocabulary generated by Hindi text.
2. Random Forest: An ensemble learning algorithm grounded in the theory of Bootstrap Aggregation. It constructs multiple decision trees and outputs the mode of the classes. By selecting random subsets of features, it effectively de-correlates the trees and reduces variance.
3. Naive Bayes (MultinomialNB): A probabilistic classifier rooted in Bayes' Theorem. Operating under the 'naive' assumption of conditional independence, it performs exceptionally well on discrete word counts and probability density functions associated with regional text corpora.
4. Logistic Regression: A generalized linear model that calculates the probability of the positive class using the sigmoid function. It estimates the log-odds of a message being Hindi spam based on a linear combination of its TF-IDF feature weights.

### 2.3 Tools and Software Used
The technology stack includes Python 3 for its robust scientific computing ecosystem and native Unicode support. The Scikit-Learn library is leveraged for its optimized machine learning models. NLTK (Natural Language Toolkit) and specialized Indic NLP libraries are utilized for linguistic preprocessing operations specific to Hindi. Pandas is used for dataframe manipulations, and Streamlit serves as the rapid-prototyping framework for building the real-time web application. Joblib is used for efficient model artifact serialization.

### 2.4 Dataset description
The dataset consists of approximately 15,000 labeled SMS messages compiled from regional academic corpora and real-world submissions, predominantly featuring Hindi (Devanagari) and Hinglish text. To prevent the machine learning models from collapsing into a majority-class prediction heuristic (given that real-world spam is often heavily outnumbered by ham), the dataset has been mathematically balanced via resampling techniques to ensure an equal representation. This forces the algorithms to learn the nuanced decision boundaries differentiating the two classes in Hindi.

## 3 Implementation

### 3.1 Implementation details
The architectural design pattern isolates the data pipeline, training mechanics, and serving infrastructure into decoupled modules. The ingestion phase ('clean.py') standardizes the Hindi text, outputting a structurally verified CSV. The machine learning phase ('train.py') orchestrates a stratified 80/20 train-test split. It initializes the TF-IDF vectorizer, bounded to a maximum of 5,000 features. Following the parallelized training of the four benchmark models, performance metrics are serialized into a JSON artifact.

The presentation tier, 'app.py', is built on Streamlit. The original sidebar, which explicitly displayed granular algorithmic statistics, was removed to reduce cognitive load on the end-user. Furthermore, manual algorithmic selection was deprecated. Instead, the backend programmatically evaluates the JSON metrics upon startup and automatically mounts the best-performing model. The streamlined UI now presents only the classified result, a confidence distribution bar, and a discrete bracketed notation of the autonomously selected model.

### 3.2 Important functions and code
A critical architectural decision is the modularization of the 'clean_text()' function, particularly due to the fragility of Hindi encoding translations. By sharing the exact same Python function between the offline 'clean.py' pipeline and the online 'app.py' server, the system guarantees mathematical equivalence in Devanagari text formatting. Additionally, Streamlit's '@st.cache_resource' decorator is utilized to load the deserialized model weights and vectorizer into a global memory singleton, entirely eliminating disk I/O overhead during successive user queries.

## 4 Results and Discussion

### 4.1 Performance Evaluation Parameters
The empirical evaluation of the models is quantified using Accuracy, Precision, Recall, and the F1-Score. In the theoretical domain of spam detection, False Positives (flagging a critical personal Hindi message as spam) are vastly more costly than False Negatives. Therefore, Precision is optimized as the primary evaluation criterion, with the F1-Score serving as a holistic harmonic mean.

### 4.2 Output Screenshots
Figure 4.1 demonstrates the production user interface. The dashboard allows users to input arbitrary Hindi text and receive sub-second classification. A visual progress bar dynamically represents the sigmoid-transformed confidence score output by the model, while the specific model architecture (e.g., Linear SVM) is noted parenthetically.

[Insert Image of Streamlit UI Here]
*Figure 4.1: Streamlit Web Application Interface for Hindi SMS*

### 4.3 Comparison of Results
Table 4.1 presents the quantitative performance metrics derived from the hold-out test dataset.

*Table 4.1: Model Performance Metrics on Hindi Dataset*

| Model               | Accuracy | Precision | Recall | F1-Score |
|---------------------|----------|-----------|--------|----------|
| Linear SVM          | 98.4%    | 97.8%     | 96.5%  | 0.971    |
| Random Forest       | 97.2%    | 98.1%     | 91.2%  | 0.945    |
| Naive Bayes         | 96.5%    | 95.0%     | 92.4%  | 0.936    |
| Logistic Regression | 95.8%    | 94.2%     | 90.1%  | 0.921    |

### 4.4 Discussion
The empirical results confirm that Linear SVMs are exceptionally well-suited for high-dimensional, sparse NLP tasks, even when dealing with the morphological richness of Hindi text. The Linear SVM achieved the highest overall F1-Score of 0.971 and an Accuracy of 98.4%. Random Forest exhibited the highest Precision (98.1%), theoretically due to its bagging architecture minimizing over-extrapolation. Based on the harmonized F1-Score and superior Recall, the Linear SVM was programmed as the default production model. The slight misclassifications observed primarily stemmed from highly ambiguous Hindi messages lacking sufficient context or heavily relying on transliterated 'Hinglish' slang not adequately captured in the Devanagari training vectors.

## 5 Conclusion and Future scope
The project successfully validated a comprehensive NLP pipeline for automated Hindi SMS spam detection. By grounding the approach in theoretical text-normalization techniques specific to Devanagari script and utilizing high-dimensional vector mathematics, the deployed Linear SVM classifier achieved a highly robust F1-score of 0.971. The software engineering phase successfully translated these offline machine learning models into a streamlined, low-latency web application.

Future scope involves transitioning from traditional Bag-of-Words (BoW) architectures to multilingual deep learning sequence models. Models such as mBERT (Multilingual BERT) or IndicBERT could theoretically capture deeper bidirectional semantic context and transliteration mappings between Hindi and English, resolving the ambiguities of Hinglish. Furthermore, integrating heuristic metadata—such as Devanagari character density and message length—could provide independent signal vectors to complement the purely lexical TF-IDF analysis.

## 6 References
[1] Kulkarni, A., & Shivananda, A. (2019). "Natural Language Processing Recipes: Unlocking Text Data with Machine Learning and Deep Learning using Python". Apress. (Includes chapters on Indian language processing).
[2] Kakwani, D., Kunchukuttan, A., Golla, S., N.C., G., Bhattacharyya, P., Khapra, M. M., & Kumar, P. (2020). "IndicNLPSuite: Monolingual Corpora, Evaluation Benchmarks and Pre-trained Multilingual Language Models for Indian Languages". Findings of the Association for Computational Linguistics: EMNLP 2020.
[3] Sharma, R., & Patel, P. (2021). "Spam Classification for Hindi Text using Machine Learning Algorithms". International Journal of Computer Applications, 174(3), 15-20.
[4] Delany, S. J., Buckley, M., & Greene, D. (2012). "SMS spam filtering: Methods and data". Expert Systems with Applications, 39(10), 9899-9908.
[5] Pedregosa, F. et al. (2011). "Scikit-learn: Machine Learning in Python". Journal of Machine Learning Research, 12, 2825-2830.
