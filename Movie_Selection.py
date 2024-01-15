import pandas as pd
import random

df = pd.read_csv("film_classifier_dataset.csv")

emotion = 'anger'
film_recommendation = ''
def random_movies_with_emotion(df, emotion, num_movies):
    movies = df[df['mood'] == emotion][['Movie_Title', 'Year', 'Rating', 'Runtime(Mins)','main_genre']]
    random_movies = random.sample(list(movies.iterrows()), num_movies)
    return random_movies

def get_movies(df,emotion):
    movies2 = list()
    if emotion == 'calmness':
        movies = random_movies_with_emotion(df, 'calmness, joy, joy', 3)
    elif emotion == 'anger' or emotion == 'sadness':
        movies = random_movies_with_emotion(df, emotion, 3)
        movies2 = random_movies_with_emotion(df, 'joy', 3)
    elif emotion == 'fear':
        movies = random_movies_with_emotion(df, emotion, 3)
        movies2 = random_movies_with_emotion(df, 'calmness, joy, joy', 3)
    else:
        movies = random_movies_with_emotion(df, emotion, 3)
    return movies, movies2




random_movies, random_movies2 = get_movies(df,emotion)


def get_str_films(film_recommendation,random_movies, random_movies2):
    for movie in random_movies:
        movie_info = movie[1]
        film_recommendation += f'''{movie_info['Movie_Title']}, {movie_info['Year']}, {movie_info['Rating']}, {movie_info['Runtime(Mins)']} mins, {movie_info['main_genre']}\n'''
    if random_movies2:
        film_recommendation+= '\n If you want to improve your mood:\n'
    for movie in random_movies2:
        movie_info = movie[1]
        film_recommendation += f'''{movie_info['Movie_Title']}, {movie_info['Year']}, {movie_info['Rating']}, {movie_info['Runtime(Mins)']} mins, {movie_info['main_genre']}\n'''
    return film_recommendation

print(get_str_films(film_recommendation,random_movies, random_movies2))
