import pandas as pd
import re
import string
import pickle

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder


# --------------------------------------------------
# LOAD DATASET
# --------------------------------------------------

data = pd.read_csv("UpdatedResumeDataSet.csv")

data = data[["Resume", "Category"]]

print("Total Records:", len(data))


# --------------------------------------------------
# REMOVE SMALL CATEGORIES
# --------------------------------------------------

category_counts = data["Category"].value_counts()

valid_categories = category_counts[
    category_counts >= 20
].index

data = data[
    data["Category"].isin(valid_categories)
]

print("Records After Filtering:", len(data))


# --------------------------------------------------
# CLEAN TEXT
# --------------------------------------------------

def clean_text(text):

    text = str(text).lower()

    text = re.sub(r"\d+", "", text)

    text = text.translate(
        str.maketrans("", "", string.punctuation)
    )

    text = re.sub(r"\s+", " ", text).strip()

    return text


data["Resume"] = data["Resume"].apply(clean_text)


# --------------------------------------------------
# FEATURES AND LABELS
# --------------------------------------------------

X = data["Resume"]

y = data["Category"]


# --------------------------------------------------
# LABEL ENCODING
# --------------------------------------------------

label_encoder = LabelEncoder()

y = label_encoder.fit_transform(y)

print("Total Categories:", len(label_encoder.classes_))


# --------------------------------------------------
# TRAIN TEST SPLIT
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# --------------------------------------------------
# TF-IDF VECTORIZATION
# --------------------------------------------------

vectorizer = TfidfVectorizer(
    max_features=15000,
    stop_words="english"
)

X_train_tfidf = vectorizer.fit_transform(X_train)

X_test_tfidf = vectorizer.transform(X_test)


# --------------------------------------------------
# TRAIN MODEL
# --------------------------------------------------

print("Training Model...")

base_model = LinearSVC()

model = CalibratedClassifierCV(
    base_model,
    cv=5
)

model.fit(
    X_train_tfidf,
    y_train
)


# --------------------------------------------------
# PREDICTION
# --------------------------------------------------

predictions = model.predict(X_test_tfidf)

accuracy = accuracy_score(
    y_test,
    predictions
)

print("Model Accuracy:", accuracy)


# --------------------------------------------------
# SAVE MODEL FILES
# --------------------------------------------------

with open("models/svm_model.pkl", "wb") as f:
    pickle.dump(model, f)


with open("models/tfidf_vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)


with open("models/label_encoder.pkl", "wb") as f:
    pickle.dump(label_encoder, f)


print("Model files saved successfully")