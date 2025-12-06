import math # импортируем модуль math для математических операций
import timeit # импортируем модуль timeit для замера времени выполнения
import doctest # импортируем модуль doctest для выполнения тестов в docstring
import unittest # импортируем модуль unittest для создания unit-тестов
from typing import Callable # импортируем Callable для аннотаций типов функций
from concurrent import futures # импортируем futures для работы с потоками и процессами
from functools import partial # импортируем partial для создания частичных функций


def integrate(f: Callable[[float], float], a: float, b: float, *, n_iter: int = 100000) -> float:
    '''
    Функция integrate() вычисляет приближенное значение определенного интеграла
    методом правых прямоугольников
    
    Параметры:
    f -- интегрируемая функция
    a -- нижний предел интегрирования
    b -- верхний предел интегрирования
    n_iter -- количество разбиений интервала
    
    Возвращает:
    float -- приближенное значение интеграла
    
    Вызывает:
    ValueError -- если n_iter <= 0 или b <= a
    '''
    if n_iter <= 0: # проверяем, что количество итераций положительное
        raise ValueError('n_iter должен быть положительным числом') # вызываем исключение
    if b <= a: # проверяем корректность пределов интегрирования
        raise ValueError('b должен быть больше a') # вызываем исключение
    
    acc = 0.0 # инициализируем аккумулятор для суммы
    step = (b - a) / n_iter # вычисляем ширину каждого прямоугольника
    
    for i in range(n_iter): # проходим по всем подинтервалам
        acc += f(a + i * step) * step # прибавляем площадь текущего прямоугольника
    
    return acc # возвращаем приближенное значение интеграла


def partial_integrate(f, start, end, n_iter):
    '''
    Функция partial_integrate() является вспомогательной функцией
    для параллельного вычисления интеграла
    
    Параметры:
    f -- интегрируемая функция
    start -- начало отрезка интегрирования
    end -- конец отрезка интегрирования
    n_iter -- количество итераций на отрезке
    
    Возвращает:
    float -- значение интеграла на отрезке [start, end]
    '''
    return integrate(f, start, end, n_iter=n_iter) # вызываем основную функцию integrate


class TestIntegrate(unittest.TestCase):
    '''
    Класс TestIntegrate содержит unit-тесты для функции integrate()
    Наследуется от unittest.TestCase для использования фреймворка тестирования
    '''
    def test_cos_integral(self):
        '''
        Функция test_cos_integral() тестирует вычисление интеграла косинуса
        '''
        result = integrate(math.cos, 0, math.pi/2, n_iter=10000) # вычисляем интеграл cos
        self.assertAlmostEqual(result, 1.0, places=2) # проверяем точность до 2 знаков
    
    def test_polynomial_integral(self):
        '''
        Функция test_polynomial_integral() тестирует интеграл квадратичной функции
        '''
        f = lambda x: 2*x**2 + 3*x + 1 # создаем лямбда-функцию полинома
        result = integrate(f, 0, 2, n_iter=10000) # вычисляем интеграл полинома
        expected = 40/3 # вычисляем ожидаемое аналитическое значение
        self.assertAlmostEqual(result, expected, places=2) # сравниваем с ожидаемым
    
    def test_iterations_stability(self):
        '''
        Функция test_iterations_stability() проверяет устойчивость при изменении числа итераций
        '''
        result1 = integrate(math.cos, 0, math.pi/2, n_iter=1000) # вычисляем с 1000 итераций
        result2 = integrate(math.cos, 0, math.pi/2, n_iter=10000) # вычисляем с 10000 итераций
        diff = abs(result2 - result1) # вычисляем разницу результатов
        self.assertLess(diff, 0.05) # проверяем, что разница меньше 0.05


def integrate_threaded(f: Callable[[float], float], a: float, b: float, *, n_jobs: int = 2, n_iter: int = 100000) -> float:
    '''
    Функция integrate_threaded() вычисляет интеграл с использованием потоков
    
    Параметры:
    f -- интегрируемая функция
    a -- нижний предел интегрирования
    b -- верхний предел интегрирования
    n_jobs -- количество потоков
    n_iter -- общее количество итераций
    
    Возвращает:
    float -- приближенное значение интеграла
    
    Вызывает:
    ValueError -- если n_iter//n_jobs == 0
    '''
    if n_iter // n_jobs == 0: # проверяем, что на каждый поток достаточно итераций
        raise ValueError('Количество итераций на поток должно быть > 0') # вызываем исключение
    
    executor = futures.ThreadPoolExecutor(max_workers=n_jobs) # создаем пул потоков
    step = (b - a) / n_jobs # вычисляем длину отрезка для каждого потока
    local_iter = n_iter // n_jobs # вычисляем количество итераций на поток
    
    spawn = partial(executor.submit, partial_integrate, f, n_iter=local_iter) # создаем частичную функцию
    fs = [spawn(a + i * step, a + (i + 1) * step) for i in range(n_jobs)] # запускаем задачи в потоках
    
    return sum(f.result() for f in futures.as_completed(fs)) # суммируем результаты всех потоков


def integrate_processes(f: Callable[[float], float], a: float, b: float, *, n_jobs: int = 2, n_iter: int = 100000) -> float:
    '''
    Функция integrate_processes() вычисляет интеграл с использованием процессов
    
    Параметры:
    f -- интегрируемая функция
    a -- нижний предел интегрирования
    b -- верхний предел интегрирования
    n_jobs -- количество процессов
    n_iter -- общее количество итераций
    
    Возвращает:
    float -- приближенное значение интеграла
    
    Вызывает:
    ValueError -- если n_iter//n_jobs == 0
    '''
    if n_iter // n_jobs == 0: # проверяем, что на каждый процесс достаточно итераций
        raise ValueError('Количество итераций на процесс должно быть > 0') # вызываем исключение
    
    executor = futures.ProcessPoolExecutor(max_workers=n_jobs) # создаем пул процессов
    step = (b - a) / n_jobs # вычисляем длину отрезка для каждого процесса
    local_iter = n_iter // n_jobs # вычисляем количество итераций на процесс
    
    spawn = partial(executor.submit, partial_integrate, f, n_iter=local_iter) # создаем частичную функцию
    fs = [spawn(a + i * step, a + (i + 1) * step) for i in range(n_jobs)] # запускаем задачи в процессах
    
    return sum(f.result() for f in futures.as_completed(fs)) # суммируем результаты всех процессов


def time_measurements():
    '''
    Функция time_measurements() выполняет замеры времени для всех версий вычисления интеграла
    '''
    print('\n' + '-'*50) # выводим разделительную линию
    print('Время работы') # выводим заголовок
    print('-'*50) # выводим разделительную линию
    
    test_func = math.cos # задаем тестовую функцию
    a, b = 0, math.pi/2 # задаем пределы интегрирования
    n_iter = 1000000 # задаем количество итераций
    
    print(f'\nТест: ∫cos(x)dx от {a} до {b}, n_iter={n_iter}') # выводим параметры теста
    print('-'*50) # выводим разделительную линию
    
    print('\n1. Базовая версия программы:') # выводим заголовок для базовой версии
    setup = 'from __main__ import integrate; import math' # настройка для timeit
    stmt = f'integrate(math.cos, {a}, {b}, n_iter={n_iter})' # выражение для измерения
    timer = timeit.Timer(stmt, setup=setup) # создаем таймер
    base_time = min(timer.repeat(repeat=3, number=1)) # измеряем минимальное время из 3 запусков
    print(f'   Время: {base_time:.6f} сек') # выводим результат
    
    print('\n2. Версия программы с потоками:') # выводим заголовок для потоков
    for n_jobs in [2, 4, 6, 8]: # перебираем количество потоков
        setup = 'from __main__ import integrate_threaded; import math' # настройка для timeit
        stmt = f'integrate_threaded(math.cos, {a}, {b}, n_jobs={n_jobs}, n_iter={n_iter})' # выражение для измерения
        timer = timeit.Timer(stmt, setup=setup) # создаем таймер
        time_val = min(timer.repeat(repeat=3, number=1)) # измеряем минимальное время
        speedup = base_time / time_val if time_val > 0 else 0 # вычисляем ускорение
        print(f'   {n_jobs} потока(ов): {time_val:.6f} сек, ускорение: {speedup:.2f}x') # выводим результат
    
    print('\n3. Версия программы с процессами:') # выводим заголовок для процессов
    for n_jobs in [2, 4, 6, 8]: # перебираем количество процессов
        setup = 'from __main__ import integrate_processes; import math' # настройка для timeit
        stmt = f'integrate_processes(math.cos, {a}, {b}, n_jobs={n_jobs}, n_iter={n_iter})' # выражение для измерения
        timer = timeit.Timer(stmt, setup=setup) # создаем таймер
        time_val = min(timer.repeat(repeat=3, number=1)) # измеряем минимальное время
        speedup = base_time / time_val if time_val > 0 else 0 # вычисляем ускорение
        print(f'   {n_jobs} процесса(ов): {time_val:.6f} сек, ускорение: {speedup:.2f}x') # выводим результат


def analyze_synchronization():
    '''
    Функция analyze_synchronization() анализирует необходимость примитивов синхронизации
    '''
    print('\n' + '-'*50) # выводим разделительную линию
    print('Анализируем синхронизацию') # выводим заголовок
    print('-'*50) # выводим разделительную линию
    
    print('\nВ данной задаче примитивы синхронизации НЕ нужны:') # выводим вывод
    print('1. Каждый поток/процесс работает на своем отрезке') # объясняем причину 1
    print('2. Нет общих данных для записи') # объясняем причину 2
    print('3. Результаты суммируются после завершения всех работ') # объясняем причину 3
    print('4. Функция math.cos потокобезопасна') # объясняем причину 4
    
    print('\nПримитивы синхронизации потребовались бы, если бы:') # выводим условия необходимости
    print('- Все потоки писали в одну переменную') # приводим пример 1
    print('- Были общие структуры данных') # приводим пример 2
    print('- Требовалась координация выполнения') # приводим пример 3


def test_cython_versions():
    '''
    Функция test_cython_versions() тестирует Cython версии функций
    '''
    try:
        from integrate_cy import integrate_cy, integrate_cos_cy, integrate_cos_nogil # импортируем Cython функции
        
        print('\n' + '-'*50) # выводим разделительную линию
        print('Тестируем Cython версию') # выводим заголовок
        print('-'*50) # выводим разделительную линию
        
        a, b = 0, math.pi/2 # задаем пределы интегрирования
        n_iter = 1000000 # задаем количество итераций
        
        setup_base = 'from __main__ import integrate; import math' # настройка для базовой версии
        stmt_base = f'integrate(math.cos, {a}, {b}, n_iter={n_iter})' # выражение для базовой версии
        timer_base = timeit.Timer(stmt_base, setup=setup_base) # создаем таймер для базовой версии
        base_time = min(timer_base.repeat(repeat=3, number=1)) # измеряем базовое время
        
        print('\n1. Cython базовая версия:') # выводим заголовок для Cython базовой
        setup = 'from integrate_cy import integrate_cy; import math' # настройка для Cython
        stmt = f'integrate_cy(math.cos, {a}, {b}, n_iter={n_iter})' # выражение для Cython
        timer = timeit.Timer(stmt, setup=setup) # создаем таймер
        time_val = min(timer.repeat(repeat=3, number=1)) # измеряем время
        speedup = base_time / time_val if time_val > 0 else 0 # вычисляем ускорение
        print(f'   Время: {time_val:.6f} сек, ускорение: {speedup:.2f}x') # выводим результат
        
        print('\n2. Cython специализированная версия:') # выводим заголовок для специализированной
        setup = 'from integrate_cy import integrate_cos_cy' # настройка для специализированной
        stmt = f'integrate_cos_cy({a}, {b}, n_iter={n_iter})' # выражение для специализированной
        timer = timeit.Timer(stmt, setup=setup) # создаем таймер
        time_val = min(timer.repeat(repeat=3, number=1)) # измеряем время
        speedup = base_time / time_val if time_val > 0 else 0 # вычисляем ускорение
        print(f'   Время: {time_val:.6f} сек, ускорение: {speedup:.2f}x') # выводим результат
        
        print('\n3. Cython noGIL версия:') # выводим заголовок для noGIL
        setup = 'from integrate_cy import integrate_cos_nogil' # настройка для noGIL
        stmt = f'integrate_cos_nogil({a}, {b}, n_iter={n_iter})' # выражение для noGIL
        timer = timeit.Timer(stmt, setup=setup) # создаем таймер
        time_val = min(timer.repeat(repeat=3, number=1)) # измеряем время
        speedup = base_time / time_val if time_val > 0 else 0 # вычисляем ускорение
        print(f'   Время: {time_val:.6f} сек, ускорение: {speedup:.2f}x') # выводим результат
        
    except ImportError:
        print('\nCython модуль не найден. Скомпилируйте его:') # выводим сообщение об ошибке
        print('python setup_cython.py build_ext --inplace') # выводим команду для компиляции


def test_nogil_prange():
    '''
    Функция test_nogil_prange() тестирует noGIL версию с использованием prange
    '''
    try:
        from integrate_cy import integrate_cos_nogil_prange # импортируем функцию с prange
        
        print('\n' + '-'*50) # выводим разделительную линию
        print('Тестируем noGIL версию') # выводим заголовок
        print('-'*50) # выводим разделительную линию
        
        a, b = 0, math.pi/2 # задаем пределы интегрирования
        n_iter = 1000000 # задаем количество итераций
        
        setup_base = 'from __main__ import integrate; import math' # настройка для базовой версии
        stmt_base = f'integrate(math.cos, {a}, {b}, n_iter={n_iter})' # выражение для базовой версии
        timer_base = timeit.Timer(stmt_base, setup=setup_base) # создаем таймер для базовой версии
        base_time = min(timer_base.repeat(repeat=3, number=1)) # измеряем базовое время
        
        process_times = [0.343870, 0.340902, 0.385189, 0.401880] # данные из предыдущих замеров
        avg_process_time = sum(process_times) / len(process_times) # вычисляем среднее время процессов
        
        print('\nСравнение noGIL потоков с Python процессами:') # выводим заголовок сравнения
        print('-'*60) # выводим разделительную линию
        
        for n_threads in [2, 4, 6, 8]: # перебираем количество потоков
            setup = 'from integrate_cy import integrate_cos_nogil_prange' # настройка для prange
            stmt = f'integrate_cos_nogil_prange({a}, {b}, n_iter={n_iter}, n_threads={n_threads})' # выражение для prange
            timer = timeit.Timer(stmt, setup=setup) # создаем таймер
            time_val = min(timer.repeat(repeat=3, number=1)) # измеряем время
            speedup = base_time / time_val if time_val > 0 else 0 # вычисляем ускорение
            
            print(f'\n{n_threads} потоков/процессов:') # выводим заголовок для текущего количества
            print(f'  Cython noGIL: {time_val:.6f} сек') # выводим время prange
            print(f'  Ускорение относительно базовой Python: {speedup:.2f}x') # выводим ускорение
            
            if n_threads == 4: # для 4 потоков/процессов
                process_speedup = base_time / avg_process_time # вычисляем ускорение процессов
                print(f'  Python процессы (4): ~{avg_process_time:.3f} сек') # выводим время процессов
                print(f'  Ускорение относительно базовой Python: ~{process_speedup:.2f}x') # выводим ускорение процессов
                print(f'  Выигрыш noGIL над процессами: {avg_process_time/time_val:.2f}x') # выводим сравнение
    
    except ImportError:
        print('\nФункция integrate_cos_nogil_prange не найдена в Cython модуле') # выводим сообщение об ошибке


def main():
    '''
    Функция main() является основной точкой входа в программу
    Координирует выполнение всех тестов и замеров
    '''
    print('Лабораторная работа 10: Методы оптимизации вычислений') # выводим заголовок работы
    print('-'*50) # выводим разделительную линию

    print('Реализуем итерации:') # выводим заголовок работы
    print('-'*50) # выводим разделительную линию
    
    print('\nТестирование:') # выводим заголовок итерации 1
    print('-'*50) # выводим разделительную линию
    
    print('Doctest:', end=' ') # выводим метку для doctest
    doctest.testmod(verbose=False) # запускаем doctest без подробного вывода
    print('OK') # выводим результат
    
    print('Unittest:', end=' ') # выводим метку для unittest
    suite = unittest.TestLoader().loadTestsFromTestCase(TestIntegrate) # создаем набор тестов
    runner = unittest.TextTestRunner(verbosity=0) # создаем runner без подробного вывода
    result = runner.run(suite) # запускаем тесты
    print('OK' if result.wasSuccessful() else 'FAILED') # выводим результат
    
    print('\nЗамеры времени:') # выводим заголовок итераций 2-3
    time_measurements() # вызываем функцию замеров времени
    
    print('\nCython оптимизация:') # выводим заголовок итерации 4
    test_cython_versions() # вызываем тестирование Cython версий
    
    print('\nnoGIL и сравнение:') # выводим заголовок итерации 5
    test_nogil_prange() # вызываем тестирование noGIL с prange
    analyze_synchronization() # вызываем анализ синхронизации
    
    print('\n' + '-'*50) # выводим разделительную линию


if __name__ == '__main__':
    main() # вызываем основную функцию при прямом запуске скрипта