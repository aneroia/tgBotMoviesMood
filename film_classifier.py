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

# Применение функции для создания нового столбца 'mood'
df['mood'] = df['main_genre'].apply(determine_mood)

# Разделение на несколько строк, если у фильма несколько настроений
df['mood'] = df['mood'].apply(lambda x: x if x else [])

# Преобразование списка настроений в строку
df['mood'] = df['mood'].apply(lambda x: ', '.join(x) if x else None)

# обработка жанров, которые не включались в датасет(у них настроение null)
df = df.dropna(subset=['mood'])

# оставляем те столбцы, которые нам необходимы для классификатора
selected_columns = ['Movie_Title', 'Year', 'Rating', 'Runtime(Mins)', 'main_genre', 'mood']
df_selected = df.loc[:, selected_columns]

# сохранение измененного датасета
df_selected.to_csv("film_classifier_dataset.csv")

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)

print(df_selected.head(2))