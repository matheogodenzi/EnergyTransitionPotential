import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

def replace_nan_based_on_type(df, columns):
    """
    Replaces NaN values in numeric columns with their mean, 
    and in non-numeric columns with their mode.

    Parameters:
    df (pd.DataFrame): The input DataFrame.

    Returns:
    pd.DataFrame: DataFrame with NaN values replaced.
    """

    df = df.copy()
    # Identify numeric and non-numeric columns
    numeric_columns = df.select_dtypes(include='number').columns
    non_numeric_columns = df.select_dtypes(exclude='number').columns

    # Replace NaN in numeric columns with the mean
    for column in numeric_columns:
        if column in columns: 
            mean_value = df[column].mean()
            df[column]=df[column].fillna(mean_value)
            print(f"Replaced NaN in numeric column '{column}' with mean: {mean_value}")

    # Replace NaN in non-numeric columns with the mode
    for column in non_numeric_columns:
        if column in columns: 
            try:
                mode_value = df[column].mode()[0]  # Get the first mode in case of ties
                df[column]=df[column].fillna(mode_value)
                print(f"Replaced NaN in non-numeric column '{column}' with mode: {mode_value}")
            except IndexError:
                print(f"Warning: Non-numeric column '{column}' has no mode (all values might be NaN).")

    return df