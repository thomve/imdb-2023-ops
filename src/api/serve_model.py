from fastapi import FastAPI
import numpy as np
import xgboost as xgb

from src.api.schemas import ImdbData

app = FastAPI()

model = xgb.Booster()
model.load_model("output/xgb.json")


@app.post("/predict")
def predict(data: ImdbData):
    features = np.array([[data.isAdult, 
                 data.runtimeMinutes, 
                 data.averageRating,
                 data.numVotes,
                 data.budget,
                 data.release_year,
                 data.release_month,
                 data.release_day,
                 data.Adventure,
                 data.Animation,
                 data.Drama,
                 data.Action,
                 data.Crime]])

    features = xgb.DMatrix(features)
    prediction = model.predict(features)
    return {"prediction": prediction[0]}