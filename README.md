
# Fashion-MNIST Clustering & Dimensionality Reduction

## Overview
This project focuses on **clustering and dimensionality reduction** techniques applied to the **Fashion-MNIST** dataset, which consists of **70,000 images** of clothing and footwear divided into **10 categories**.

## Features
- **Dimensionality Reduction Techniques:**
  - **PCA (Principal Component Analysis)**
  - **SAE (Stacked Autoencoder)**
  - **UMAP (Uniform Manifold Approximation and Projection)**

- **Clustering Algorithms:**
  - **MiniBatch K-Means**
  - **DBSCAN**
  - **Agglomerative Clustering (Ward, Average, Complete)**

- **Evaluation Metrics:**
  - **Silhouette Score**
  - **Calinski-Harabasz Index**
  - **Davies-Bouldin Index**
  - **Dunn Index**

- **Performance Evaluation:** 
  - Visualizing **2D and 3D projections** of the dataset.
  - Comparing different clustering models on different dimensionality reduction techniques.
  - Analyzing class separability in the reduced feature space.

## Dataset
The **Fashion-MNIST** dataset contains **70,000 grayscale images (28x28 pixels)** categorized into **10 classes**:
- **T-shirt/top**
- **Trouser**
- **Pullover**
- **Dress**
- **Coat**
- **Sandal**
- **Shirt**
- **Sneaker**
- **Bag**
- **Ankle boot**

## Installation
Install the necessary dependencies using:
```bash
pip install tensorflow numpy pandas scikit-learn matplotlib seaborn umap-learn
