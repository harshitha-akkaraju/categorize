from gensim.models import Word2Vec
from nltk.tokenize import RegexpTokenizer
from nltk.cluster import KMeansClusterer
from sklearn import metrics
from sklearn import cluster

import pandas as pd
import nltk

def tokenize(text):
  # remove punctuation
  tokenizer = RegexpTokenizer(r'\w+')
  tokens = tokenizer.tokenize(text)

  # remove words with digits in them
  tokens = [item for item in tokens if not any(filter(str.isdigit, item))]

  # remove words to ignore
  tokens = [token.lower().strip() for token in tokens]
  # tokens = [elem for elem in tokens if elem not in ignore]

  return tokens


def main():
  episode_data = pd.read_csv('./data/the_daily_episode_data.csv')
  titles = episode_data['title']
  descriptions = episode_data['description']

  documents = []
  for doc in descriptions:
    tokens = tokenize(doc)
    documents.append(tokens)
  
  model = Word2Vec(documents, min_count=5)
  X = model[model.wv.vocab]

  NUM_CLUSTERS = 7
  kclusterer = KMeansClusterer(NUM_CLUSTERS, distance=nltk.cluster.util.cosine_distance, repeats=25)
  assigned_clusters = kclusterer.cluster(X, assign_clusters=True)

  clusters = []
  for i in range (0, NUM_CLUSTERS):
    clusters.append([])
  
  vocab = list(model.wv.vocab)
  count = 0
  for i, word in enumerate(vocab):
    c = assigned_clusters[i]
    clusters[c].append(word)


  kmeans = cluster.KMeans(n_clusters=NUM_CLUSTERS)
  kmeans.fit(X)

  labels = kmeans.labels_
  centroids = kmeans.cluster_centers_

  df = group(clusters, documents, titles, descriptions)
  df.to_csv('./data/grouped.csv')

def group(clusters, documents, titles, descriptions):
  annotated = {}
  groups = ["" for elem in documents]

  for doc_index in range (0, len(documents)):
    doc = documents[doc_index]

    for cluster_index in range (0, len(clusters)):
      common = set(doc).intersection(clusters[cluster_index])

      if len(common) > 0:
        annotated
        groups[doc_index] = groups[doc_index] + ", " + str(cluster_index)
  
  annotated["title"] = titles
  annotated["description"] = descriptions
  annotated["cluster"] = groups

  return pd.DataFrame.from_dict(annotated)


if __name__ == "__main__":
  main()

