import pickle


model = pickle.load(open(r"model_and_utils/model.pkl" , "rb"))




def predict_sentiment(comment : list[str]):
    if comment:
        sentiments = model.predict(comment)

        return [sentiment.lower() for sentiment in sentiments]
    else:
        return ["no comments found"]
    