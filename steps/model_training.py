# import the needed libraries

from zenml import step
import pandas as pd
import numpy as np
from zenml.logger import get_logger
from typing_extensions import Annotated
from typing import Optional,Tuple,Dict
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score,recall_score,f1_score

# configure our logging
logger = get_logger(__name__)

@step
def train_model(X_train: pd.DataFrame, 
                y_train:pd.Series,
                X_test:pd.DataFrame,
                y_test: pd.Series) -> Annotated[Optional[RandomForestClassifier],
                                                "Model Object"]:
    model = None
    try:
        model = RandomForestClassifier(random_state=23,max_depth=12,min_samples_split=20,
                              min_samples_leaf=10,class_weight='balanced')
        model.fit(X_train, y_train)
        train_preds = model.predict(X_train)
        test_preds = model.predict(X_test)
        
        # compute the scores
        train = f1_score(y_train, train_preds, average='weighted')
        test = f1_score(y_test, test_preds, average='weighted')
        
        logger.info(f"""
                    Completed training the base model with metrics:
                    train: {train}
                    test: {test}
                    """)
    except Exception as err:
        logger.error(f"An error occured. Detail: {err}")
    
    return model