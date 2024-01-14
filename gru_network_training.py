import epochs
import numpy as np
import pandas as pd
from keras_preprocessing.sequence import pad_sequences
from keras_preprocessing.text import Tokenizer
from keras.models import Sequential
from keras.layers import Embedding, GRU, Dense
from sklearn.model_selection import train_test_split

# Загрузка датасета
emotions_dataset = pd.read_csv('EmotionsDataset.csv')

# Предобработка текста
tokenizer = Tokenizer()
tokenizer.fit_on_texts(emotions_dataset['text'])
stop_words = set(['and', 'in', 'not', 'that', 'on', 'with'])  # замените это на ваш фильтр стоп-слов
emotions_dataset['filtered_text'] = emotions_dataset['text'].apply(lambda x: ' '.join([word for word in x.split() if word.lower() not in stop_words]))

# Преобразование текста в числовые векторы
sequences = tokenizer.texts_to_sequences(emotions_dataset['filtered_text'])
max_sequence_length = max(len(s) for s in sequences)  # определяем максимальную длину последовательности
X = pad_sequences(sequences, maxlen=max_sequence_length)

# Преобразование меток эмоций
emotions_labels = emotions_dataset[['anger', 'fear', 'joy', 'sadness', 'сalmness']]
y = np.array(emotions_labels)

# Разделение на обучающий и тестовый наборы
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Построение модели GRU
embedding_dim = 100
gru_units = 64

model = Sequential()
model.add(Embedding(input_dim=len(tokenizer.word_index) + 1, output_dim=embedding_dim, input_length=max_sequence_length))
model.add(GRU(units=gru_units))
model.add(Dense(units=len(emotions_labels.columns), activation='sigmoid'))

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Обучение модели
epochs = 10  # подберите количество эпох
batch_size = 32  # подберите размер батча
model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_data=(X_val, y_val))
