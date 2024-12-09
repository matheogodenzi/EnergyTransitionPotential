#import libraries
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

import requests
from bs4 import BeautifulSoup
from io import StringIO  # Import StringIO
# load cleaned pronovo data 

# Now, you can import the functions
from municipality_dict import create_municipalities_dict
from replace_nan import replace_nan_based_on_type

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
    #print("umeric columns :", numeric_columns)
    #print("Non-numeric columns:", non_numeric_columns)
    for target, sources in merge_dict.items():
        # Filter to keep only the rows that exist in the DataFrame
        
        existing_rows = df.index[df.index.isin(sources)]
        print(f"Existing rows for target '{target}': {existing_rows.tolist()}")
        
        numeric_sum = None
        if len(existing_rows.tolist()) >0:
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
                print("Numeric sum.", numeric_sum)
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

    import re 

    import sys
    import os

    # Dynamically add the 'utils' folder to the Python path
    sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '../../source/')))

    datapath = "data/cleaned_data/Swiss_solar_potential.csv"
    Swiss_solar_potential_df = pd.read_csv(datapath)
    Swiss_solar_potential_df.set_index("mun_name", inplace=True)
    print(Swiss_solar_potential_df.head())

    print(Swiss_solar_potential_df[Swiss_solar_potential_df.index=="Seedorf"])

    # Define the Wikipedia page URL
    url = 'https://en.wikipedia.org/wiki/List_of_former_municipalities_of_Switzerland'  # Example URL

    # Send a GET request to the page
    response = requests.get(url)

    # Parse the page content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the first table on the page (You can also specify which table to scrape)
    table = soup.find('table', {'class': 'wikitable'})

    # Convert the table HTML to a StringIO object
    table_html = str(table)
    table_io = StringIO(table_html)

    # Use pandas to read the table from the StringIO object
    df_wiki = pd.read_html(table_io)[0]

    # Display the DataFrame
    df_wiki = df_wiki.sort_values(by="Year", ascending=True, inplace=False)
    df_wiki = df_wiki[df_wiki.Year >= 2000]

    #testing
    df_wiki[df_wiki.Fate.str.contains('Lugano', case=False, na=False)]

    # importing population data 
    population_df = pd.read_excel('data/raw_data/Municipal_populations_2023.xlsx', skiprows=5, skipfooter=11)
    population_df.columns = ["MunicipalityNumber", "MunicipalityName", "Population"]
    population_df.set_index("MunicipalityName", inplace=True)
    print(population_df.head())

    # Get a dictionary of merged municipalities
    mun_dict = create_municipalities_dict(df_wiki)
    print("**********************************")
    print(mun_dict)
    print("***********************************")
    new_muns = list(mun_dict.keys())
    mask = Swiss_solar_potential_df.index.str.contains('|'.join( rf"\b{re.escape(term)}\b" for term in new_muns), case=False, na=False)
    new_mun_ids_dict = Swiss_solar_potential_df.loc[mask].mun_id.to_dict()
    print("**********************************")
    print(new_mun_ids_dict)
    print("***********************************")

    population_2024_df= merge_municipalities_covariates(population_df,mun_dict,new_mun_ids_dict)
    print(population_2024_df)

    print(population_2024_df[population_2024_df.MunicipalityNumber.isna()])
    print()
    print(Swiss_solar_potential_df[Swiss_solar_potential_df.index=="Luzern"])
    print(population_2024_df[population_2024_df.index=="Luzern"])

    
    """
    mun_dict_test = {
        "Miralago" :["Miralago 1", "Miralago 2"]
    }

    new_mun_ids_dict_test = {
        "Miralago" : 5
    }


    test_dict = {
        "MunicipalityName" : ["Chur", "Poschiavo", "Le Prese", "Brusio", "Miralago 1", "Miralago 2"], 
        "MunicipalityNumber" : [1, 2, 3, 4, 5, 6],
        "Population": [36453, 1234, 543, 567, 45, 63]
    }

    test_df = pd.DataFrame(test_dict)
    test_df.set_index("MunicipalityName", inplace=True)
    print(test_df.head(6))
    trial_df= merge_municipalities_covariates(test_df,mun_dict_test,new_mun_ids_dict_test)
    print(trial_df.head(5))
    """



