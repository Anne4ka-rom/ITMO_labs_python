from collections import deque as dq # импортируем двустороннюю очередь (deque) из библиотеки collections и даём её короткое имя -- dq
'''Двусторонняя очередь (deque) -- позволяет добавлять элемент и в начало очереди, и в конец, 
а также удалять/брать элемент из начала или конца очереди'''
import timeit # импортируем библиотеку timeit для точного измерения различных фрагментов кода
import matplotlib.pyplot as plt # импортируем библиотеку matplotlib.pyplot для создания графиков и даём её короткое имя -- plt

'''БЛОК ФУНКЦИЙ ДЛЯ РЕКУРСИВНОГО МЕТОДА'''
def left_leaf (root: int):
    '''Левая ветка нашего дерева.
    
    Ключевые аргументы:
    root -- корень дерева'''
    return root ** 2 # возвращаем условие, задающее левую ветку дерева

def right_leaf(root: int):
    '''Правая ветка нашего дерева.
    
    Ключевые аргументы:
    root -- корень дерева'''
    return 2 + root ** 2 # возвращаем условие, задающее правую ветку дерева

def build_tree_recursive(height: int, root: int):
    '''Функция рекурсивно генерирующая дерево.
    
    Ключевые аргументы:
    height -- высота дерева
    root -- корень дерева'''
    if isinstance(height, int) and isinstance(root, int) and height >= 0: # проверяем, что height и root - целые числа и высота height больше или равна
        if height == 0: # если высота height равна 0
            return {root: []} # выходим из рекурсии и возвращаем последнюю нужную ветку дерева
        g = {root: [build_tree_recursive(height=height - 1, root=left_leaf(root)), build_tree_recursive(height=height - 1, root=right_leaf(root))]} # в другом случае создаём словарь g, в котором рекурсивно тзадаём правую и левую ветки дерева
        return g # возвращаем словарь g
    else:
        return None # в противно случае возвращаем None

time_recursive = timeit.timeit(lambda: build_tree_recursive(3, 11), number=10000) # создаём переменную time_recursive, которая хранит время выполнения рекурсивной функции: lambda: build_tree_recursive(3, 11) -- анонимная функция, вызывающая рекурсивную функцию создания бинарного дерева, number=10000 -- количество повторений этого вызова

'''БЛОК ФУНКЦИЙ ДЛЯ НЕРЕКУРСИВНОГО МЕТОДА'''
def build_tree_iterative(height: int, root: int, left_branch = lambda l_b: l_b ** 2, right_branch = lambda r_b: 2 + r_b ** 2):
    '''Функция get_bin_tree получает на вход ключевые аргументы и с их помощью строит бинарное дерево 
    с заданным корнем, высотой и функциями для двух ветвей НЕ рекурсивным методом
    
    Ключевые аргументы:
    height -- высота дарева (количество вершин на одной ветви)
    root -- корень дерева (число, к которому будем применять функции построения вершин ветвей)
    left_branch -- функция для левой ветви дерева
    right_branch -- функция для правой ветви дерева'''
    
    result = {root: []} # создаём словарь result, в котором будут отображаться наши вершины и ветви, исходящии из них -- дерево

    if isinstance(height, int) and isinstance(root, int) and height >= 0: # проверяем: если высота height и корень root -- целые числа и высота height больше или равна 0
        if height == 0: # првоеряем: если высота -- 0
            return result # возвращаем результат из переменной result (0-ая вершина -- корень дерева)
        
        queue = dq([(root, 0, result[root])]) # создаём двойную очередь -- queue и задаём ей список из одного элемента -- кортежа: root -- текущее значение вершины, 0 -- уровень текущей высоты вершины (изначально у нас корень дерева, поэтому значение -- 0), result[root] -- список ветвей для текущей вершины
        
        while queue: # проверяем: пока условие, что в очереди queue есть хоть один элемент, верно
            value, height_value, branches_list = queue.popleft() # берём левый элемент очереди queue (кортеж из 3-ёх элементов) и присваеваем 3 значения кортежа переменным: value -- текущее значение вершины, height_value -- уровень текущей высоты вершины, branches_list -- список ветвей для текущей вершины
            
            if height_value < height: # проверяем: если текущая высота вершины строго меньше высоты дерева
                left_value = left_branch(value) # задаём вершину левой ветви -- left_value путём передачи функции left_branch значения текущей вершины value
                right_value = right_branch(value) # задаём вершину правой ветви -- right_value путём передачи функции right_branch значения текущей вершины value
                
                left_vertex = {left_value: []} # задаём ветвь левой вершины left_vertex путём создания словаря: left_value -- вершина левой ветви, которому принадлежит пустой список [] (будущие ветви)
                right_vertex = {right_value: []} # задаём ветвь правой вершины right_vertex путём создания словаря: right_vertex -- вершина правой ветви, которому принадлежит пустой список [] (будущие ветви)
                
                branches_list.extend([left_vertex, right_vertex]) # добавляем в список ветвей 2-а элемента(!): left_vertex -- левую вевь дерева и right_vertex -- правую ветвь дерева
                '''метод extend -- добавляет все элементы итерируемого объекта в конец списка
                
                Отличие от append: append добавляет объект, extend добавляет элементы'''

                queue.append((left_value, height_value + 1, left_vertex[left_value])) # добавляем в очередь queue кортеж элементов: left_value -- вершина левой ветви, height_value + 1 -- увеличиваем текущее значение высоты на 1, left_vertex[left_value] -- список ветвей для левой вершины
                queue.append((right_value, height_value + 1, right_vertex[right_value])) # добавляем в очередь queue кортеж элементов: right_value -- вершина правой ветви, height_value + 1 -- увеличиваем текущее значение высоты на 1, right_vertex[right_value] -- список ветвей для правой вершины
    
        return result # возвращаем результат result
    return None # в противно случае возвращаем None

time_iterative = timeit.timeit(lambda: build_tree_iterative(3, 11), number=10000) # создаём переменную time_iterative, которая хранит время выполнения нерекурсивной функции: lambda: build_tree_iterative(3, 11) -- анонимная функция, вызывающая нерекурсивную функцию создания бинарного дерева, number=10000 -- количество повторений этого вызова

def benchmark(function, height, root, repeat=1000):
    '''Возвращает среднее время выполнения function(height, root)
    
    Ключевые аргументы:
    function --
    height -- высота дерева
    root -- корень дерева
    repeat=1000 -- количество повторений функции function'''
    times = timeit.repeat(lambda: function(height, root), number=1, repeat=repeat) # создаём переменную times, которая выполняет многократные измерения времени выполнения анонимной функции lambda, вызывающей функцию function(height, root): number=1 -- за одно измерение выполняет функцию один раз, repeat=repeat -- повторяет процесс измерения
    return min(times) # возвращаем минимальное полученное время times

def main():
    '''Функция строит график зависимости времени выполнения рекурсивной и нерекурсивной функций от высоты дерева'''
    test_height = list(range(0, 10)) # создаем список высот деревьев test_height (значение высот от 0 до 10 включительно)

    res_recursive = [] # создаём список res_recursive, в котором будут содержаться значения времени для разных высот для рекурсивной функции
    res_iterative = [] # создаём список res_iterative, в котором будут содержаться значения времени для разных высот для нерекурсивной функции

    for height in test_height: # проходимся по всем высотам списка test_height
        res_recursive.append(benchmark(function=build_tree_recursive, height=height, root=11)) # добавляем в список res_recursive результат выполнения функции benchmark: build_tree_recursive -- рекурсивная функция, height -- текущая высота, root -- корень дерева
        res_iterative.append(benchmark(function=build_tree_iterative, height=height, root=11)) # добавляем в список res_iterative результат выполнения функции benchmark: build_tree_iterative -- рекурсивная функция, height -- текущая высота, root -- корень дерева

    plt.plot(test_height, res_recursive, label="Рекурсивный") # создаём график для рекурсивной версии: test_height -- значения по оси X (высот деревьев),res_recursive -- значения по оси Y (время выполнения функции в секундах), label="Рекурсивный" -- подпись графика
    plt.plot(test_height, res_iterative, label="Нерекурсивный") # создаём график для нерекурсивной версии: test_height -- значения по оси X (высот деревьев),res_iterative -- значения по оси Y (время выполнения функции в секундах), label="Нерекурсивный" -- подпись графика
    plt.xlabel("Высота дерева") # подпись оси X
    plt.ylabel("Время выполнения функции (сек)") # подпись оси Y
    plt.title("Сравнение рекурсивной и нерекурсивной функции построения бинарного дерева") # заголовок графика
    plt.legend() # добавление легенды на график (показывает какой график каким цветом обозначен)
    plt.show() # отображение графика в отдельном окне

if __name__ == "__main__": # вызов функции main
    main()