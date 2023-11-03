# setup.py

import sys
from cx_Freeze import setup, Executable

# Список файлов и директорий, необходимых для включения в сборку
include_files = [
    "modules",
    "screenshoot",
    "auth_utils.py",
    "instruction.html",
    "logo.png",
    "mainwindow.py",
    "semantic_analysis_tab.py",
    "stopwords.txt",
    "styles.css",
    "word2vec_utils.py"
]

# Список зависимостей (библиотек), которые нужно включить
packages = [
    "PyQt5",
    "nltk",
    "matplotlib",
    "gensim",
    "openpyxl",
    "docx2txt",
    "PyPDF4",
    "stop_words"
]

# Создание исполняемого файла
setup(
    name="SA",
    version="0.1",
    description="Semantic analysis",
    options={
        "build_exe": {
            "packages": packages,
            "include_files": include_files
        }
    },
    executables=[Executable("app.py")]
)