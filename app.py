import streamlit as st
import pandas as pd

from services.prediction import predict_news
from services.fact_check import fact_check_news
from database import create_table, save_prediction, get_history

# Page settings
st.set_page_config(
    page_title="Fake News Detector",
    page_icon="🔍",
    layout="wide"
)

create_table()

st.title("🔍 Fake News Detection System")
st.write("Check news using Machine Learning and Google Fact Check API.")

tab1, tab2 = st.tabs(["Check News", "Prediction History"])

# News prediction page
with tab1:

    news = st.text_area(
        "Enter News Article",
        height=200,
        placeholder="Paste your news article here..."
    )

    if st.button("Check News", type="primary"):

        if len(news.strip()) < 20:
            st.warning("Please enter a longer news article.")

        else:
            with st.spinner("Analyzing news..."):

                prediction, score = predict_news(news)

                save_prediction(news, prediction, score)

                fact_check = fact_check_news(news)

            st.subheader("Machine Learning Result")

            if prediction == "FAKE":
                st.error("Prediction: FAKE")
            else:
                st.success("Prediction: REAL")

            st.write(f"Model Score: {score}%")
            st.caption("This score is the model's prediction probability, not proof of truth.")

            st.divider()

            st.subheader("Google Fact Check Results")

            if fact_check["error"]:
                st.warning(fact_check["error"])

            elif fact_check["results"]:

                for item in fact_check["results"]:

                    st.write(f"**Claim:** {item['claim']}")
                    st.write(f"**Publisher:** {item['publisher']}")
                    st.write(f"**Review:** {item['title']}")
                    st.write(f"**Rating:** {item['rating']}")

                    if item["url"]:
                        st.markdown(f"[Read Full Review]({item['url']})")

                    st.divider()

            else:
                st.info("No matching fact-check reviews found.")

            st.caption(
                "Fact-check results refer to specific reviewed claims. "
                "No result does not mean the news is true."
            )


# Prediction history page
with tab2:

    st.subheader("Previous Predictions")

    history = get_history()

    if history:

        df = pd.DataFrame(
            history,
            columns=["ID", "News", "Prediction", "Score", "Date"]
        )

        st.dataframe(df, width="stretch", hide_index=True)

    else:
        st.info("No prediction history available yet.")
