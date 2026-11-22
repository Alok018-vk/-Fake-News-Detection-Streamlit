# Fake News Detection System

A simple Fake News Detection web application built using Python, Machine Learning, Streamlit and Google Fact Check API.

## Features

- Predicts whether news is FAKE or REAL using Logistic Regression.
- Uses TF-IDF for text feature extraction.
- Searches existing fact-check reviews using Google Fact Check API.
- Stores prediction history using SQLite.
- Provides a simple Streamlit interface.

## Technologies Used

- Python
- Streamlit
- Scikit-learn
- TF-IDF
- Logistic Regression
- SQLite
- Google Fact Check API

## Project Structure

```text
Fake-News-Detection-Streamlit/
│
├── app.py
├── database.py
├── requirements.txt
├── model/
│   ├── fake_news_model.pkl
│   └── tfidf_vectorizer.pkl
│
├── services/
│   ├── prediction.py
│   ├── fact_check.py
│   └── __init__.py
│
├── .env.example
├── .gitignore
└── README.md
