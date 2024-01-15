import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import Embedding, GRU, Dense
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

from gru_network_training import tokenizer, embedding_dim, gru_units, emotions_labels, stop_words

max_sequence_length = 100


def preprocess_text(text, tokenizer, stop_words):
    filtered_text = ' '.join([word for word in text.split() if word.lower() not in stop_words])
    sequence = tokenizer.texts_to_sequences([filtered_text])
    padded_sequence = pad_sequences(sequence, maxlen=max_sequence_length)
    return padded_sequence


def predict_emotion(user_input):
    best_model = Sequential()
    best_model.add(
        Embedding(input_dim=len(tokenizer.word_index) + 1, output_dim=embedding_dim, input_length=max_sequence_length))
    best_model.add(GRU(units=gru_units))
    best_model.add(Dense(units=len(emotions_labels.columns), activation='sigmoid'))
    best_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    best_model.load_weights('best_model_weights.h5')

    preprocessed_input = preprocess_text(user_input, tokenizer, stop_words)
    prediction = best_model.predict(preprocessed_input)

    max_emotion = max(emotions_labels.columns,
                      key=lambda emotion: prediction[0][emotions_labels.columns.get_loc(emotion)])

    return max_emotion