# -*- coding: utf-8 -*-
"""assignment2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1XiBJge9f_I7VvHPnv7QstO86DECeiMYG
"""

#Assignment 2
#Clustering problem
#fashion_mnist dataset

#Μηχανική Μάθηση 2024 (εξάμηνο 7ο)
#Καθηγητής: Ευτύχιος Πρωτοπαπαδάκης
#Φοιτητες: iis22127 Δαδακίδης Γιώργος
#          iis22125 Παναγιώτης Μώκος

# Import necessary libraries
import tensorflow as tf
from tensorflow.keras.datasets import fashion_mnist
import numpy as np
import matplotlib.pyplot as plt

# Load the dataset
(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

# Normalize pixel values to the range [0, 1]
train_images = train_images / 255.0
test_images = test_images / 255.0

# Split the training data into training and validation sets
#Devide 80% training and 20% validation
validation_split = 0.2
val_size = int(len(train_images) * validation_split)

val_images = train_images[:val_size]
val_labels = train_labels[:val_size]

train_images = train_images[val_size:]
train_labels = train_labels[val_size:]

print(f"Training set size: {train_images.shape[0]}")
print(f"Validation set size: {val_images.shape[0]}")
print(f"Test set size: {test_images.shape[0]}")

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import numpy as np
import matplotlib.pyplot as plt

# Step 1: Flatten the images
flat_train_images = train_images.reshape(train_images.shape[0], -1)
flat_test_images = test_images.reshape(test_images.shape[0], -1)

# Step 2: Standardize the data
scaler = StandardScaler()
flat_train_images_scaled = scaler.fit_transform(flat_train_images)
flat_test_images_scaled = scaler.transform(flat_test_images)

# Step 3: Apply PCA
# Retain 95% of the variance
pca = PCA(n_components=0.95, random_state=42)
flat_train_images_pca = pca.fit_transform(flat_train_images_scaled)
flat_test_images_pca = pca.transform(flat_test_images_scaled)

# Print results
print(f"Original number of features: {flat_train_images.shape[1]}")
print(f"Reduced number of features: {flat_train_images_pca.shape[1]}")

# Step 4: Visualize variance explained
plt.figure(figsize=(10, 6))
plt.plot(np.cumsum(pca.explained_variance_ratio_), marker='o')
plt.xlabel('Number of Components')
plt.ylabel('Cumulative Explained Variance')
plt.title('PCA - Cumulative Explained Variance')
plt.grid()
plt.show()

# --------------------------------------------------
# Cell B: Reconstruct & visualize images from PCA
# --------------------------------------------------
import matplotlib.pyplot as plt

n_images = 10

# Pick a small batch from the TEST set (or train set, if you prefer)
sample_images = test_images[:n_images]           # shape = (n_images, 28, 28)
sample_images_flat = flat_test_images[:n_images] # shape = (n_images, 784)

# 1) Transform to PCA-space
encoded = pca.transform(sample_images_flat)           # shape = (n_images, n_components)

# 2) Reconstruct by inverse transform
reconstructed = pca.inverse_transform(encoded)        # shape = (n_images, 784)
reconstructed = reconstructed.reshape(n_images, 28, 28)

# Plot side by side: original (top) vs. reconstructed (bottom)
plt.figure(figsize=(2 * n_images, 4))
for i in range(n_images):
    # Original image
    ax = plt.subplot(2, n_images, i + 1)
    plt.imshow(sample_images[i], cmap='gray')
    plt.title("Original")
    plt.axis("off")

    # Reconstructed image
    ax = plt.subplot(2, n_images, i + 1 + n_images)
    plt.imshow(reconstructed[i], cmap='gray')
    plt.title("Reconstructed")
    plt.axis("off")

plt.tight_layout()
plt.show()

import time
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
import matplotlib.pyplot as plt
import numpy as np

# Assume train_images and train_labels are already loaded and normalized
flat_train_images = train_images.reshape(train_images.shape[0], -1)  # Flatten images

# Function to calculate clustering performance
def calculate_cluster_performance(data, labels, n_clusters=10):
    # Perform clustering using KMeans
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    cluster_labels = kmeans.fit_predict(data)

    # Calculate performance metrics
    silhouette = silhouette_score(data, cluster_labels)
    ch_score = calinski_harabasz_score(data, cluster_labels)
    db_score = davies_bouldin_score(data, cluster_labels)

    return silhouette, ch_score, db_score

# Function to visualize 2D PCA projection
def plot_2d(data, labels, title):
    plt.figure(figsize=(8, 6))
    scatter = plt.scatter(data[:, 0], data[:, 1], c=labels, cmap="viridis", s=5, alpha=0.7)
    plt.colorbar(scatter)
    plt.title(title)
    plt.xlabel("Principal Component 1")
    plt.ylabel("Principal Component 2")
    plt.grid()
    plt.show()

# Function to visualize 3D PCA projection
def plot_3d(data, labels, title):
    from mpl_toolkits.mplot3d import Axes3D
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    scatter = ax.scatter(data[:, 0], data[:, 1], data[:, 2], c=labels, cmap="viridis", s=5, alpha=0.7)
    fig.colorbar(scatter)
    ax.set_title(title)
    ax.set_xlabel("PC1")
    ax.set_ylabel("PC2")
    ax.set_zlabel("PC3")
    plt.show()

# Step 1: PCA 2D Projection
print("=== PCA 2D ===")
start_time_2d = time.time()
pca_2d = PCA(n_components=2)
X_pca_2d = pca_2d.fit_transform(flat_train_images)
end_time_2d = time.time()
pca_time_2d = end_time_2d - start_time_2d

# Calculate clustering performance for 2D
silhouette_2d, ch_score_2d, db_score_2d = calculate_cluster_performance(X_pca_2d, train_labels)
print(f"Time taken (PCA 2D): {pca_time_2d:.4f} seconds")
print(f"Silhouette Score (PCA 2D): {silhouette_2d:.2f}")
print(f"Calinski-Harabasz Index (PCA 2D): {ch_score_2d:.2f}")
print(f"Davies-Bouldin Index (PCA 2D): {db_score_2d:.2f}")

# Visualize PCA 2D
plot_2d(X_pca_2d, train_labels, "PCA 2D Projection")

# Step 2: PCA 3D Projection
print("\n=== PCA 3D ===")
start_time_3d = time.time()
pca_3d = PCA(n_components=3)
X_pca_3d = pca_3d.fit_transform(flat_train_images)
end_time_3d = time.time()
pca_time_3d = end_time_3d - start_time_3d

# Calculate clustering performance for 3D
silhouette_3d, ch_score_3d, db_score_3d = calculate_cluster_performance(X_pca_3d, train_labels)
print(f"Time taken (PCA 3D): {pca_time_3d:.4f} seconds")
print(f"Silhouette Score (PCA 3D): {silhouette_3d:.2f}")
print(f"Calinski-Harabasz Index (PCA 3D): {ch_score_3d:.2f}")
print(f"Davies-Bouldin Index (PCA 3D): {db_score_3d:.2f}")

# Visualize PCA 3D
plot_3d(X_pca_3d, train_labels, "PCA 3D Projection")

#Visualize the Dataset (random)
# Class names for Fashion-MNIST
class_names = [
    "T-shirt/top", "Trouser", "Pullover", "Dress", "Coat",
    "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot"
]

# Display random images from the dataset
def plot_sample_images(images, labels, class_names, count=9):
    plt.figure(figsize=(10, 10))
    for i in range(count):
        plt.subplot(3, 3, i + 1)
        plt.imshow(images[i], cmap="gray")
        plt.title(class_names[labels[i]])
        plt.axis("off")
    plt.show()

# Show images from the training set
plot_sample_images(train_images, train_labels, class_names)

#Random dataset visualization
import matplotlib.pyplot as plt

import numpy as np

# Class names for Fashion-MNIST
class_names = [
    "T-shirt/top", "Trouser", "Pullover", "Dress", "Coat",
    "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot"
]

# Function to plot 30 random images from the dataset
def plot_random_images(images, labels, class_names):
    plt.figure(figsize=(15, 10))
    indices = np.random.choice(range(len(images)), 30, replace=False)  # Randomly select 30 images
    for i, idx in enumerate(indices):
        plt.subplot(5, 6, i + 1)  # 5 rows, 6 columns
        plt.imshow(images[idx], cmap="gray")
        plt.title(class_names[labels[idx]])
        plt.axis("off")
    plt.tight_layout()
    plt.show()

# Plot 30 random images from the training set
plot_random_images(train_images, train_labels, class_names)

# Function to calculate Dunn Index
import time
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import MiniBatchKMeans, DBSCAN, AgglomerativeClustering
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
from scipy.spatial.distance import cdist
import numpy as np
import gc
def calculate_dunn_index(data, cluster_labels):
    clusters = np.unique(cluster_labels)
    intra_cluster_distances = []
    inter_cluster_distances = []

    for cluster in clusters:
        cluster_points = data[cluster_labels == cluster]
        if len(cluster_points) > 1:
            intra_distances = cdist(cluster_points, cluster_points, metric='euclidean')
            intra_cluster_distances.append(np.max(intra_distances))
        else:
            intra_cluster_distances.append(0)

    for i in range(len(clusters)):
        for j in range(i + 1, len(clusters)):
            cluster_i_points = data[cluster_labels == clusters[i]]
            cluster_j_points = data[cluster_labels == clusters[j]]
            inter_cluster_distances.append(np.min(cdist(cluster_i_points, cluster_j_points, metric='euclidean')))

    return np.min(inter_cluster_distances) / np.max(intra_cluster_distances)

# Function to evaluate clustering performance
def evaluate_clustering(data, labels, cluster_labels):
    silhouette = silhouette_score(data, cluster_labels)
    ch_score = calinski_harabasz_score(data, cluster_labels)
    db_score = davies_bouldin_score(data, cluster_labels)
    dunn = calculate_dunn_index(data, cluster_labels)
    return silhouette, ch_score, db_score, dunn
# Function to visualize clustering in 2D
def plot_clustering_2d(data, cluster_labels, title):
    plt.figure(figsize=(8, 6))
    scatter = plt.scatter(data[:, 0], data[:, 1], c=cluster_labels, cmap="viridis", s=5, alpha=0.7)
    plt.colorbar(scatter)
    plt.title(title)
    plt.xlabel("Principal Component 1")
    plt.ylabel("Principal Component 2")
    plt.grid()
    plt.show()

# Import MiniBatchKMeans
from sklearn.cluster import MiniBatchKMeans
# Subsample the test dataset
sample_size = 1000  # Adjust as needed
sampled_indices = np.random.choice(flat_test_images.shape[0], sample_size, replace=False)
flat_test_images_sampled = flat_test_images[sampled_indices]
test_labels_sampled = test_labels[sampled_indices]

# Apply PCA on the sampled test data
pca_2d = PCA(n_components=2)
X_pca_2d_sampled = pca_2d.fit_transform(flat_test_images_sampled)



# MiniBatch KMeans
print("\n=== MiniBatch KMeans ===")
kmeans = MiniBatchKMeans(n_clusters=10, random_state=42)
kmeans_labels = kmeans.fit_predict(X_pca_2d_sampled)
silhouette, ch_score, db_score, dunn = evaluate_clustering(X_pca_2d_sampled, test_labels_sampled, kmeans_labels)
print("MiniBatch KMeans Metrics:")
print(f"Silhouette: {silhouette}\nCH: {ch_score}\nDB: {db_score}\nDunn: {dunn}\n")
plot_clustering_2d(X_pca_2d_sampled, kmeans_labels, "MiniBatch KMeans on PCA 2D")

# Clear memory
del kmeans, kmeans_labels
gc.collect()

# DBSCAN PCA
from sklearn.cluster import DBSCAN

print("\n=== DBSCAN ===")
dbscan = DBSCAN(eps=0.5, min_samples=10)
dbscan_labels = dbscan.fit_predict(X_pca_2d_sampled)
silhouette, ch_score, db_score, dunn = evaluate_clustering(X_pca_2d_sampled, test_labels_sampled, dbscan_labels)

if silhouette is not None:
    print("DBSCAN Metrics:")
    print(f"Silhouette: {silhouette}\nCH: {ch_score}\nDB: {db_score}\nDunn: {dunn}\n")
    plot_clustering_2d(X_pca_2d_sampled, dbscan_labels, "DBSCAN on PCA 2D")
else:
    print("DBSCAN did not produce valid clusters.")

# Clear memory
del dbscan, dbscan_labels
gc.collect()

# Agglomerative Clustering PCA (WARD)
from sklearn.cluster import AgglomerativeClustering

print("\n=== Agglomerative Clustering ===")
agg = AgglomerativeClustering(n_clusters=10, linkage='ward')
agg_labels = agg.fit_predict(X_pca_2d_sampled)
silhouette, ch_score, db_score, dunn = evaluate_clustering(X_pca_2d_sampled, test_labels_sampled, agg_labels)
print("Agglomerative Clustering Metrics:")
print(f"Silhouette: {silhouette}\nCH: {ch_score}\nDB: {db_score}\nDunn: {dunn}\n")
plot_clustering_2d(X_pca_2d_sampled, agg_labels, "Agglomerative Clustering on PCA 2D (WARD)")

# Clear memory
del agg, agg_labels
gc.collect()

# Agglomerative Clustering PCA (AVERAGE)
from sklearn.cluster import AgglomerativeClustering

print("\n=== Agglomerative Clustering ===")
agg_avg = AgglomerativeClustering(n_clusters=10, linkage='average')
agg_labels_avg = agg_avg.fit_predict(X_pca_2d_sampled)
silhouette, ch_score, db_score, dunn = evaluate_clustering(X_pca_2d_sampled, test_labels_sampled, agg_labels_avg)
print("Agglomerative Clustering Metrics:")
print(f"Silhouette: {silhouette}\nCH: {ch_score}\nDB: {db_score}\nDunn: {dunn}\n")
plot_clustering_2d(X_pca_2d_sampled, agg_labels_avg, "Agglomerative Clustering on PCA 2D (AVERAGE)")

# Clear memory
del agg_avg, agg_labels_avg
gc.collect()

# Agglomerative Clustering PCA (COMPLETE)
from sklearn.cluster import AgglomerativeClustering

print("\n=== Agglomerative Clustering ===")
agg_cmp = AgglomerativeClustering(n_clusters=10, linkage='complete')
agg_labels_cmp = agg_cmp.fit_predict(X_pca_2d_sampled)
silhouette, ch_score, db_score, dunn = evaluate_clustering(X_pca_2d_sampled, test_labels_sampled, agg_labels_cmp)
print("Agglomerative Clustering Metrics:")
print(f"Silhouette: {silhouette}\nCH: {ch_score}\nDB: {db_score}\nDunn: {dunn}\n")
plot_clustering_2d(X_pca_2d_sampled, agg_labels_cmp, "Agglomerative Clustering on PCA 2D (COMPLETE)")

# Clear memory
del agg_cmp, agg_labels_cmp
gc.collect()

#Umap
try:
    import umap
except ImportError:
    !pip install umap-learn
    import umap





# Function to evaluate clustering performance
def evaluate_clustering(data, labels, cluster_labels):
    n_clusters = len(np.unique(cluster_labels))

    if n_clusters < 2:
        print(f"Insufficient clusters for evaluation: {n_clusters}")
        return None, None, None, None

    silhouette = silhouette_score(data, cluster_labels)
    ch_score = calinski_harabasz_score(data, cluster_labels)
    db_score = davies_bouldin_score(data, cluster_labels)
    dunn = calculate_dunn_index(data, cluster_labels)
    return silhouette, ch_score, db_score, dunn

# Function to plot clustering results in 2D
def plot_clustering_2d(data, cluster_labels, title):
    plt.figure(figsize=(8, 6))
    scatter = plt.scatter(data[:, 0], data[:, 1], c=cluster_labels, cmap="viridis", s=5, alpha=0.7)
    plt.colorbar(scatter)
    plt.title(title)
    plt.xlabel("UMAP Dimension 1")
    plt.ylabel("UMAP Dimension 2")
    plt.grid()
    plt.show()

# Apply UMAP to the test data
print("\n=== UMAP Dimensionality Reduction ===")
start_time_umap = time.time()

umap_reducer = umap.UMAP(n_components=2, random_state=42)
train_umap = umap_reducer.fit_transform(flat_train_images)
test_umap = umap_reducer.transform(flat_test_images)

end_time_umap = time.time()
umap_time = end_time_umap - start_time_umap
print(f"UMAP Training Time: {umap_time:.4f} seconds")

# Visualize UMAP results
plt.scatter(train_umap[:, 0], train_umap[:, 1], c=train_labels, cmap="viridis", s=5, alpha=0.7)
plt.title("UMAP - 2D Projection")
plt.xlabel("UMAP Dimension 1")
plt.ylabel("UMAP Dimension 2")
plt.colorbar()
plt.show()

# Initialize a results DataFrame
results_df = pd.DataFrame(columns=[
    "DimRedTechnique", "ClusteringAlgorithm", "DimRedTrainTime",
    "ClustExecTime", "NumClusters", "CalinskiHarabasz",
    "DaviesBouldin", "Silhouette", "DunnIndex"
])

# Clustering with MiniBatch KMeans
print("\n=== MiniBatch KMeans on UMAP ===")
kmeans = MiniBatchKMeans(n_clusters=10, random_state=42)
start_clustering = time.time()
kmeans_labels = kmeans.fit_predict(test_umap)
end_clustering = time.time()

silhouette, ch_score, db_score, dunn = evaluate_clustering(test_umap, test_labels, kmeans_labels)
print(f"Silhouette: {silhouette}\nCH: {ch_score}\nDB: {db_score}\nDunn: {dunn}\n")
plot_clustering_2d(test_umap, kmeans_labels, "MiniBatch KMeans on UMAP")

new_row = {
    "DimRedTechnique": "UMAP",
    "ClusteringAlgorithm": "MiniBatch KMeans",
    "DimRedTrainTime": umap_time,
    "ClustExecTime": end_clustering - start_clustering,
    "NumClusters": len(np.unique(kmeans_labels)),
    "CalinskiHarabasz": ch_score,
    "DaviesBouldin": db_score,
    "Silhouette": silhouette,
    "DunnIndex": dunn
}
results_df = pd.concat([results_df, pd.DataFrame([new_row])], ignore_index=True)


# Clustering with DBSCAN
print("\n=== DBSCAN on UMAP ===")
dbscan = DBSCAN(eps=0.5, min_samples=10)
start_clustering = time.time()
dbscan_labels = dbscan.fit_predict(test_umap)
end_clustering = time.time()

if len(np.unique(dbscan_labels)) > 1:
    silhouette, ch_score, db_score, dunn = evaluate_clustering(test_umap, test_labels, dbscan_labels)
    print(f"Silhouette: {silhouette}\nCH: {ch_score}\nDB: {db_score}\nDunn: {dunn}\n")
    plot_clustering_2d(test_umap, dbscan_labels, "DBSCAN on UMAP")
else:
    print("DBSCAN did not produce valid clusters.")

new_row = {
    "DimRedTechnique": "UMAP",
    "ClusteringAlgorithm": "DB Scan",
    "DimRedTrainTime": umap_time,
    "ClustExecTime": end_clustering - start_clustering,
    "NumClusters": len(np.unique(kmeans_labels)),
    "CalinskiHarabasz": ch_score,
    "DaviesBouldin": db_score,
    "Silhouette": silhouette,
    "DunnIndex": dunn
}
results_df = pd.concat([results_df, pd.DataFrame([new_row])], ignore_index=True)


# Clustering with Agglomerative Clustering
print("\n=== Agglomerative Clustering on UMAP ===")
agg = AgglomerativeClustering(n_clusters=10, linkage='ward')
start_clustering = time.time()
agg_labels = agg.fit_predict(test_umap)
end_clustering = time.time()

silhouette, ch_score, db_score, dunn = evaluate_clustering(test_umap, test_labels, agg_labels)
print(f"Silhouette: {silhouette}\nCH: {ch_score}\nDB: {db_score}\nDunn: {dunn}\n")
plot_clustering_2d(test_umap, agg_labels, "Agglomerative Clustering on UMAP")

new_row = {
    "DimRedTechnique": "UMAP",
    "ClusteringAlgorithm": "Agglomerative Clustering",
    "DimRedTrainTime": umap_time,
    "ClustExecTime": end_clustering - start_clustering,
    "NumClusters": len(np.unique(kmeans_labels)),
    "CalinskiHarabasz": ch_score,
    "DaviesBouldin": db_score,
    "Silhouette": silhouette,
    "DunnIndex": dunn
}
results_df = pd.concat([results_df, pd.DataFrame([new_row])], ignore_index=True)




# Clear memory
del train_umap, test_umap, kmeans, dbscan, agg, kmeans_labels, dbscan_labels, agg_labels
gc.collect()

#SAE
from tensorflow.keras import layers, models
from tensorflow.keras.callbacks import EarlyStopping
import numpy as np

# Flatten the images
flat_train_images = train_images.reshape(train_images.shape[0], -1)
flat_val_images = val_images.reshape(val_images.shape[0], -1)
flat_test_images = test_images.reshape(test_images.shape[0], -1)

# Define SAE architecture
input_dim = flat_train_images.shape[1]
encoding_dim = 64  # Adjust based on required dimensionality

# Encoder
input_layer = layers.Input(shape=(input_dim,))
encoded = layers.Dense(128, activation='relu')(input_layer)
encoded = layers.Dense(encoding_dim, activation='relu')(encoded)

# Decoder
decoded = layers.Dense(128, activation='relu')(encoded)
decoded = layers.Dense(input_dim, activation='sigmoid')(decoded)

# SAE Model
sae = models.Model(input_layer, decoded)

# Compile SAE
sae.compile(optimizer='adam', loss='mse')

# Train SAE with validation data
early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
history = sae.fit(
    flat_train_images, flat_train_images,
    epochs=50, batch_size=256,
    validation_data=(flat_val_images, flat_val_images),
    callbacks=[early_stopping]
)

# ====================================================
# Visualize Reconstructed Images from the SAE
# ====================================================
import matplotlib.pyplot as plt

# Select how many images you want to display
n_images = 10

# Take a small batch from the test set
test_sample = test_images[:n_images]        # shape = (n_images, 28, 28)
test_sample_flat = flat_test_images[:n_images]  # shape = (n_images, 784)

# Pass the flattened images through the autoencoder
reconstructed = sae.predict(test_sample_flat)   # shape = (n_images, 784)

# Reshape the reconstructed images back to 28x28
reconstructed = reconstructed.reshape((n_images, 28, 28))

# Plot side-by-side: originals (top row) vs. reconstructions (bottom row)
plt.figure(figsize=(2 * n_images, 4))
for i in range(n_images):
    # Original image
    ax = plt.subplot(2, n_images, i + 1)
    plt.imshow(test_sample[i], cmap='gray')
    plt.title("Original")
    plt.axis("off")

    # Reconstructed image
    ax = plt.subplot(2, n_images, i + 1 + n_images)
    plt.imshow(reconstructed[i], cmap='gray')
    plt.title("Reconstructed")
    plt.axis("off")

plt.tight_layout()
plt.show()




# Extract the encoder
encoder = models.Model(input_layer, encoded)

# ====================================================
# Visualize Reconstructed Images from the SAE
# ====================================================
import matplotlib.pyplot as plt

# Select how many images you want to display
n_images = 10

# Take a small batch from the test set
test_sample = test_images[:n_images]        # shape = (n_images, 28, 28)
test_sample_flat = flat_test_images[:n_images]  # shape = (n_images, 784)

# Pass the flattened images through the autoencoder
reconstructed = sae.predict(test_sample_flat)   # shape = (n_images, 784)

# Reshape the reconstructed images back to 28x28
reconstructed = reconstructed.reshape((n_images, 28, 28))

# Plot side-by-side: originals (top row) vs. reconstructions (bottom row)
plt.figure(figsize=(2 * n_images, 4))
for i in range(n_images):
    # Original image
    ax = plt.subplot(2, n_images, i + 1)
    plt.imshow(test_sample[i], cmap='gray')
    plt.title("Original")
    plt.axis("off")

    # Reconstructed image
    ax = plt.subplot(2, n_images, i + 1 + n_images)
    plt.imshow(reconstructed[i], cmap='gray')
    plt.title("Reconstructed")
    plt.axis("off")

plt.tight_layout()
plt.show()

# Reduce dimensions of train, validation, and test sets
train_encoded = encoder.predict(flat_train_images)
val_encoded = encoder.predict(flat_val_images)
test_encoded = encoder.predict(flat_test_images)

print(f"Original Dimensionality: {flat_train_images.shape[1]}")
print(f"Reduced Dimensionality: {train_encoded.shape[1]}")

from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
from scipy.spatial.distance import cdist
import numpy as np



# MiniBatch KMeans
print("\n=== MiniBatch KMeans on SAE Encoded Data ===")
kmeans = MiniBatchKMeans(n_clusters=10, random_state=42)
kmeans_labels = kmeans.fit_predict(test_encoded)
silhouette, ch_score, db_score, dunn = evaluate_clustering(test_encoded, test_labels, kmeans_labels)
print(f"Silhouette: {silhouette}\nCH: {ch_score}\nDB: {db_score}\nDunn: {dunn}")

# DBSCAN
print("\n=== DBSCAN on SAE Encoded Data ===")
dbscan = DBSCAN(eps=0.5, min_samples=10)
dbscan_labels = dbscan.fit_predict(test_encoded)
if len(np.unique(dbscan_labels)) > 1:
    silhouette, ch_score, db_score, dunn = evaluate_clustering(test_encoded, test_labels, dbscan_labels)
    print(f"Silhouette: {silhouette}\nCH: {ch_score}\nDB: {db_score}\nDunn: {dunn}")
else:
    print("DBSCAN did not produce valid clusters.")

# Agglomerative Clustering
print("\n=== Agglomerative Clustering on SAE Encoded Data ===")
agg = AgglomerativeClustering(n_clusters=10, linkage='ward')
agg_labels = agg.fit_predict(test_encoded)
silhouette, ch_score, db_score, dunn = evaluate_clustering(test_encoded, test_labels, agg_labels)
print(f"Silhouette: {silhouette}\nCH: {ch_score}\nDB: {db_score}\nDunn: {dunn}")

from sklearn.metrics import pairwise_distances
import numpy as np

distances = pairwise_distances(test_encoded, metric='euclidean')
print(f"Mean Distance: {np.mean(distances):.4f}")
print(f"Max Distance: {np.max(distances):.4f}")
print(f"Min Distance: {np.min(distances):.4f}")
plt.scatter(test_encoded[:, 0], test_encoded[:, 1], s=5, alpha=0.7)
plt.title("Encoded Data (2D)")
plt.xlabel("Feature 1")
plt.ylabel("Feature 2")
plt.show()

# Visualize clusters in 2D (optional if encoding is 2D)
plot_clustering_2d(test_encoded, kmeans_labels, "MiniBatch KMeans on SAE Encoded Data")
plot_clustering_2d(test_encoded, dbscan_labels, "DBSCAN on SAE Encoded Data")
plot_clustering_2d(test_encoded, agg_labels, "Agglomerative Clustering on SAE Encoded Data")

import pandas as pd
import time
from sklearn.cluster import MiniBatchKMeans, DBSCAN, AgglomerativeClustering

# Initialize a DataFrame to store results
results_df = pd.DataFrame(columns=[
    "DimRedTechnique", "ClusteringAlgorithm", "DimRedTrainTime",
    "ClustExecTime", "NumClusters", "CalinskiHarabasz",
    "DaviesBouldin", "Silhouette", "DunnIndex"
])

# Function to add results to the DataFrame
def add_results_to_dataframe(results_df, technique, algo, dim_time, clust_time, num_clusters, ch, db, silhouette, dunn):
    new_row = {
        "DimRedTechnique": technique,
        "ClusteringAlgorithm": algo,
        "DimRedTrainTime": dim_time,
        "ClustExecTime": clust_time,
        "NumClusters": num_clusters,
        "CalinskiHarabasz": ch,
        "DaviesBouldin": db,
        "Silhouette": silhouette,
        "DunnIndex": dunn
    }
    return pd.concat([results_df, pd.DataFrame([new_row])], ignore_index=True)

# Common logic for clustering evaluation
def run_clustering_and_store(data, technique_name, dim_time):
    global results_df

    # MiniBatch KMeans
    start_clustering = time.time()
    kmeans_labels = MiniBatchKMeans(n_clusters=10, random_state=42).fit_predict(data)
    end_clustering = time.time()
    silhouette, ch_score, db_score, dunn = evaluate_clustering(data, test_labels, kmeans_labels)
    results_df = add_results_to_dataframe(
        results_df, technique_name, "MiniBatch KMeans", dim_time, end_clustering - start_clustering,
        len(np.unique(kmeans_labels)), ch_score, db_score, silhouette, dunn
    )

    # DBSCAN
    start_clustering = time.time()
    dbscan_labels = DBSCAN(eps=0.5, min_samples=10).fit_predict(data)
    end_clustering = time.time()
    if len(np.unique(dbscan_labels)) > 1:
        silhouette, ch_score, db_score, dunn = evaluate_clustering(data, test_labels, dbscan_labels)
    else:
        silhouette, ch_score, db_score, dunn = None, None, None, None
    results_df = add_results_to_dataframe(
        results_df, technique_name, "DBSCAN", dim_time, end_clustering - start_clustering,
        len(np.unique(dbscan_labels)), ch_score, db_score, silhouette, dunn
    )

    # Agglomerative Clustering
    start_clustering = time.time()
    agg_labels = AgglomerativeClustering(n_clusters=10, linkage='ward').fit_predict(data)
    end_clustering = time.time()
    silhouette, ch_score, db_score, dunn = evaluate_clustering(data, test_labels, agg_labels)
    results_df = add_results_to_dataframe(
        results_df, technique_name, "Agglomerative Clustering", dim_time, end_clustering - start_clustering,
        len(np.unique(agg_labels)), ch_score, db_score, silhouette, dunn
    )
 # Agglomerative Clustering AVERAGE
    start_clustering = time.time()
    agg_labels = AgglomerativeClustering(n_clusters=10, linkage='average').fit_predict(data)
    end_clustering = time.time()
    silhouette, ch_score, db_score, dunn = evaluate_clustering(data, test_labels, agg_labels)
    results_df = add_results_to_dataframe(
        results_df, technique_name, "Agglomerative Clustering WITH AVERAGE", dim_time, end_clustering - start_clustering,
        len(np.unique(agg_labels)), ch_score, db_score, silhouette, dunn
    )
     # Agglomerative Clustering COMPLETE
    start_clustering = time.time()
    agg_labels = AgglomerativeClustering(n_clusters=10, linkage='complete').fit_predict(data)
    end_clustering = time.time()
    silhouette, ch_score, db_score, dunn = evaluate_clustering(data, test_labels, agg_labels)
    results_df = add_results_to_dataframe(
        results_df, technique_name, "Agglomerative Clustering WITH complete", dim_time, end_clustering - start_clustering,
        len(np.unique(agg_labels)), ch_score, db_score, silhouette, dunn
    )
# PCA Results
print("\n=== PCA Dimensionality Reduction ===")
start_time_pca = time.time()
pca = PCA(n_components=2)
train_pca = pca.fit_transform(flat_train_images)
test_pca = pca.transform(flat_test_images)
end_time_pca = time.time()
pca_time = end_time_pca - start_time_pca

run_clustering_and_store(test_pca, "PCA", pca_time)

# SAE Results
print("\n=== SAE Dimensionality Reduction ===")
start_time_sae = time.time()
train_encoded = encoder.predict(flat_train_images)
test_encoded = encoder.predict(flat_test_images)
end_time_sae = time.time()
sae_time = end_time_sae - start_time_sae

run_clustering_and_store(test_encoded, "SAE", sae_time)

# UMAP Results
print("\n=== UMAP Dimensionality Reduction ===")
start_time_umap = time.time()
umap_reducer = umap.UMAP(n_components=2, random_state=42)
train_umap = umap_reducer.fit_transform(flat_train_images)
test_umap = umap_reducer.transform(flat_test_images)
end_time_umap = time.time()
umap_time = end_time_umap - start_time_umap

run_clustering_and_store(test_umap, "UMAP", umap_time)

# Display the consolidated results
print("\n=== Final Results DataFrame ===")
print(results_df)

# Save to CSV
results_df.to_csv("clustering_results.csv", index=False)
print("Results saved to clustering_results.csv")

from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Ensure test_encoded is already computed by the SAE encoder
# test_encoded = encoder.predict(flat_test_images)

# 2D Visualization using PCA
def plot_latent_space_2d(data, labels, title):
    plt.figure(figsize=(8, 6))
    scatter = plt.scatter(data[:, 0], data[:, 1], c=labels, cmap="viridis", s=5, alpha=0.7)
    plt.colorbar(scatter, label="Class")
    plt.title(title)
    plt.xlabel("Latent Dimension 1")
    plt.ylabel("Latent Dimension 2")
    plt.grid()
    plt.show()

# 3D Visualization using PCA
def plot_latent_space_3d(data, labels, title):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    scatter = ax.scatter(data[:, 0], data[:, 1], data[:, 2], c=labels, cmap="viridis", s=5, alpha=0.7)
    fig.colorbar(scatter, label="Class")
    ax.set_title(title)
    ax.set_xlabel("Latent Dimension 1")
    ax.set_ylabel("Latent Dimension 2")
    ax.set_zlabel("Latent Dimension 3")
    plt.show()

# Apply PCA to reduce SAE latent space to 2D and 3D
pca_2d = PCA(n_components=2)
latent_2d = pca_2d.fit_transform(test_encoded)

pca_3d = PCA(n_components=3)
latent_3d = pca_3d.fit_transform(test_encoded)

# Visualize in 2D
plot_latent_space_2d(latent_2d, test_labels, "SAE Latent Space (2D PCA)")

# Visualize in 3D
plot_latent_space_3d(latent_3d, test_labels, "SAE Latent Space (3D PCA)")

# Optional: Visualization using t-SNE
def plot_latent_space_tsne(data, labels, title):
    tsne_2d = TSNE(n_components=2, random_state=42)
    latent_tsne_2d = tsne_2d.fit_transform(data)
    plot_latent_space_2d(latent_tsne_2d, labels, title)

plot_latent_space_tsne(test_encoded, test_labels, "SAE Latent Space (2D t-SNE)")

import numpy as np
import matplotlib.pyplot as plt

# Select four classes for demonstration
chosen_classes = [0, 1, 8, 9]  # Example: T-shirt, Trouser, Bag, Ankle Boot
class_names = [
    "T-shirt/top", "Trouser", "Pullover", "Dress", "Coat",
    "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot"
]

# Function to display clustering results for a class
def show_class_clustering_results(data, labels, cluster_labels, class_id, class_name, num_samples=5):
    indices = np.where(labels == class_id)[0]
    sampled_indices = np.random.choice(indices, num_samples, replace=False)

    plt.figure(figsize=(15, 5))
    for i, idx in enumerate(sampled_indices):
        plt.subplot(1, num_samples, i + 1)
        plt.imshow(test_images[idx], cmap="gray")
        plt.title(f"Class: {class_name}\nCluster: {cluster_labels[idx]}")
        plt.axis("off")
    plt.suptitle(f"Clustering Results for Class: {class_name}")
    plt.show()

# Example: Using UMAP + MiniBatch KMeans for clustering
umap_reducer = umap.UMAP(n_components=2, random_state=42)
test_umap = umap_reducer.fit_transform(flat_test_images)

kmeans = MiniBatchKMeans(n_clusters=10, random_state=42)
cluster_labels = kmeans.fit_predict(test_umap)

# Show clustering results for chosen classes
for class_id in chosen_classes:
    show_class_clustering_results(
        test_umap, test_labels, cluster_labels, class_id, class_names[class_id]
    )