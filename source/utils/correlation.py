import matplotlib.pyplot as plt
import pandas as pd
import numpy as np 
import seaborn as sns

def calc_and_plot_cor_mat(df, linear=1):
    # Create a zero matrix for correlation coefficients
    corr_mat = np.zeros(len(df.columns.drop("achieved_rp")))

    # Loop through columns and compute correlations
    for i, col in enumerate(df.columns.drop("achieved_rp")):
        # Check for constant column or NaN values
        if df[col].std() == 0 or df[col].isna().any():
            corr_mat[i] = np.nan  # Assign NaN if column is constant or has NaN values
        else:
            if linear:
                corr_mat[i] = df["achieved_rp"].corr(df[col], "pearson")
            else:
                corr_mat[i] = df["achieved_rp"].corr(df[col], "spearman")

    # Reshape the correlation matrix (ensure it has the correct size)
    try:
        corr_mat = corr_mat.reshape(9, 6)  # Adjust (9, 6) to match your intended shape
    except ValueError as e:
        print("Reshape error:", e)

    print("Correlation matrix shape:", corr_mat.shape)

    # Plot the correlation matrix using seaborn
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr_mat, annot=True, cmap="coolwarm", vmin=-1, vmax=1)
    plt.title("Correlation of covariates vs achieved recommended potential - Type 7")
    plt.show()
    return corr_mat
