from fastapi import FastAPI 
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from Schemas.url import Input_URL
from Schemas.comment import commentsentiment , response
from model_and_utils.fetch_comments import fetch_comments
from model_and_utils.predict import predict_sentiment

app = FastAPI()

@app.get("/")
def home():
    return JSONResponse(content={"message" : "Youtube comment sentiment analysis api" , "description" : "this api is developed  to analyse the sentiment of a particular youtube video by URL input "})

@app.put("/predict" , response_model= response)
def predict(url : Input_URL):
    id = url.video_id

    comments = fetch_comments(id)
    sentiments = predict_sentiment(comments)
    result = [commentsentiment(comment=comment , sentiment= sentiment)
              for comment , sentiment in zip(comments ,sentiments) ] 
    return JSONResponse(status_code=200,content=jsonable_encoder({"result": result}))