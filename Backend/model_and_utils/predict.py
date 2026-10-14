import pickle
import pandas as pd
import re


model = pickle.load(open(r"model_and_utils/model.pkl" , "rb"))
big_model = pickle.load(open(r"model_and_utils/big_model.pkl" , "rb"))



  



def preprocess(text):
    pro_text =re.sub("[^a-zA-z]" , " " ,text)
    pro_text = pro_text.lower()
    return pro_text


def predict_sentiment(comment : list[str]):
    if comment:
        comment = [preprocess(text) for text in comment]
        
        sentiments = model.predict(comment)

        return [sentiment.lower() for sentiment in sentiments]
    else:
        return ["no comments found"]
    