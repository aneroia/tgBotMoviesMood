import pandas as pd

df = pd.read_csv("IMDb_All_Genres_etf_clean1.csv")
def determine_mood(genre):
    moods = []
    if "Drama" in genre:
        moods.append("sadness")
    if any(g in genre for g in ["Horror", "Thriller", "Mystery"]):
        moods.append("fear")
    if any(g in genre for g in ["Romance", "Adventure"]):
        moods.extend(["calmness", "joy"])
    if any(g in genre for g in ["Comedy", "Adventure", "Sci-Fi"]):
        moods.append("joy")
    if any(g in genre for g in ["Action", "Crime"]):
        moods.append("anger")
    if "Sport" in genre:
        moods.extend(["joy", "anger"])
    return moods if moods else None

df['mood'] = df['main_genre'].apply(determine_mood)

df['mood'] = df['mood'].apply(lambda x: x if x else [])

df['mood'] = df['mood'].apply(lambda x: ', '.join(x) if x else None)

df = df.dropna(subset=['mood'])

selected_columns = ['Movie_Title', 'Year', 'Rating', 'Runtime(Mins)', 'main_genre', 'mood']
df_selected = df.loc[:, selected_columns]

# сохранение измененного датасета
df_selected.to_csv("film_classifier_dataset.csv")