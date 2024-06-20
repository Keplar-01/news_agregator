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
from pymorphy2 import MorphAnalyzer

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
morph = MorphAnalyzer()
class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class BaseModelService(metaclass=SingletonMeta):
    def __init__(self):
        self.file_extension = None

    def set_model(self, model_name: str = 'model_svm.pkl'):
        self.model = self.load_model(model_name)

    def preprocess_text_to_tokens(self, text: str):
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        tokens = word_tokenize(text, language='russian')
        tokens = [word for word in tokens if word not in stop_words]
        lemmatized_tokens = [morph.parse(word)[0].normal_form for word in tokens]
        return lemmatized_tokens

    def preprocess_text_to_one_text(self, text: str):
        tokens = self.preprocess_text_to_tokens(text)
        return " ".join(tokens)

    def save_tokenizer(self, tokenizer, filename):
        with open(filename, 'wb') as handle:
            joblib.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def load_tokenizer(self, filename):
        script_dir = os.path.dirname(__file__)
        model_path = os.path.join(script_dir, 'ml_models/tokenizer', filename)

        with open(model_path, 'rb') as f:
            tokenizer = joblib.load(f)
            return tokenizer

    def save_w2v_model(self, w2v_model, filename):
        w2v_model.save(filename)

    def load_w2v_model(self, filename):
        return Word2Vec.load(filename)

    def load_encoder(self, filename):
        script_dir = os.path.dirname(__file__)
        model_path = os.path.join(script_dir, 'ml_models/encoders', filename)

        with open(model_path, 'rb') as f:
            loaded_encoder = pickle.load(f)
            return loaded_encoder

    def load_model(self, name_model: str):
        script_dir = os.path.dirname(__file__)
        model_path = os.path.join(script_dir, 'ml_models/', name_model)
        self.file_extension = os.path.splitext(model_path)[1]

        if self.file_extension == '.pkl':
            with open(model_path, 'rb') as file:
                model = joblib.load(file)
        elif self.file_extension == '.keras':
            model = load_model_keras(model_path)
        else:
            raise ValueError(f'Расширение не поддерживается: {self.file_extension}. '
                             f'Только .pkl и .keras могут быть использованы.')

        return model

    def prediction(self, text: str):
        pass


class MlModelService(BaseModelService):
    def __init__(self, model_name: str = 'model_svm.pkl', tokenizer_name: str = 'tokenizer.pkl',
                 encoder_name: str = 'encoder.pkl'):
        super().__init__()
        self.tokenizer = self.load_tokenizer(tokenizer_name)
        self.encoder = self.load_encoder(encoder_name)
        self.model = self.load_model(model_name)

    def predict(self, text: str):
        if self.file_extension == '.pkl':
            new_text = self.preprocess_text_to_one_text(text)
            prediction = self.model.predict([new_text])
        else:
            new_text = self.preprocess_text_to_tokens(text)
            sequence = self.tokenizer.texts_to_sequences([new_text])
            sequence = pad_sequences(sequence, maxlen=360)
            prediction = self.model.predict(sequence)
            prediction = self.encoder.inverse_transform([np.argmax(prediction)])
        return prediction[0]


class MoodModelService(BaseModelService):
    def __init__(self, model_name: str = 'emotion.pkl', tokenizer_name: str = 'emotion_vectorizer_tfidf.pkl',
                 encoder_name: str = 'emotion_encoder.pkl'):
        super().__init__()
        self.mood_model = self.load_model(model_name)
        self.mood_tokenizer = self.load_tokenizer(tokenizer_name)
        self.mood_encoder = self.load_encoder(encoder_name)

    def predict(self, text: str):
        new_text = self.preprocess_text_to_one_text(text)
        sequence = self.mood_tokenizer.transform([new_text])
        prediction = self.mood_model.predict(sequence)
        prediction = self.mood_encoder[prediction[0]]
        return prediction
