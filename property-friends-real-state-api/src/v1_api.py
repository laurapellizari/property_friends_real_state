from fastapi import FastAPI, HTTPException, Depends, Header
import mlflow
import mlflow.pyfunc
import pandas as pd
from typing import List
from property_friends_real_state_api.schemas.models import HealthSchema, InputFeatures
import os

v1_api = FastAPI()

API_KEYS = {
    "client_1": "api_key_1",
    "client_2": "api_key_2",
}

def validate_api_key(api_key: str = Header(...)):
    if api_key not in API_KEYS.values():
        raise HTTPException(status_code=401, detail="Invalid API key")
    return api_key


def get_model():

    model_uri = os.path.join("/app/property-friends-real-state-api/src/mlruns/model/artifacts", "model")
    
    model = mlflow.pyfunc.load_model(model_uri)

    return model

@v1_api.get("/health/", status_code=200)
async def root():
    return HealthSchema(
        api_up=True,
        api_version=1,
        message="API is healthy!"
    )

@v1_api.post("/predict/")
async def predict(
    features: List[InputFeatures], 
    model=Depends(get_model),
    api_key: str = Depends(validate_api_key) 
):
    try:
        if len(features) != 1:
            raise HTTPException(status_code=400, detail="Only one set of features is allowed")

        to_predict = pd.DataFrame([features[0].dict()])

        prediction = model.predict(to_predict)

        return {"prediction": prediction.tolist()}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")