##1##  pip install huggingface_hub
##2##  git clone https://huggingface.co/datasets/go_emotions
import pandas as pd
import numpy as np

df = pd.read_csv('go_emotions_dataset.csv')
print(df.head())
print(df.columns)
df = df.drop('id', axis=1)
df = df.drop('example_very_unclear', axis=1)
print(df)

# Выделяем основные эмоции

# SADNESS
# Заменяем значения в столбце 'sadness'
df['sadness'] = df[['disappointment', 'grief', 'remorse', 'sadness']].any(axis=1).astype(int)
# Удаляем столбцы 'disappointment', 'grief', 'remorse'
df = df.drop(['disappointment', 'grief', 'remorse'], axis=1)

# FEAR
# Заменяем значения в столбце 'fear'
df['fear'] = df[['fear', 'embarrassment', 'nervousness', 'confusion']].any(axis=1).astype(int)
# Удаляем столбцы 'embarrassment', 'nervousness', 'confusion'
df = df.drop(['embarrassment', 'nervousness', 'confusion'], axis=1)

# CALMNESS
# Создаем новый столбец, т.к. среди имеющихся нет подходящего
df = df.assign(сalmness=0)
# Заменяем значения в столбце 'сalmness'
df['сalmness'] = df[['сalmness', 'approval', 'caring',
                     'desire', 'gratitude', 'love',
                     'optimism', 'pride', 'relief',
                     'realization', 'neutral']].any(axis=1).astype(int)
# Удаляем все столбцы кроме calmness
df = df.drop(['approval', 'caring',
                     'desire', 'gratitude', 'love',
                     'optimism', 'pride', 'relief',
                     'realization', 'neutral'], axis=1)