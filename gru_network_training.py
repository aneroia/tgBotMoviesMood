import epochs
import numpy as np
import pandas as pd
import keras.preprocessing
from keras.models import Sequential
from keras.layers import Embedding, GRU, Dense
from keras.src.preprocessing.text import Tokenizer
from keras.src.utils import pad_sequences
from sklearn.model_selection import train_test_split
from keras.callbacks import ModelCheckpoint, EarlyStopping

# Загрузка датасета

emotions_dataset = pd.read_csv('EmotionsDataset.csv')

# Предобработка текста
tokenizer = Tokenizer()
tokenizer.fit_on_texts(emotions_dataset['text'])
stop_words = set(['and', 'in', 'not', 'that', 'on', 'with'])
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
gru_units = 32

model = Sequential()
model.add(Embedding(input_dim=len(tokenizer.word_index) + 1, output_dim=embedding_dim, input_length=max_sequence_length))
model.add(GRU(units=gru_units))
model.add(Dense(units=len(emotions_labels.columns), activation='sigmoid'))

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Обучение модели
epochs = 10  # подберите количество эпох
batch_size = 23  # подберите размер батча



# Определение коллбэка для сохранения лучших весов модели
checkpoint_callback = ModelCheckpoint('best_model_weights.h5', save_best_only=True, monitor='val_loss', mode='min', verbose=1)

# Определение коллбэка для ранней остановки обучения
early_stopping_callback = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True, verbose=1)

# Обучение модели с использованием коллбэков
history = model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size,
                    validation_data=(X_val, y_val), callbacks=[checkpoint_callback, early_stopping_callback])

# После обучения, вы можете загрузить лучшие веса
best_model = Sequential()
best_model.add(Embedding(input_dim=len(tokenizer.word_index) + 1, output_dim=embedding_dim, input_length=max_sequence_length))
best_model.add(GRU(units=gru_units))
best_model.add(Dense(units=len(emotions_labels.columns), activation='sigmoid'))
best_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
best_model.load_weights('best_model_weights.h5')

