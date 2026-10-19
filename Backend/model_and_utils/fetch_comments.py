import os
import requests
import streamlit as st
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()



def fetch_comments(video_id :str) -> list[str]:
    api_key = os.getenv("youtubev3_api")

    if not api_key:
        raise ValueError("youtubev3_api key not found")

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

        try:
            response = requests.get(url ,params=params , timeout=100)
            response.raise_for_status()

        except requests.HTTPError as exc:
            status = exc.response.status_code

            if status == 400:
                raise HTTPException(status_code=400,detail="Invalid video ID or bad request.")

            elif status == 403:
                raise HTTPException(
                    status_code=403,
                    detail="YouTube API access denied. Check your API key or quota."
                )

            elif status == 404:
                raise HTTPException(
                    status_code=404,
                    detail="Video not found. Please check the video ID."
                )

            else:
                raise HTTPException(
                    status_code=500,
                    detail="An unexpected error occurred while fetching comments."
                )
        except requests.RequestException:
            raise HTTPException(status_code=502,detail="Could not connect to YouTube API.")
            


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




def get_video_details(video_id: str) -> dict:
    api_key = os.getenv("youtubev3_api")

    url = "https://www.googleapis.com/youtube/v3/videos"

    params = {
        "part": "snippet",
        "id": video_id,
        "key": api_key
    }

    try:
        response = requests.get(url, params=params, timeout=100)
        response.raise_for_status()
        items = response.json().get("items", [])

        if not items:
            raise HTTPException(
                status_code=404,
                detail="Video details not found."
            )

        snippet = items[0]["snippet"]

        return {
            "title": snippet["title"],
            "channel_name": snippet["channelTitle"],
            "upload_date": snippet["publishedAt"][:10]
        }

    except requests.RequestException:
        raise HTTPException(
            status_code=502,
            detail="Unable to retrieve YouTube video details."
        )