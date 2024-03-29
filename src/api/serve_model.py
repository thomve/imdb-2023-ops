import mlflow
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import ValidationError

from schemas import ImdbData


app = FastAPI()


model_name = "imdb-model"
model_version = 1
model_uri = f"models:/{model_name}@champion"

mlflow.set_tracking_uri("/home/mlflow-backend-store")
model = mlflow.pyfunc.load_model(model_uri=model_uri)

@app.post("/predict")
def predict(data: ImdbData):
    try:
        features = [[
            data.isAdult, 
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
            data.Crime]]
        prediction = model.predict(features).tolist()

        return {"prediction": prediction[0]}
    
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=str(ve))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

if __name__ == "__main__":
    uvicorn.run("serve_model:app", port=8080, log_level="info")