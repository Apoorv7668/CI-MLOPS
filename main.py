from fastapi import FastAPI
import mlflow
from pydantic import BaseModel
import pandas as pd

app = FastAPI(
    title="Water Potability Prediction",
    description="Predicting Water Potability"
)

# Set up MLflow tracking
dagshub_url = "https://dagshub.com"
repo_owner = "Apoorv7668"
repo_name = "CI-MLOPS"
mlflow.set_tracking_uri(f"{dagshub_url}/{repo_owner}/{repo_name}.mlflow")
print(mlflow.get_tracking_uri())
# mlflow.set_experiment("FINAL MODEL")

def load_model():
    client = mlflow.tracking.MlflowClient()
    versions = client.get_latest_versions("Best Model", stages=["Staging"])
    run_id = versions[0].run_id
    return mlflow.pyfunc.load_model(f"runs:/{run_id}/Best Model")

# Load the model once to avoid reloading during every prediction
model = load_model()

class Water(BaseModel):
    ph: float
    Hardness: float
    Solids: float
    Chloramines: float
    Sulfate: float
    Conductivity: float
    Organic_carbon: float
    Trihalomethanes: float
    Turbidity: float

@app.get("/")
def home():
    return {"message": "Welcome to Water Potability Prediction FastAPI"}

@app.post("/predict")
def model_predict(water: Water):
    # Convert the input data into a DataFrame
    sample = pd.DataFrame({
        'ph': [water.ph],
        'Hardness': [water.Hardness],
        'Solids': [water.Solids],
        'Chloramines': [water.Chloramines],
        'Sulfate': [water.Sulfate],
        'Conductivity': [water.Conductivity],
        'Organic_carbon': [water.Organic_carbon],
        'Trihalomethanes': [water.Trihalomethanes],
        'Turbidity': [water.Turbidity]
    })

    # Model prediction
    predicted_value = model.predict(sample)

    # Assuming the model's output is an array
    if predicted_value[0] == 1:
        return {"prediction": "Water is Consumable"}
    else:
        return {"prediction": "Water is not Consumable"}
