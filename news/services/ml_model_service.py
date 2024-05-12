import os
import pickle
import re
import pandas as pd
import numpy as np
import nltk
import re
import joblib

from keras.src.saving import load_model as load_model_keras
from keras.src.utils import pad_sequences

nltk.download("stopwords")
nltk.download('punkt')

from nltk.corpus import stopwords
from string import punctuation
from nltk import word_tokenize
import re
from nltk.corpus import stopwords
from gensim.models import Word2Vec
import keras as keras
# Загрузка стоп-слов для русского языка
stop_words = set(stopwords.words('russian'))

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class MlModelService(metaclass=SingletonMeta):
    def __init__(self, model_name: str = 'model_svm.pkl', tokenizer_name: str = 'tokenizer.pkl', encoder_name: str = 'encoder.pkl'):
        if not hasattr(self, 'tokenizer'):
            self.tokenizer = self.load_tokenizer(tokenizer_name)
        if not hasattr(self, 'encoder'):
            self.encoder = self.load_encoder(encoder_name)
        if not hasattr(self, 'model'):
            self.model = self.load_model(model_name)

    def set_model(self, model_name:str='model_svm.pkl'):
        self.model = self.load_model(model_name)

    def preprocess_text_to_tokens(self, text: str):
        # Приведение к нижнему регистру
        text = text.lower()
        # Удаление пунктуации
        text = re.sub(r'[^\w\s]', '', text)
        # Токенизация текста
        tokens = word_tokenize(text, language='russian')
        # Удаление стоп-слов
        tokens = [word for word in tokens if word not in stop_words]
        # Объединение токенов обратно в текст
        return tokens

    def preprocess_text_to_vector(self):
        pass

    def preprocess_text_to_one_text(self, text: str):
        # Приведение к нижнему регистру
        text = text.lower()
        # Удаление пунктуации
        text = re.sub(r'[^\w\s]', '', text)
        # Токенизация текста
        tokens = word_tokenize(text)
        # Удаление стоп-слов
        tokens = [word for word in tokens if word not in stop_words]
        # Объединение токенов обратно в текст
        return " ".join(tokens)

    def train_model(self):
        pass

    def save_tokenizer(self, tokenizer, filename):
        with open(filename, 'wb') as handle:
            joblib.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def load_tokenizer(self, filename):
        script_dir = os.path.dirname(__file__)
        model_path = os.path.join(script_dir, '..', 'ml_models/tokenizer', filename)

        with open(model_path, 'rb') as f:
            tokenizer = joblib.load(f)
            return tokenizer

    def save_w2v_model(self, w2v_model, filename):
        w2v_model.save(filename)

    def load_w2v_model(self, filename):
        return Word2Vec.load(filename)
    
    def load_encoder(self, filename):
        script_dir = os.path.dirname(__file__)
        model_path = os.path.join(script_dir, '..', 'ml_models/encoders', filename)

        with open(model_path, 'rb') as f:
            loaded_encoder = pickle.load(f)
            return loaded_encoder
    
    def predict(self, model, text: str, type_model: str = 'pkl'):
        if type_model == 'pkl':
            new_text = self.preprocess_text_to_one_text(text)
            prediction = model.predict([new_text])
            print(prediction)
        else:
            new_text = self.preprocess_text_to_tokens(text)
            sequence = self.tokenizer.texts_to_sequences([new_text])
            sequence = pad_sequences(sequence, maxlen=280)
            prediction = model.predict(sequence)
            prediction = self.encoder.inverse_transform([np.argmax(prediction)])
        return prediction[0]


    def save_model(self):
        pass

    def create_model(self):
        pass

    def load_model(self, name_model: str):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        model_path = os.path.join(base_dir, 'ml_models', name_model)

        file_extension = os.path.splitext(model_path)[1]

        if file_extension == '.pkl':
            with open(model_path, 'rb') as file:
                model = joblib.load(file)
        elif file_extension == '.keras':
            model = keras.models.load_model(model_path)
        else:
            raise ValueError(f'Unsupported file extension: {file_extension}. Only .pickle and .keras are supported.')

        return model