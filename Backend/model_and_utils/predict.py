import pickle


model = pickle.load(open("model.pkl" , "rb"))




def predict_sentiment(comment : list[str]):
    if comment:
        sentiments = model.predict(comment)
        return sentiments
    else:
        return ["no comments found"]
    