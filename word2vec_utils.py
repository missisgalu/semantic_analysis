# word2vec_utils.py

import re
import nltk
from razdel import tokenize # Библиотека для токенизации русского текста
from nltk.stem import WordNetLemmatizer
from gensim.models import Word2Vec
from stop_words import get_stop_words

nltk.download('wordnet', quiet=True)

russian_stopwords = get_stop_words('ru')

# Создание лемматизатора на основе WordNet
lemmatizer = WordNetLemmatizer()

# Функция очистки текста от чисел, лишних символов и приведения к нижнему регистру
def clean_text(text):
    text = text.lower()
    # Удаление чисел
    text = re.sub(r'[0-9]+', '', text)
    # Удаление лишних символов
    text = re.sub(r'[^а-яА-ЯёЁ\s]', '', text)
    # Замена ё на е
    text = text.replace('ё', 'е')

    return text

# Функция предобработки текста перед токенизацией
def preprocess_text(text):
    text = clean_text(text)
    # Токенизация очищенного текста 
    tokens = [t.text for t in tokenize(text)]

    return tokens 

# Функция лемматизации списка токенов
def lemmatize_tokens(tokens):
    return [lemmatizer.lemmatize(token) for token in tokens]

# Функция токенизации
def tokenize_text(text):
    return [t.text for t in tokenize(text)]

# Функция удаления стоп-слов 
def remove_stopwords(tokens, stop_words):

  return [token for token in tokens if token not in stop_words]

# Функция нормализации текста
def normalize_text(text):
    text = clean_text(text)
    
    return text

# Функция разбиения текста на предложения
def split_sentences(text):
    return [sent.text for sent in tokenize(text)]

def train_word2vec_model(texts, progress_callback):
    # Загрузка стоп-слов
    with open('stopwords.txt', encoding='utf-8') as f:
        stop_words = f.read().splitlines()
    # Список для хранения предобработанных текстов
    preprocessed_texts = []
    # Словарь для подсчета частоты слов
    # Нужен для удаления редко встречающихся слов
    word_counts = {}

    total_steps = len(texts)
    current_step = 0

    # Цикл по исходным текстам
    for text in texts:
        # Нормализация текста - приведение к нижнему регистру,
        # удаление спецсимволов 
        text = normalize_text(text)
        # Разбиваем текст на предложения
        sentences = split_sentences(text)

        # Обрабатываем каждое предложение
        for sentence in sentences:
            tokens = tokenize_text(sentence)
            tokens = remove_stopwords(tokens, stop_words)
            tokens = lemmatize_tokens(tokens)
            preprocessed_texts.append(tokens)

            # Счетчик частоты слов
            for token in tokens:
                word_counts[token] = word_counts.get(token, 0) + 1

        current_step += 1
        progress = int((current_step / total_steps) * 100)
        progress_callback(progress)

    # Удаление редких слов и увеличение порога частоты слов
    preprocessed_texts = [
        [token for token in tokens if word_counts[token] > 1]
        for tokens in preprocessed_texts
    ]

    # Размер словаря (min_count),
    # размер векторов слов (vector_size),
    # оптимальное окно контекста (window)
    model = Word2Vec(vector_size=100, min_count=2, window=10)
    model.build_vocab(preprocessed_texts)
    model.train(preprocessed_texts, total_examples=model.corpus_count, epochs=10)

    return model