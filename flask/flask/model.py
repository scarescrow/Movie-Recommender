import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.neighbors import NearestNeighbors

def load_movie_metadata():
    df = pd.read_csv('static/data/the-movies-dataset/movies_metadata.csv')
    return df

def get_cosine_sim(df, overview_col_name='overview'):
    tfidf = TfidfVectorizer(stop_words='english')
    df[overview_col_name] = df[overview_col_name].fillna('')
    tfidf_matrix = tfidf.fit_transform(df[overview_col_name])
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix) 
    return cosine_sim

def content_show_recommendations(title, df, cosine_sim, title_col_name='title', overview_col_name='overview'):
    recs = []
    indices = pd.Series(df.index, index=df[title_col_name].apply(lambda x: str(x).lower())).drop_duplicates()
    idx = indices[title.lower()]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:6]
    movie_indices = [i[0] for i in sim_scores]
    for index, row in df.iloc[movie_indices][[title_col_name, overview_col_name]].iterrows():
        recs.append(list(row))
    return recs

def load_pickled_df():
    df = pd.read_pickle('static/data/df.pkl')
    return df

def fit_knn(feature_array, nn=6, algorithm='ball_tree', metric='euclidean'):
    knn = NearestNeighbors(n_neighbors=nn, algorithm=algorithm, metric=metric, n_jobs = -1).fit(feature_array) 
    return knn  

def find_nbrs(nbr_indices, images_df):
    nbrs = []
    for i in range(len(nbr_indices)): 
        nbr_index = nbr_indices[i]
        image_id = images_df[(images_df.index == nbr_index)].iloc[0]['imdb_id']
        original_title = images_df[(images_df.index == nbr_index)].iloc[0]['original_title']
        overview = images_df[(images_df.index == nbr_index)].iloc[0]['overview']
        nbrs.append([image_id, original_title, overview])
    return nbrs

def get_image_ids(df):
    required_fields = ['imdb_url', 'original_title', 'imdb_id', 'overview']
    return list(df[required_fields].T.to_dict().values())

def construct_nbr_file_path(image_id, dir):
    path = 'static/' + dir + image_id + '.jpg'
    return path


def show_recommendations(original_title, df, dir='img/', feature_column_name='feature_array'):
    knn = fit_knn(list(df['feature_array']))
    feature_array = df[(df['original_title'].str.lower() == original_title.lower())].iloc[0][feature_column_name].reshape(1,-1)
    nbr_indices = knn.kneighbors(feature_array, return_distance=False)
    nbr_indices = nbr_indices.tolist()[0]
    nbrs = find_nbrs(nbr_indices, df)
    for nbr in nbrs:
        path = construct_nbr_file_path(nbr[0], dir)
        nbr.append(path)
    return nbrs



