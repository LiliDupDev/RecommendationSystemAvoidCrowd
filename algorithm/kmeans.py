import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


# Currently, this dataset is too short for cluster algorithms but the idea is to let it ready for bigger datasets.
# ** means is a parameter to be changed with different datasets

# Load Data
f_name = "../Data/store_data_ext.csv"   # **
df_stores = pd.read_csv(f_name)


store_coordinates = df_stores[['X','Y']]
stores = df_stores[['X','Y','Name','Capacity','Congestion']]          # **



# Througth elbow method we determined an estimated number of clusters
distortions = []
K = range(1,5)    # **
for k in K:
    kmeansModel = KMeans(n_clusters=k)
    kmeansModel = kmeansModel.fit(store_coordinates)
    distortions.append(kmeansModel.inertia_)

fig, ax = plt.subplots(figsize=(12, 8))
plt.plot(K, distortions, marker='o')
plt.xlabel('k')
plt.ylabel('Distortions')
plt.title('Elbow Method For Optimal k')
plt.savefig('elbow.png')
# plt.show()



# silhouette_score to evaluate dissimilarity
sil = []
kmax = 5  # ** No. Clusters to evaluate with score

# dissimilarity would not be defined for a single cluster, thus, minimum number of clusters should be 2
for k in range(2, kmax + 1):
    kmeans = KMeans(n_clusters=k).fit(store_coordinates)
    labels = kmeans.labels_
    sil.append(silhouette_score(store_coordinates, labels, metric='euclidean'))

clusters = 5

#K-means algorithm
means = KMeans(n_clusters=clusters, init='k-means++')    # **
kmeans.fit(store_coordinates)
y = kmeans.labels_
print("k = ", str(clusters), " silhouette_score ", silhouette_score(store_coordinates, y, metric='euclidean'))


# Saving results in files
# This part generates clusters+1 files, 1 file per cluster and a file with k_means.
# This can be changed to work with a databse directly.

# Add labels to dataset
k_labels = np.asarray(kmeans.labels_)
stores['cluster'] = k_labels


# Save K-means
k_means_matrix = np.asarray(kmeans.cluster_centers_)
df_means = pd.DataFrame(data=k_means_matrix, index= np.unique(k_labels), columns=["Longitude","Latitude"])
df_means.to_csv("../Data/Results/k_means_ext.csv")

# Save each store in their respective cluster
f_cluster = "../Data/Results/Cluster_ext_"
f_cluster_sufix = ".csv"

for i_index in np.unique(k_labels):
    file_name=f_cluster+str(i_index)+f_cluster_sufix
    cluster_query=stores.query("cluster=="+str(i_index))
    cluster_query.to_csv(file_name,index=False)


