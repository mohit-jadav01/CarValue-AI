from fastapi import FastAPI
from fastapi.responses import JSONResponse
from schema import CarFeature, PredictionResponce
from model import load_artifacts,predict_price

app=FastAPI(title='Car Price Prediction',version='1.0')

@app.on_event('startup')
def startup_event():
    load_artifacts()

@app.get('/')
def test():
    return JSONResponse(status_code=200,content={'success':'true','route':'Test route work successfully'})


@app.post("/predict", response_model=PredictionResponce)
def predict(features: CarFeature):
    price = predict_price(features.model_dump())
    return PredictionResponce(prediction_price=price)


