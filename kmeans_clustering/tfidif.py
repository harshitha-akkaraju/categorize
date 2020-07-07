import numpy as np 
import pandas as pd

from sklearn.cluster import KMeans 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
from sklearn.preprocessing import normalize
from sklearn.metrics import pairwise_distances
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import word_tokenize

from nltk.cluster import KMeansClusterer

import nltk
import string

import fasttext
import os

import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

ignore = [
  'today',
  'new'
  'york',
  'times',
  'com',
  'thedaily',
  'michael',
  'understand'
  "nytimes.com/thedaily",
  "episode",
  'nytimes',
  'rabbit',
  'hole',
  's',
  'rabbithole'
  'mr',
  'trump',
]

def get_cbow_model(regenerate=False):
    cbow_model_file_path = './models/cbow_model.bin'
    if regenerate:
        print("regenerating the cbow model...")
        
        data_file_path = "./data/the_daily_data.txt"
        cbow_model = fasttext.train_unsupervised(data_file_path, model='cbow')
        cbow_model.save_model(cbow_model_file_path)
    
    if os.path.exists(cbow_model_file_path):
        model = fasttext.load_model(cbow_model_file_path)
        return model
    
    return None

def tokenize(text):
  # remove punctuation
  tokenizer = RegexpTokenizer(r'\w+')
  tokens = tokenizer.tokenize(text)

  # remove words with digits in them
  tokens = [item for item in tokens if not any(filter(str.isdigit, item))]

  # remove words to ignore
  tokens = [token.lower().strip() for token in tokens]
  tokens = [elem for elem in tokens if elem not in ignore]

  return tokens

def get_top_features(tf_idf_vectorizer, tf_idf_array, prediction, num_features):
  labels = np.unique(prediction)
  dfs = []
  for label in labels:
    cluster_index = np.where(prediction==label)
    average_scores = np.mean(tf_idf_array[cluster_index], axis = 0)
    top_k = np.argsort(average_scores)[::-1][:num_features]
    features = tf_idf_vectorizer.get_feature_names()

    best_features = [(features[i], average_scores[i]) for i in top_k]
    df = pd.DataFrame(best_features, columns = ['features', 'score'])
    dfs.append(df)
  
  return dfs

def determine_number_of_clusters(Y_sklearn):
  number_of_clusters = range(1, 7)
  kmeans = [KMeans(n_clusters=i, max_iter = 1000) for i in number_of_clusters]
  score = [kmeans[i].fit(Y_sklearn).score(Y_sklearn) for i in range(len(kmeans))]

  plt.plot(number_of_clusters, score)
  plt.xlabel('Number of Clusters')
  plt.ylabel('Score')
  plt.title('Elbow Method')
  plt.show()

def tfidf():
  episode_data = pd.read_csv('./data/the_daily_episode_data.csv')
  descriptions = episode_data['description']

  tf_idf_vectorizer = TfidfVectorizer(
      stop_words = 'english',
      tokenizer=tokenize,
      max_features = 5000
    )
  
  # clean the text
  tf_idf = tf_idf_vectorizer.fit_transform(descriptions)
  tf_idf_norm = normalize(tf_idf)
  tf_idf_array = tf_idf_norm.toarray()

  # print feature names
  # feature_names = pd.DataFrame(tf_idf_array, columns=tf_idf_vectorizer.get_feature_names())
  # print(pd.DataFrame(tf_idf_array, columns=tf_idf_vectorizer.get_feature_names()).head(5))

  sklearn_pca = PCA(n_components = 2)
  Y_sklearn = sklearn_pca.fit_transform(tf_idf_array)

  # elbow method
  # determine_number_of_clusters(Y_sklearn)

  kmeans = KMeans(n_clusters=3, max_iter=600, algorithm = 'auto')
  fitted = kmeans.fit(Y_sklearn)

  prediction = kmeans.predict(Y_sklearn)

  dfs = get_top_features(tf_idf_vectorizer, tf_idf_array, prediction, 10)
  print(dfs)

