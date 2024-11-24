#import libraries
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

#function
def merge_municipalities_covariates(df, merge_dict, target_mun_numbers=None, numeric_only=False):
    """
    Merges multiple municipalities based on a dictionary of source and target mappings, 
    selecting the most common value for non-numeric fields.

    Parameters:
    df (pd.DataFrame): The DataFrame containing municipal data.
    merge_dict (dict): Dictionary where keys are target municipalities, and values are lists of source municipalities.
    target_mun_numbers (dict, optional): Dictionary mapping target municipalities to their new MunicipalityNumbers.

    Returns:
    pd.DataFrame: Updated DataFrame with source municipalities merged and removed.
    """
    if numeric_only:
        # Coerce the entire DataFrame to numeric, converting non-numeric values to NaN
        df = df.apply(pd.to_numeric, errors='coerce')

    # Identify numeric and non-numeric columns
    numeric_columns = list(df.select_dtypes(include='number').columns)
    if "MunicipalityNumber" in numeric_columns:
        numeric_columns.remove("MunicipalityNumber")
    non_numeric_columns = list(df.select_dtypes(exclude='number').columns)

    for target, sources in merge_dict.items():
        # Filter to keep only the rows that exist in the DataFrame
        
        existing_rows = df.index[df.index.isin(sources)]
        #print(f"Existing rows for target '{target}': {existing_rows.tolist()}")
        
        try:
            # Sum numeric columns for the target and each source
            numeric_sum = df.loc[existing_rows, numeric_columns].fillna(0).sum()
            #print(f"Numeric sum for target '{target}': {numeric_sum}")
            
        except Exception as e:
            print(f"Error calculating numeric sum for target '{target}': {e}")
            numeric_sum = None

        non_numeric_data = {}
        try:
            # For non-numeric columns, determine the most common value across target and sources
            for col in non_numeric_columns:
                if not existing_rows.empty:  # Ensure there are rows to process
                    most_common_value = df.loc[existing_rows, col].mode().iloc[0]
                    non_numeric_data[col] = most_common_value
                    #print(f"Most common value in column '{col}' for target '{target}': {most_common_value}")
        except Exception as e:
            print(f"Error processing non-numeric columns for target '{target}': {e}")

        try:
            # Update target row with numeric sums and most common non-numeric values
            if numeric_sum is not None:
                for col, value in numeric_sum.items():
                    df.at[target, col] = value

            for col, value in non_numeric_data.items():
                df.at[target, col] = value

            # Update 'MunicipalityNumber' if specified in target_mun_numbers dictionary
            if target_mun_numbers and target in target_mun_numbers:
                df.loc[target, 'MunicipalityNumber'] = target_mun_numbers[target]

            # Ensure target is removed from sources to avoid self-referencing
            if target in sources:
                sources.remove(target)
            
            # Drop each source municipality row after merging
            df = df.drop(existing_rows, axis=0)

        except Exception as e:
            print(f"Error updating DataFrame for target '{target}': {e}")

    return df

if __name__ == "__main__": 

    # Create a dummy DataFrame
    data = {
        'Name': ['Alice', 'Bob', 'Charlie'],
        'Age': [25, 30, 35],
        'City': ['New York', 'Los Angeles', 'Chicago']
    }

    df = pd.DataFrame(data)
    print(df)



