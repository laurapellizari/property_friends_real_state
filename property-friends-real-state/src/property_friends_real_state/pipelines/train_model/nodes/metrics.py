import numpy as np
import pandas as pd
import mlflow
from sklearn.metrics import (
    mean_squared_error,
    mean_absolute_percentage_error,
    mean_absolute_error)


def evaluate_model(
    y_pred: np.ndarray,
    y_test: np.ndarray,
)-> dict:
    
    results = {}

    results['rmse'] = [np.sqrt(mean_squared_error(y_pred, y_test))]
    results['mae'] = [mean_absolute_error(y_pred, y_test)]
    results['mape'] = [mean_absolute_percentage_error(y_pred, y_test)]

    df_results = pd.DataFrame.from_dict(results)

    mlflow.log_metric("RMSE", results['rmse'][0])
    mlflow.log_metric("MAE", results['mae'][0])
    mlflow.log_metric("MAPE", results['mape'][0])

    return df_results

