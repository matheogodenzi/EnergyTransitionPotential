import matplotlib.pyplot as plt
import pandas as pd
import numpy as np 
import seaborn as sns

def calc_and_plot_cor_mat(df, linear=1, corr_threshold=0.2):
    # Create a zero matrix for correlation coefficients
    corr_mat = np.zeros(len(df.columns.drop("achieved_rp")))
    interesting_correlations ={}

    # Loop through columns and compute correlations
    for i, col in enumerate(df.columns.drop("achieved_rp")):
        # Check for constant column or NaN values
        print(col)
        if df[col].std() == 0 or df[col].isna().any():
            corr_mat[i] = np.nan  # Assign NaN if column is constant or has NaN values
        else:
            if linear:
                cor_per = df["achieved_rp"].corr(df[col], "pearson")
                corr_mat[i] = cor_per
                if (cor_per > corr_threshold) or (cor_per < -corr_threshold): 
                    interesting_correlations[col] = cor_per
            else:
                cor_spe = df["achieved_rp"].corr(df[col], "spearman")
                corr_mat[i] = cor_spe
                if (cor_spe > corr_threshold) or (cor_spe < -corr_threshold): 
                    interesting_correlations[col] = cor_spe

    # Reshape the correlation matrix (ensure it has the correct size)
    try:
        corr_mat = corr_mat.reshape(9, 6)  # Adjust (9, 6) to match your intended shape
    except ValueError as e:
        print("Reshape error:", e)

    print("Correlation matrix shape:", corr_mat.shape)

    # Plot the correlation matrix using seaborn
    """plt.figure(figsize=(8, 6))
    sns.heatmap(corr_mat, annot=True, cmap="coolwarm", vmin=-1, vmax=1)
    plt.title("Correlation of covariates vs achieved recommended potential - Type 7")
    plt.show()"""
    return corr_mat, interesting_correlations
