import streamlit as st
import requests
import pandas as pd

st.set_page_config(
    page_title="YouTube Sentiment Analysis",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 YouTube Sentiment Analysis")
st.markdown("Analyze the sentiment of YouTube video comments.")

video_url = st.text_input("",placeholder="Paste your YouTube video URL here")

if st.button("Analyze"):
    if video_url:

        url = "http://127.0.0.1:8000/predict"
        response = requests.put(url=url , json={"url" : video_url}  , timeout= 35)
        if response.status_code == 200:
            result = response.json().get("result" , [])

        else:
            error_message = response.json().get("detail","Something went wrong.")
            st.error(error_message)


    else:
        st.warning("Enter Youtube Video Url")
    

