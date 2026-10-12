import os
import requests
import streamlit as st


def fetch_comments(video_id :str) -> list[str]:
    api_key = os.getenv("youtubev3_api")

    if not api_key:
        raise ValueError("api key not found")

    url = "https://www.googleapis.com/youtube/v3/commentThreads"

    comments = []
    page_token = None

    while True:
        params  = params = {
            "part": "snippet",
            "videoId": video_id,
            "maxResults": 100,
            "textFormat": "plainText",
            "key": api_key}
        if page_token:
            params["pageToken"] = page_token

        response = requests.get(url ,params=params , timeout=30)
        response.raise_for_status()

        data = response.json()

        threads = data.get("items" ,[])
        for thread in threads:
            comment = (
                thread["snippet"]["topLevelComment"]
                ["snippet"]["textDisplay"]
            )

            comments.append(comment)

        page_token = data.get("nextPageToken")

        if not page_token:
            break
    return comments


id = st.text_input("enter  youtube video id")
data = fetch_comments(id)
st.write(data)
st.write(len(data))
        