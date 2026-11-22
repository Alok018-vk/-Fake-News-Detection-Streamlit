
import os
import re
import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://factchecktools.googleapis.com/v1alpha1/claims:search"


def fact_check_news(news):
    api_key = os.getenv("GOOGLE_FACT_CHECK_API_KEY")

    if not api_key:
        return {"error": "Google API key not found.", "results": []}

    # Clean the search text
    query = re.sub(r"https?://\S+", "", news)
    query = re.sub(r"\s+", " ", query).strip()
    query = query[:300]

    try:
        response = requests.get(
            API_URL,
            params={
                "query": query,
                "languageCode": "en",
                "pageSize": 5,
                "key": api_key
            },
            timeout=15
        )

        response.raise_for_status()
        data = response.json()

        results = []

        for claim in data.get("claims", []):
            for review in claim.get("claimReview", []):
                results.append({
                    "claim": claim.get("text", ""),
                    "publisher": review.get("publisher", {}).get("name", ""),
                    "title": review.get("title", ""),
                    "rating": review.get("textualRating", ""),
                    "url": review.get("url", "")
                })

        return {"error": None, "results": results}

    except requests.RequestException as error:
        return {"error": str(error), "results": []}
