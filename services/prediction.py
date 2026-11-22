import re
import joblib
import nltk
from pathlib import Path
from nltk.corpus import stopwords

# Load trained model and vectorizer
BASE_DIR = Path(__file__).resolve().parent.parent

model = joblib.load(BASE_DIR / "model" / "fake_news_model.pkl")
vectorizer = joblib.load(BASE_DIR / "model" / "tfidf_vectorizer.pkl")

# Load English stopwords
try:
    stop_words = set(stopwords.words("english"))
except LookupError:
    nltk.download("stopwords", quiet=True)
    stop_words = set(stopwords.words("english"))


def clean_text(text):
    text = text.lower()
    text = re.sub(r"https?://\S+|www\.\S+", "", text)
    text = re.sub(r"[^a-zA-Z]", " ", text)

    words = text.split()
    words = [word for word in words if word not in stop_words]

    return " ".join(words)


def predict_news(news):
    cleaned_news = clean_text(news)
    features = vectorizer.transform([cleaned_news])

    prediction = model.predict(features)[0]
    probabilities = model.predict_proba(features)[0]

    score = max(probabilities) * 100

    label = "REAL" if prediction == 1 else "FAKE"

    return label, round(score, 2)
