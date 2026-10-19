import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import date

st.set_page_config(
    page_title="YouTube Sentiment Analysis",
    page_icon="🎬",
    layout="wide"
)

if "page" not in st.session_state:
    st.session_state.page =  "home"

st.title("🎬 YouTube Sentiment Analysis" )

st.divider()

#=====================================================Home Page=======================================================

if st.session_state.page == "home":
    
    st.markdown("Analyze the sentiment of YouTube video comments.")

    video_url = st.text_input("",placeholder="Paste your YouTube video URL here").strip()

    if "data" not in st.session_state:
        st.session_state.data = None

    if "video_url" not in st.session_state:
        st.session_state.video_url = ""

    if "meta_data" not in st.session_state:
            st.session_state.meta_data = None

    st.session_state.video_url = video_url

    if st.button("Analyze"):
        if video_url:

            try:
                #=====================================connection with fastapi=================================================

                url = "http://127.0.0.1:8000/predict"

                with st.spinner("Analyzing YouTube comments..."):
                    response = requests.put(url=url , json={"url" : video_url}  , timeout= 60)

                if response.status_code == 200:
                    result = response.json().get("result" , [])
                    meta_data = response.json().get("video_info" , {})
                    st.balloons()

                    df = pd.DataFrame(result)
                    st.session_state.data = df
                    st.session_state.meta_data = meta_data

                    st.session_state.page = "dashboard"
                    st.rerun()

                else:
                    error_message = response.json().get("detail","Something went wrong.")
                    st.error(error_message)

            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to FastAPI. Check that your backend is running.")

            except requests.exceptions.Timeout:
                st.error("The request timed out. Please try again.")

            except requests.exceptions.RequestException:
                st.error("A network error occurred. Please try again.")


        else:
            st.error("Enter Youtube Video Url")

#==========================================Dashboard page==================================================

if st.session_state.page == "dashboard":

    st.subheader("Dashboard")

    sentiment_counts = (st.session_state.data["sentiment"].value_counts().reindex(["positive", "negative", "neutral"], fill_value=0))

    # ================================Metrics======================================

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        with st.container(border=True):
            st.metric("Total Comments" , st.session_state.data.shape[0])

    with c2:
        with st.container(border=True):
            st.metric("😊 Positive", int(sentiment_counts["positive"]))

    with c3:
        with st.container(border=True):
            st.metric("😠 Negative", int(sentiment_counts["negative"]))

    with c4:
        with st.container(border=True):
            st.metric("😐 Neutral", int(sentiment_counts["neutral"]))


    if st.button("Analyze another video"):
        st.session_state.page = "home"
        st.rerun()

# =====================================================3 column layout========================================================

    col1 , col2 ,col3= st.columns(3)
    col1.video(st.session_state.video_url)  #col1 video

#======================================================col2 meta data=========================================================

    meta_data = st.session_state.meta_data

    with col2:
        with st.container(border=True):
            st.caption("📺 VIDEO OVERVIEW")

            st.markdown(meta_data.get("title", "Untitled video"))

            st.divider()

            st.caption("📡 YOUTUBE CHANNEL")
            st.markdown(f"**{meta_data.get('channel_name', 'Unknown channel')}**")

            st.caption("📅 PUBLISHED ON")
            upload_date = meta_data.get("upload_date", "")
            try:
                formatted_date = date.fromisoformat(upload_date).strftime("%d %B %Y")
            except (ValueError, TypeError):
                formatted_date = upload_date or "Unknown date"

            st.markdown(f"**{formatted_date}**")

# ===================================================col3 Plotly Chart=============================================================
    fig = px.pie(
        values=sentiment_counts.values,
        names=sentiment_counts.index,
        title="Sentiment Distribution",
        hole=0.6,
        color=sentiment_counts.index,
        color_discrete_map={
            "positive": "#22C55E",
            "negative": "#EF4444",
            "neutral": "#F59E0B"
        }
    )

    total = sentiment_counts.sum()
    fig.update_layout(
        title="Sentiment Distribution",
        showlegend=True,
        height = 300,
        width = 350,
        legend=dict(
            title="",
            orientation="v",
            x=1.02,
            y=0.5
        ),
        annotations=[
            dict(
                text=f"<b>{total}</b><br>Comments",
                x=0.5,
                y=0.5,
                font_size=18,
                showarrow=False
            )
        ],
        margin=dict(t=60, b=20, l=10, r=100),
        )

    col3.plotly_chart(fig, use_container_width=True)

#==================================================sentiment selection========================================================

    option = st.selectbox("Select An Option" , options= ["ALL" , "POSITIVE" ,"NEGATIVE" , "NEUTRAL"]).lower()
    filtered_df = st.session_state.data
    filtered_df = filtered_df if option == "all" else filtered_df[filtered_df["sentiment"] == option]

    st.download_button("Download the Analysis" ,
                        data= filtered_df.to_csv(index=False).encode("utf-8") ,
                        file_name= "sentiment.csv" ,
                        mime="text/csv")

    st.subheader(f"{option.capitalize()}  comments" if option != "all" else "Comments of the Video")

    #===============================================Showing Comments========================================================

    for comment, sentiment in zip(filtered_df["comment"],filtered_df["sentiment"]):

        with st.container(border=True):
            com1, com2 = st.columns([5, 1], vertical_alignment="center")

            with com1:
                st.write(comment)

            with com2:
                if sentiment == "positive":
                    st.success(sentiment.capitalize())
                elif sentiment == "negative":
                    st.error(sentiment.capitalize())
                else:
                    st.warning(sentiment.capitalize())
