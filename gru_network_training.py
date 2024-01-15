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

emotions_dataset = pd.read_csv('EmotionsDataset.csv')

tokenizer = Tokenizer()
tokenizer.fit_on_texts(emotions_dataset['text'])
stop_words = set(['and', 'in', 'not', 'that', 'on', 'with'])
emotions_dataset['filtered_text'] = emotions_dataset['text'].apply(
    lambda x: ' '.join([word for word in x.split() if word.lower() not in stop_words]))

sequences = tokenizer.texts_to_sequences(emotions_dataset['filtered_text'])
max_sequence_length = max(len(s) for s in sequences)  # определяем максимальную длину последовательности
X = pad_sequences(sequences, maxlen=max_sequence_length)

emotions_labels = emotions_dataset[['anger', 'fear', 'joy', 'sadness', 'сalmness']]
y = np.array(emotions_labels)

X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

embedding_dim = 100
gru_units = 32

model = Sequential()
model.add(
    Embedding(input_dim=len(tokenizer.word_index) + 1, output_dim=embedding_dim, input_length=max_sequence_length))
model.add(GRU(units=gru_units))
model.add(Dense(units=len(emotions_labels.columns), activation='sigmoid'))

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

epochs = 10
batch_size = 23

checkpoint_callback = ModelCheckpoint('best_model_weights.h5', save_best_only=True, monitor='val_loss', mode='min',
                                      verbose=1)
early_stopping_callback = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True, verbose=1)


def training_method():
    history = model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size,
                        validation_data=(X_val, y_val), callbacks=[checkpoint_callback, early_stopping_callback])

