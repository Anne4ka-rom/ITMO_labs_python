from setuptools import setup, Extension # импортируем setup и Extension для создания Python-пакетов
from Cython.Build import cythonize # импортируем cythonize для компиляции Cython-модулей
import numpy as np # импортируем numpy, хотя в данном скрипте не используется напрямую


extra_compile_args = ['/openmp']  # Для MSVC -- флаг для включения поддержки OpenMP в компиляторе Microsoft
extra_link_args = ['/openmp'] # флаг для линковщика -- также включает поддержку OpenMP

# создаем список расширений для компиляции
extensions = [
    Extension( # создаем объект Extension для описания компилируемого модуля
        "integrate_cy", # имя модуля, который будет импортироваться в Python
        ["integrate_cy.pyx"], # список исходных файлов на Cython
        extra_compile_args=extra_compile_args, # дополнительные флаги для компилятора
        extra_link_args=extra_link_args, # дополнительные флаги для линковщика
    )
]

# вызываем функцию setup для конфигурации и сборки пакета
setup(
    name="integrate_cython", # имя пакета для установки через pip
    ext_modules=cythonize( # передаем результат функции cythonize как список модулей для компиляции
        extensions, # список объектов Extension для компиляции
        annotate=True,  # Для HTML отчета -- генерировать аннотированный HTML-файл для анализа кода
        compiler_directives={ # передаем директивы компилятора Cython
            'language_level': "3", # указываем версию Python
            'boundscheck': False, # отключаем проверку границ массивов для повышения производительности
            'wraparound': False, # отключаем поддержку отрицательных индексов в массивах для ускорения
        }
    ),
)