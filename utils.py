from zenml.client import Client
from sklearn.ensemble import RandomForestClassifier
import logging
from logging import getLogger
import pandas as pd
import numpy as np
from typing import List, Tuple, Dict
from sklearn.preprocessing import StandardScaler
from dotenv import load_dotenv
import os

load_dotenv()

model_id = os.getenv(key="MODEL_ARTIFACT")
scaler_id = os.getenv(key="SCALER_ARTIFACT")
encoder_id = os.getenv(key="ENCODER_ARTIFACT")

# configure logging
logging.basicConfig(level=logging.INFO)
logger = getLogger(__name__)

# get the columns in the training_data
def get_columns() -> List[str]:
    artifact = Client().get_artifact_version("4ee0e3f0-e141-48c7-b416-b6dc6caaedbf")
    data = artifact.load()
    column_names = list(data.columns)
    
    return column_names

# get the scaler, encoder and model objects.
def get_artifacts() -> Tuple[Dict, StandardScaler, RandomForestClassifier]:
    """This function returns the encoder dictionary,
    model, standard scaler object and model artifact
    associated with the prod training pipeline."""
    
    # encoder
    artifact = Client().get_artifact_version(str(encoder_id))
    label_encoders = artifact.load()
    # scaler
    artifact = Client().get_artifact_version(str(scaler_id))
    scaler = artifact.load()
    # model
    artifact = Client().get_artifact_version(str(model_id))
    model = artifact.load()
    
    return label_encoders, scaler, model

# write a function that makes prediction

def predict_Target(data: Dict) -> float:
    final_data = {column:[value] for column, value in data.items()}
    logger.info(f"data: {final_data}")
    final_data = pd.DataFrame(final_data)
    label_encoders, scaler, model = get_artifacts()
    for column_name in label_encoders.keys():
        final_data[column_name] = label_encoders[column_name].transform(final_data[column_name])
    # scale the dataset
    columns = list(final_data.columns)
    final_data = scaler.transform(final_data)
    final_data = pd.DataFrame(data=final_data, columns=columns)
    
    # get prediction
    pred = model.predict(final_data)
    
    return pred[0]

if __name__ == "__main__":
    data = {
        
        "Marital status": 1,
        "application mode": 1,
        "application order": 1,
        "course": 9,
        "daytime/evening attendance": 0,
        "previous qualification": 1,
        "nacionality": 1,
        "mother's qualification": 3,
        "father's qualification": 3,
        "mother's occupation": 3,
        "father's occupation": 3,
        "displaced": 0,
        "educational special needs": 0,
        "debtor": 0,
        "tuition fees up to date": 1,
        "gender": 1,
        "scholarship holder": 0,
        "age at enrollment": 18,
        "international": 0,
        "Curricular units 1st sem (credited)": 0,
        "Curricular units 1st sem (enrolled)": 0,
        "Curricular units 1st sem (evaluations)": 5,
        "Curricular units 1st sem (approved)": 5,
        "Curricular units 1st sem (grade)": 5,
        "Curricular units 1st sem (without evaluations)": 0,
        "Curricular units 2nd sem (credited)": 0,
        "Curricular units 2nd sem (enrolled)": 5,
        "Curricular units 2nd sem (evaluations)": 5,
        "Curricular units 2nd sem (approved)": 4,
        "Curricular units 2nd sem (grade)": 13.5,
        "Curricular units 2nd sem (without evaluations)": 0,
        "Unemployment rate": 7.5,
        "Inflation rate": 2.3,
        "GDP": 2.5
    }
    print(predict_Target(data=data))