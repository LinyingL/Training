# -*- coding: utf-8 -*-
"""Top2Vec.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tfXbY3Yd7kJs4KGBRXhoVHIhWOfVupCA
"""

import pandas as pd

# Read the csv file from Kaggle, It's about Trump's tweets until July 2020.
from google.colab import drive
drive.mount('/content/drive')
df = pd.read_csv("/content/drive/My Drive/Colab Notebooks/realdonaldtrump.csv")

# create a new column called "iddf" to store the index of each row
df["iddf"]=range(len(df))
df2= df[["iddf","content"]]

# remove rows with empty content
df2 = df2.dropna(subset=['content'])

# See length of df2
len(df2)

import nltk
nltk.download('stopwords')
nltk.download('punkt')

# Cleaning the text. According to the guideline, the cleaning is not necessary.
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
stop_words = set(stopwords.words('english'))

def preprocess(text):
    text = text.lower()
    text = ''.join([word for word in text if word not in string.punctuation])
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word not in stop_words]
    return ' '.join(tokens)

datatext = df2["content"].apply(preprocess)

!pip install top2vec
!pip install top2vec[sentence_transformers]
!pip install top2vec[sentence_encoders]

from top2vec import Top2Vec
#Training model
model = Top2Vec(datatext.values, embedding_model = "universal-sentence-encoder")

# Get the number of topics(random)
model.get_num_topics()

# Generate wordclound for 4.topic
model.generate_topic_wordcloud(4)

# Reducting the topics and create a new model2
model2 = model.hierarchical_topic_reduction(num_topics=10)

model2.generate_topic_wordcloud(4)

!pip install umap-learn[plot]

import matplotlib.pyplot as plt

import umap
import numpy as np
# Get the topic vectors
topic_vectors = model.topic_vectors

# Dimensionalization
umap_model = umap.UMAP(n_neighbors=5, min_dist=0.2, n_components=2, random_state=28)
umap_embeddings = umap_model.fit_transform(topic_vectors)


# Plotting the UMAP
plt.figure(figsize=(10, 9))
plt.scatter(umap_embeddings[:, 0], umap_embeddings[:, 1], alpha=0.5)
plt.title('UMAP projection of Top2Vec Topic Vectors')
plt.show()

!pip install hdbscan

import hdbscan
# Apply HDBSCAN
umap_model = umap.UMAP(n_neighbors=15, min_dist=0.1, n_components=2, random_state=28)
clusterer = hdbscan.HDBSCAN(min_cluster_size=20, gen_min_span_tree=True)
cluster_labels = clusterer.fit_predict(umap_embeddings)

# Plotting
plt.figure(figsize=(12, 10))
unique_clusters = np.unique(cluster_labels)
colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_clusters)))

for cluster, color in zip(unique_clusters, colors):
    if cluster == -1:  # Outliers marked as -1
        color = 'red'

    member_mask = cluster_labels == cluster
    plt.scatter(umap_embeddings[member_mask, 0], umap_embeddings[member_mask, 1],
                s=50, color=color, label=f'Cluster {cluster}' if cluster != -1 else 'Outliers')

plt.title('HDBSCAN Clustering of Document Vectors')
plt.legend()
plt.show()

model3 = Top2Vec(df2['content'].values, embedding_model = "universal-sentence-encoder")

model3.get_num_topics()

model3.generate_topic_wordcloud(250)

topic_vectors = model3.topic_vectors

# Dimensionalization
umap_model = umap.UMAP(n_neighbors=5, min_dist=0.2, n_components=2, random_state=28)
umap_embeddings = umap_model.fit_transform(topic_vectors)


# Plotting the UMAP
plt.figure(figsize=(10, 9))
plt.scatter(umap_embeddings[:, 0], umap_embeddings[:, 1], alpha=0.5)
plt.title('UMAP projection of Top2Vec Topic Vectors')
plt.show()

umap_model = umap.UMAP(n_neighbors=15, min_dist=0.1, n_components=2, random_state=28)
clusterer = hdbscan.HDBSCAN(min_cluster_size=20, gen_min_span_tree=True)
cluster_labels = clusterer.fit_predict(umap_embeddings)

# Plotting
plt.figure(figsize=(12, 10))
unique_clusters = np.unique(cluster_labels)
colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_clusters)))

for cluster, color in zip(unique_clusters, colors):
    if cluster == -1:  # Outliers marked as -1
        color = 'red'

    member_mask = cluster_labels == cluster
    plt.scatter(umap_embeddings[member_mask, 0], umap_embeddings[member_mask, 1],
                s=50, color=color, label=f'Cluster {cluster}' if cluster != -1 else 'Outliers')

plt.title('HDBSCAN Clustering of Document Vectors')
plt.legend()
plt.show()