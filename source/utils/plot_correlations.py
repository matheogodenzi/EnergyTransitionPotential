import matplotlib.pyplot as plt 
import pandas as pd
import numpy as np
import seaborn as sns

def plot_main_corr(cor_df, type="Overall"):
    """
    Inputs:
    - cor_df["correlation, "Covariate"] (pandas Dataframe) : main correlations for each covariate of interest 
    - type (string) : should mention the mnicipality type

    Returns:
    none

    >plots the correlation graph
    """
    # Create the barplot with the 'Covariate' hue and a 'RdYlGn' palette
    plt.figure()
    sns.barplot(x="Covariate", y="correlation", data=cor_df, hue="Covariate", palette="RdYlGn", legend=True)

    # Customize grid, ticks, and labels
    plt.grid(axis="y")
    plt.xticks([])  # Hide x-ticks
    plt.xlabel("")
    plt.ylabel("Correlation [-]", size=12)

    # Title of the plot
    plt.title(f"Relevant correlations - {type}", size=15)

    # Move the legend below the plot
    plt.legend(title="Covariates", title_fontsize=14, loc="upper center", bbox_to_anchor=(0.5, -0.05), ncol=1, fontsize=12)  # Adjust legend position and number of columns

    # Show the plot with adjusted layout
    #plt.tight_layout()  # Adjust layout to avoid overlap
    plt.show()