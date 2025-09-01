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

def get_columns() -> List[str]:
    artifact = Client().get_artifact_version("56baba9b-3f02-4942-8219-223bb71117e7")
    data = artifact.load()
    column_names = list(data.columns)
    return column_names

def get_artifacts() -> Tuple[Dict, StandardScaler, RandomForestClassifier]:
    """Returns the encoder dictionary, scaler, and model artifact."""
    artifact = Client().get_artifact_version(str(encoder_id))
    label_encoders = artifact.load()
    artifact = Client().get_artifact_version(str(scaler_id))
    scaler = artifact.load()
    artifact = Client().get_artifact_version(str(model_id))
    model = artifact.load()
    return label_encoders, scaler, model

def predict_Target(data: Dict) -> str:
    # Map incoming schema field names to training column names
    column_mapping = {
        "Marital_status": "Marital status",
        "Application_mode": "Application mode",
        "Application_order": "Application order",
        "Course": "Course",
        "Daytime_evening_attendance": "Daytime/evening attendance",
        "Previous_qualification": "Previous qualification",
        "Nacionality": "Nacionality",
        "Mothers_qualification": "Mother's qualification",
        "Fathers_qualification": "Father's qualification",
        "Mothers_occupation": "Mother's occupation",
        "Father_occupation": "Father's occupation",
        "Displaced": "Displaced",
        "Education_special_needs": "Educational special needs",
        "Debtor": "Debtor",
        "Tuition_fees_up_to_date": "Tuition fees up to date",
        "Gender": "Gender",
        "Scholarship_holder": "Scholarship holder",
        "Age_at_enrollment": "Age at enrollment",
        "International": "International",
        "Curricular_units_1st_sem_credited": "Curricular units 1st sem (credited)",
        "Curricular_units_1st_sem_enrolled": "Curricular units 1st sem (enrolled)",
        "Curricular_units_1st_sem_evaluations": "Curricular units 1st sem (evaluations)",
        "Curricular_units_1st_sem_approved": "Curricular units 1st sem (approved)",
        "Curricular_units_1st_sem_grade": "Curricular units 1st sem (grade)",
        "Curricular_units_1st_sem_without_evaluations": "Curricular units 1st sem (without evaluations)",
        "Curricular_units_2nd_sem_credited": "Curricular units 2nd sem (credited)",
        "Curricular_units_2nd_sem_enrolled": "Curricular units 2nd sem (enrolled)",
        "Curricular_units_2nd_sem_evaluations": "Curricular units 2nd sem (evaluations)",
        "Curricular_units_2nd_sem_approved": "Curricular units 2nd sem (approved)",
        "Curricular_units_2nd_sem_grade": "Curricular units 2nd sem (grade)",
        "Curricular_units_2nd_sem_without_Evaluations": "Curricular units 2nd sem (without evaluations)",
        "Unemployment_rate": "Unemployment rate",
        "Inflation_rate": "Inflation rate",
        "GDP": "GDP"
    }

    # apply mapping
    final_data = {column_mapping.get(column, column): [value] for column, value in data.items()}
    logger.info(f"Mapped input data: {final_data}")

    final_data = pd.DataFrame(final_data)

    label_encoders, scaler, model = get_artifacts()

    # Only encode feature columns, not Target
    for column_name in label_encoders.keys():
        if column_name != "Target" and column_name in final_data.columns:
            final_data[column_name] = label_encoders[column_name].transform(final_data[column_name])

    # scale the dataset
    columns = list(final_data.columns)
    final_data = scaler.transform(final_data)
    final_data = pd.DataFrame(data=final_data, columns=columns)

    # get prediction (integer)
    pred = model.predict(final_data)

    # decode integer to string label
    target_label = label_encoders["Target"].inverse_transform([pred[0]])[0]
    return target_label

if __name__ == "__main__":
    # Test case
    data = {
        "Marital_status": "Single",
        "Application_mode": 1,
        "Application_order": 1,
        "Course": 33,
        "Daytime_evening_attendance": 1,
        "Previous_qualification": 1,
        "Nacionality": 1,
        "Mothers_qualification": 19,
        "Fathers_qualification": 19,
        "Mothers_occupation": 5,
        "Father_occupation": 4,
        "Displaced": 0,
        "Education_special_needs": 0,
        "Debtor": 0,
        "Tuition_fees_up_to_date": 1,
        "Gender": "Male",
        "Scholarship_holder": 0,
        "Age_at_enrollment": 20,
        "International": 0,
        "Curricular_units_1st_sem_credited": 6,
        "Curricular_units_1st_sem_enrolled": 6,
        "Curricular_units_1st_sem_evaluations": 6,
        "Curricular_units_1st_sem_approved": 6,
        "Curricular_units_1st_sem_grade": 14,
        "Curricular_units_1st_sem_without_evaluations": 0,
        "Curricular_units_2nd_sem_credited": 6,
        "Curricular_units_2nd_sem_enrolled": 6,
        "Curricular_units_2nd_sem_evaluations": 6,
        "Curricular_units_2nd_sem_approved": 6,
        "Curricular_units_2nd_sem_grade": 13,
        "Curricular_units_2nd_sem_without_Evaluations": 0,
        "Unemployment_rate": 10.5,
        "Inflation_rate": 2.5,
        "GDP": 1.2
    }
    print(predict_Target(data=data))
