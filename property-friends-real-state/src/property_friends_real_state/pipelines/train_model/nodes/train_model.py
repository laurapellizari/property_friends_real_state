from sklearn.ensemble import GradientBoostingRegressor
from sklearn.pipeline import Pipeline
from category_encoders import TargetEncoder
from sklearn.compose import ColumnTransformer
import pandas as pd
import numpy as np
import os
import mlflow
from mlflow import sklearn

tags = {
    "Project": "property-friends-real-state",
}
    
def train_model(
        train: pd.DataFrame,
        train_cols: list,
        target: str,
        categorical_cols: dict,
        parameters_model: dict
)-> GradientBoostingRegressor:
    
    categorical_transformer = TargetEncoder()

    preprocessor = ColumnTransformer(
        transformers=[
            ('categorical',
            categorical_transformer,
            categorical_cols)
        ])

    steps = [
        ('preprocessor', preprocessor),
        ('model', GradientBoostingRegressor(**parameters_model))
    ]

    pipeline = Pipeline(steps)

    pipeline.fit(train[train_cols], train[target])
    
    mlflow.set_experiment("property-friends-real-state")
    mlflow.set_tags(tags)

    mlflow.sklearn.log_model(pipeline, "model")
    mlflow.sklearn.save_model(pipeline, "model")
    return pipeline

def predict_model(
    pipeline: Pipeline,
    test: pd.DataFrame,
    train_cols: list,
    target: dict
) -> np.ndarray:

    test_predictions = pipeline.predict(test[train_cols])
    test_target = test[target].values

    return test_target, test_predictions