import pandas as pd
import matplotlib.pyplot as plt
import numpy as np 
import seaborn as sns



def create_municipalities_dict(df):
    """
    Creates a dictionary of with the target municipylity as key and the merged municipalities as values
    
    input : correspondance df 
    output : merging dictionary

    """

    municipalities_dict = {}
    for index, row in df.iterrows():
        if row["Resulting municipality"] not in municipalities_dict.keys():
            if "Merged" in row["Fate"]:
                #print(row["Fate"])
                municipalities_dict[row["Resulting municipality"]]=[row["Name"]]
            elif "Incorporated" in row["Fate"]:
                municipalities_dict[row["Resulting municipality"]]=[row["Name"]]
            else:
                print(row["Fate"])
        else: 
            municipalities_dict[row["Resulting municipality"]].append(row["Name"])

    municipalities_dict["Buchegg"].append("Lüterswil-Gächliwil")
    municipalities_dict["Basse-Vendline"] = ["Bonfol", "Beurnevésin"]
    municipalities_dict["Reutigen"] = ["Zwieselberg"],
    municipalities_dict["Baden"]=["Turgi", "Baden"]
    municipalities_dict["Wangen an der Aare"]=["Wangenried", "Wangen an der Aare"]

    return municipalities_dict


