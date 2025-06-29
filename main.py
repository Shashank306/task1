from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import numpy as np
import joblib

# Load model
preprocessor = joblib.load('column_transformer.pkl')
model = joblib.load('watch_accuracy_model.pkl')

# Define expected input data model
class WatchInput(BaseModel):
    Device_Name: str
    Brand: str
    Model: str
    Category: str
    Price_USD: float
    Battery_Life_Hours: float
    User_Satisfaction_Rating: float
    GPS_Accuracy_Meters: float
    Health_Sensors_Count: int
    Performance_Score: float
    Test_Date_Timestamp: float  # UNIX timestamp

# Create FastAPI app
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Watch Accuracy Prediction API"}

@app.post("/predict")
def predict_watch_accuracy(data: WatchInput):
    # Convert input data to a single-row DataFrame
    input_df = pd.DataFrame([data.dict()])

    # Preprocess the input using the saved ColumnTransformer
    input_processed = preprocessor.transform(input_df)

    # Predict using the trained model
    prediction = model.predict(input_processed)[0]

    # Return the prediction in JSON format
    return {
        "Heart_Rate_Accuracy_Percent": round(prediction[0], 2),
        "Step_Count_Accuracy_Percent": round(prediction[1], 2),
        "Sleep_Tracking_Accuracy_Percent": round(prediction[2], 2)
    }
