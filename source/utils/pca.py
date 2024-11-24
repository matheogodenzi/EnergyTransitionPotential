import numpy as np
import pandas as pd

def pca(data, n_components=2):
    """
    Perform PCA on the given data and return the transformed data along with
    the principal components (eigenvectors).

    Parameters:
    data (ndarray or pd.DataFrame): Input data where each row is a data point and each column is a feature.
    n_components (int): Number of principal components to keep (default is 2).

    Returns:
    transformed_data (ndarray): The data projected onto the top `n_components` principal components.
    components (ndarray): The principal components (eigenvectors).
    explained_variance (ndarray): Variance explained by each component.
    """
    
    # Step 1: Center the data (zero mean)
    mean = np.mean(data, axis=0)
    centered_data = data - mean
    print(f"Centered data : {centered_data}")
    # Step 2: Compute the covariance matrix
    covariance_matrix = np.cov(centered_data, rowvar=False)
    print(f"Covariance matrix : {covariance_matrix}")

    # Step 3: Compute eigenvalues and eigenvectors
    eigenvalues, eigenvectors = np.linalg.eigh(covariance_matrix)  # egh is faster and more accurate for symmetric matrices
    
    # Step 4: Sort eigenvalues and eigenvectors
    sorted_indices = np.argsort(eigenvalues)[::-1]  # Sort indices in descending order
    sorted_eigenvalues = eigenvalues[sorted_indices]
    sorted_eigenvectors = eigenvectors[:, sorted_indices]
    
    # Step 5: Select the top `n_components` eigenvectors
    top_eigenvectors = sorted_eigenvectors[:, :n_components]
    
    # Step 6: Project data onto the new basis (principal components)
    transformed_data = np.dot(centered_data, top_eigenvectors)

    # Return the transformed data, components, and explained variance
    explained_variance = sorted_eigenvalues[:n_components] / np.sum(sorted_eigenvalues)
    return transformed_data, top_eigenvectors, explained_variance

# Example Usage
if __name__ == "__main__":
    # Example data (e.g., 4 data points with 3 features)
    data = np.array([[2.5, 3.5, 1.5],
                     [3.0, 4.0, 2.0],
                     [3.5, 4.5, 2.5],
                     [4.0, 5.0, 3.0]])

    # Perform PCA to reduce to 2 components
    transformed_data, components, explained_variance = pca(data, n_components=2)

    # Print results
    print("Transformed Data (Principal Components):")
    print(transformed_data)

    print("\nPrincipal Components (Eigenvectors):")
    print(components)

    print("\nExplained Variance by Each Component:")
    print(explained_variance)
