import pandas as pd

def get_train_cols(
    df_train: pd.DataFrame,
    cols_drop: list,
)-> list:
    train_cols = [
    col for col in df_train.columns if col not in cols_drop]

    return train_cols