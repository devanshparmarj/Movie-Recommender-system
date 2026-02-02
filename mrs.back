import numpy as np
import pandas as pd
import csv
import ast

credits = pd.read_csv(
    '/content/tmdb_5000_credits.csv',
    sep=',',
    encoding='utf-8',
    engine='python',
    on_bad_lines='skip',
    quotechar='"',
    doublequote=True
)
movies = pd.read_csv(
    '/content/tmdb_5000_movies.csv',
    sep=',',
    encoding='utf-8',
    engine='python',
    on_bad_lines='skip',
    quotechar='"',
    doublequote=True
)

movies.head(1)
credits.head(1)
movies = movies.merge(credits, on='title')
movies.head(1)
movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]


movies.isnull().sum()
movies.dropna(inplace=True)
movies.duplicated().sum()
movies.iloc[0].genres

def convert(obj):
    L = []
    for i in ast.literal_eval(obj):
     L.append(i['name'])
    return L

movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)
movies.head()

def convert3(obj):
    L = []
    counter = 0
    for i in ast.literal_eval(obj):
      if counter != 3:
        L.append(i['name'])
        counter+=1
      else:
        break
    return L

movies['cast'] = movies['cast'].apply(convert3)

def fetch_director(text):
    directors = []

    if pd.isna(text):
        return directors

    try:
        for i in ast.literal_eval(text):
            if i.get('job') == 'Director':
                directors.append(i.get('name'))
                break
    except:
        return directors

    return directors


def fetch_director(obj):
  L = []
  for i in ast.literal_eval(obj):
    if i['job'] == 'Director':
      L.append(i['name'])
      break
  return L
movies['crew'] = movies['crew'].apply(fetch_director)

movies.head()
movies['overview'] = movies['overview'].apply(lambda x:x.split())
movies.head()

movies['genres'] = movies['genres'].apply(lambda x:[i.replace(" ","")for i in x])
movies['keywords'] = movies['keywords'].apply(lambda x:[i.replace(" ","")for i in x])
movies['cast'] = movies['cast'].apply(lambda x:[i.replace(" ","")for i in x])
movies['crew'] = movies['crew'].apply(lambda x:[i.replace(" ","")for i in x])

movies.head()
movies['tags'] = movies['overview'] + movies['keywords'] + movies['genres'] + movies['crew'] + movies['cast']
movies.head()
new_df = movies[['movie_id','title','tags']].copy()
new_df['tags'] = new_df['tags'].apply(lambda x:" ".join(x))
new_df.head()
new_df['tags'] = new_df['tags'].apply(lambda x:x.lower())
new_df.head()

#vectorization

from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=5000,stop_words='english')
vectors = cv.fit_transform(new_df['tags']).toarray()



from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()

def stem(text):
    y = []
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)

new_df['tags'] = new_df['tags'].apply(stem)
ps.stem('danced')

#Cosine Similarity

from sklearn.metrics.pairwise import cosine_similarity
similarity = cosine_similarity(vectors)

sorted_list = sorted(list(enumerate(similarity[0])), reverse=True, key=lambda x:x[1])

#Recommendation

def recommend(movie):
  if movie not in new_df['title'].values:
    print(f"Movie '{movie}' not found in the dataset.")
    return

    movie_index = new_df[new_df['title'] == movie].index[0]
    distances = similarity[movie_index]


    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

    for i in movies_list:
        print(new_df.iloc[i[0]].title)

        recommend('Avatar')
        new_df.iloc[1216].title