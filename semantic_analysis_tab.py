# semantic_analysis_tab.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTableWidget, QTableWidgetItem
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtWidgets import QDialog, QTableWidget  
from PyQt5.QtWidgets import QFileDialog

from scipy.spatial.distance import cosine
from scipy.spatial.distance import euclidean
from scipy.spatial.distance import chebyshev

from gensim.models import Word2Vec
import matplotlib.pyplot as plt

import random
import gc
import os
import time

class SemanticAnalysisTab(QWidget):
    def __init__(self):
        super().__init__()

        # Атрибуты класса для хранения моделей 
        self.vacancy_model = None  
        self.discipline_model = None
        self.init_ui()

    def init_ui(self):

        # Вертикальный менеджер компоновки
        layout = QVBoxLayout()

        # Кнопка 1  
        load_vacancy_model_button = QPushButton("Загрузить модель вакансий")
        load_vacancy_model_button.clicked.connect(self.load_vacancy_model)

        load_vacancy_model_button.setStyleSheet("QPushButton {background-color: #42A5F5; color: black; padding: 10px;}")
        
        layout.addWidget(load_vacancy_model_button)

        self.loaded_vacancy_model_label = QLabel()
        layout.addWidget(self.loaded_vacancy_model_label) 

        # Кнопка 2
        load_discipline_model_button = QPushButton("Загрузить модель дисциплин")
        load_discipline_model_button.clicked.connect(self.load_discipline_model)  

        load_discipline_model_button.setStyleSheet("QPushButton {background-color: #42A5F5; color: black; padding: 10px;}")

        layout.addWidget(load_discipline_model_button)

        self.loaded_discipline_model_label = QLabel()
        layout.addWidget(self.loaded_discipline_model_label) 

        # Кнопка 3
        compare_models_button = QPushButton("Сравнить модели")
        compare_models_button.clicked.connect(self.compare_models)

        compare_models_button.setStyleSheet("QPushButton {background-color: #cc80ff; color: black; padding: 10px;}")

        layout.addWidget(compare_models_button)

        self.result_table = QTableWidget()
        self.result_table.setColumnCount(3)
        self.result_table.setHorizontalHeaderLabels(["Метрика", "Сходство, %", "Описание"])
        layout.addWidget(self.result_table)

        self.result_table.setColumnWidth(0, 170)
        self.result_table.setColumnWidth(1, 140)
        self.result_table.setColumnWidth(2, 250)
        
        # Кнопка 4
        plot_graphs_button = QPushButton("Составить графики")
        plot_graphs_button.clicked.connect(self.plot_graphs)

        plot_graphs_button.setStyleSheet("QPushButton {background-color: #ffa420; color: black; padding: 10px;}")

        layout.addWidget(plot_graphs_button)

        # Установка менеджера компоновки 
        self.setLayout(layout)

    # Метод загрузки модели вакансий
    def load_vacancy_model(self):
        
        file_path, _ = QFileDialog.getOpenFileName(self, "Выбрать модель вакансий", "", "Модели (*.model)")

        if file_path:
            try:
                self.vacancy_model = Word2Vec.load(file_path)
                self.loaded_vacancy_model_label.setText(f"Загружена модель: {file_path}")
                self.loaded_vacancy_model_label.adjustSize()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", str(e))
        else:
            QMessageBox.critical(self, "Ошибка", "Файл не выбран.")

    # Метод загрузки модели дисциплин
    def load_discipline_model(self):

        file_path, _ = QFileDialog.getOpenFileName(self, "Выбрать модель дисциплины", "", "Модели (*.model)")

        if file_path:
            try:
                self.discipline_model = Word2Vec.load(file_path)
                self.loaded_discipline_model_label.setText(f"Загружена модель: {file_path}")
                self.loaded_discipline_model_label.adjustSize()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", str(e))
        else:
            QMessageBox.critical(self, "Ошибка", "Файл не выбран.")

    # Метод сравнения загруженных моделей
    def compare_models(self):
        if self.vacancy_model is None or self.discipline_model is None:
            QMessageBox.critical(self, "Ошибка", "Модели не загружены.")
            return

        self.result_table.setRowCount(0)

        # Получаем размер словарей моделей
        vacancy_vocab_size = len(self.vacancy_model.wv.key_to_index)
        discipline_vocab_size = len(self.discipline_model.wv.key_to_index)

        # Генерируем случайные индексы
        random_vacancy_index = random.randint(0, vacancy_vocab_size - 1)
        random_discipline_index = random.randint(0, discipline_vocab_size - 1)

        # Получаем случайные слова по индексам
        random_word_vacancy = self.vacancy_model.wv.index_to_key[random_vacancy_index]
        random_word_discipline = self.discipline_model.wv.index_to_key[random_discipline_index]

        # Извлекаем векторы слов
        vacancy_vector = self.vacancy_model.wv[random_word_vacancy]
        discipline_vector = self.discipline_model.wv[random_word_discipline]

        # Вычисляем Евклидово расстояние
        euclidean_distance = euclidean(vacancy_vector, discipline_vector)
        percent_dissimilarity = euclidean_distance * 100
        formatted_percent = f"{100 - percent_dissimilarity:.2f}%"

        # Добавляем результаты в таблицу
        self.result_table.insertRow(self.result_table.rowCount())
        self.result_table.setItem(self.result_table.rowCount() - 1, 0, 
                                QTableWidgetItem("Евклидово расстояние"))
        self.result_table.setItem(self.result_table.rowCount() - 1, 1,
                                QTableWidgetItem(formatted_percent))
        self.result_table.setItem(self.result_table.rowCount() - 1, 2, 
                                QTableWidgetItem("Чем ближе значение к 100%, тем выше схожесть векторных представлений слов из разных моделей по данной метрике."))

        # Расстояние Чебышёва
        # Генерируем случайные индексы
        random_vacancy_index = random.randint(0, vacancy_vocab_size - 1)
        random_discipline_index = random.randint(0, discipline_vocab_size - 1)

        # Получаем случайные слова по индексам
        random_word_vacancy = self.vacancy_model.wv.index_to_key[random_vacancy_index]
        random_word_discipline = self.discipline_model.wv.index_to_key[random_discipline_index]

        # Извлекаем векторы слов
        vacancy_vector = self.vacancy_model.wv[random_word_vacancy]
        discipline_vector = self.discipline_model.wv[random_word_discipline]

        # Вычисляем расстояние Чебышёва
        chebyshev_distance = chebyshev(vacancy_vector, discipline_vector)
        percent_dissimilarity = chebyshev_distance * 100
        formatted_percent = f"{100 - percent_dissimilarity:.2f}%"

        # Добавляем результаты в таблицу
        self.result_table.insertRow(self.result_table.rowCount())
        self.result_table.setItem(self.result_table.rowCount() - 1, 0, 
                                QTableWidgetItem("Расстояние Чебышёва"))
        self.result_table.setItem(self.result_table.rowCount() - 1, 1,
                                QTableWidgetItem(formatted_percent))
        self.result_table.setItem(self.result_table.rowCount() - 1, 2,
                                QTableWidgetItem("Также показывает близость векторов."))

        # Сравнение наиболее похожих слов
        vacancy_vocab_size = len(self.vacancy_model.wv.key_to_index) 
        discipline_vocab_size = len(self.discipline_model.wv.key_to_index)

        # Генерируем случайные индексы
        random_vacancy_index1 = random.randint(0, vacancy_vocab_size - 1)
        random_vacancy_index2 = random.randint(0, vacancy_vocab_size - 1)
        random_discipline_index1 = random.randint(0, discipline_vocab_size - 1)
        random_discipline_index2 = random.randint(0, discipline_vocab_size - 1)

        # Получаем случайные слова по индексам
        random_word_vacancy_1 = self.vacancy_model.wv.index_to_key[random_vacancy_index1]
        random_word_vacancy_2 = self.vacancy_model.wv.index_to_key[random_vacancy_index2]
        random_word_discipline_1 = self.discipline_model.wv.index_to_key[random_discipline_index1] 
        random_word_discipline_2 = self.discipline_model.wv.index_to_key[random_discipline_index2]
        
        # Получаем размер словарей моделей 
        vacancy_vocab_size = len(self.vacancy_model.wv.key_to_index)
        discipline_vocab_size = len(self.discipline_model.wv.key_to_index)

        # Генерируем случайные индексы
        random_vacancy_index = random.randint(0, vacancy_vocab_size - 1)
        random_discipline_index = random.randint(0, discipline_vocab_size - 1)

        # Получаем случайные слова по индексам  
        random_word_vacancy = self.vacancy_model.wv.index_to_key[random_vacancy_index]
        random_word_discipline = self.discipline_model.wv.index_to_key[random_discipline_index]

        # Извлекаем векторы слов
        vacancy_vector = self.vacancy_model.wv.get_vector(random_word_vacancy)
        discipline_vector = self.discipline_model.wv.get_vector(random_word_discipline)

        # Вычисляем косинусное сходство
        cosine_similarity = 1 - cosine(vacancy_vector, discipline_vector)
        percent_similarity = (abs(cosine_similarity) * 100)
        formatted_percent = f"{100 - percent_similarity:.2f}%"

        # Добавляем результат в таблицу 
        self.result_table.insertRow(self.result_table.rowCount())
        self.result_table.setItem(self.result_table.rowCount() - 1, 0, 
                                QTableWidgetItem("Проецирование в общее пространство"))
        self.result_table.setItem(self.result_table.rowCount() - 1, 1, 
                                QTableWidgetItem(formatted_percent))
        self.result_table.setItem(self.result_table.rowCount() - 1, 2,
                                QTableWidgetItem("Приведение векторов из разных моделей в общее векторное пространство."))

    # Создание графика           
    def plot_graphs(self):
        if self.vacancy_model is None or self.discipline_model is None:
            QMessageBox.critical(self, "Ошибка", "Модели не загружены.")
            return

        num_words = 20  # Количество слов для отображения на графике

        # Получаем самые частые слова из моделей
        vacancy_top_words = self.vacancy_model.wv.index_to_key[:num_words]
        discipline_top_words = self.discipline_model.wv.index_to_key[:num_words]

        words = []
        similarities = []

        for word_vacancy, word_discipline in zip(vacancy_top_words, discipline_top_words):
            # Извлекаем векторы слов
            vacancy_vector = self.vacancy_model.wv[word_vacancy]
            discipline_vector = self.discipline_model.wv[word_discipline]

            # Вычисляем косинусное сходство между векторами
            similarity = 1 - cosine(vacancy_vector, discipline_vector)

            # Масштабируем значение сходства
            similarity_scaled = (similarity + 1) / 2  # Приводим значение в диапазон [0, 1]

            # Добавляем результаты в списки
            words.append(f"{word_vacancy} - {word_discipline}")
            similarities.append(similarity_scaled)

        # Создание и настройка графика
        fig, ax = plt.subplots()
        ax.bar(words, similarities)
        ax.set_xlabel("Слова")
        ax.set_ylabel("Сходство")
        ax.set_title("Сравнение слов моделей")
        ax.set_xticklabels(words, rotation=45, ha="right")

        # Настройка отступов и размещения элементов графика
        plt.tight_layout()

        # Отображение графика
        plt.show()