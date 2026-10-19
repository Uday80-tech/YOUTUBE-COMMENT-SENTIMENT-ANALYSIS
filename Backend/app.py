from fastapi import FastAPI 
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from Schemas.url import Input_URL
from Schemas.comment import commentsentiment , response ,VideoInfo
from model_and_utils.fetch_comments import fetch_comments ,get_video_details
from model_and_utils.predict import predict_sentiment

app = FastAPI()

@app.get("/")
def home():
    return JSONResponse(content={"message" : "Youtube comment sentiment analysis api" , "description" : "this api is developed  to analyse the sentiment of a particular youtube video by URL input "})

@app.put("/predict" , response_model= response)
def predict(url : Input_URL):
    id = url.video_id
    video_details = get_video_details(id)
    comments = fetch_comments(id)
    sentiments = predict_sentiment(comments)
    result = [commentsentiment(comment=comment , sentiment= sentiment)
              for comment , sentiment in zip(comments ,sentiments) ] 
    meta_data = VideoInfo(title=video_details["title"] , channel_name=video_details["channel_name"] ,upload_date=video_details["upload_date"] )
    
    return JSONResponse(status_code=200,content=jsonable_encoder({"result": result , "video_info" : meta_data}))

