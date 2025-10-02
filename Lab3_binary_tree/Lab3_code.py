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

def gen_bin_tree(height: int, root: int):
    '''Функция рекурсивно генерирующая дерево.
    
    Ключевые аргументы:
    height -- высота дерева
    root -- корень дерева'''
    if isinstance(height, int) and isinstance(root, int) and height >= 0: # проверяем, что height и root - целые числа и высота height больше или равна
        if height == 0: # если высота height равна 0
            return {root: []} # выходим из рекурсии и возвращаем последнюю нужную ветку дерева
        g = {root: [gen_bin_tree(height=height - 1, root=left_leaf(root)), gen_bin_tree(height=height - 1, root=right_leaf(root))]} # в другом случае создаём словарь g, в котором рекурсивно тзадаём правую и левую ветки дерева
        return g # возвращаем словарь g
    else:
        return None # в противно случае возвращаем None

print(gen_bin_tree(3, 11)) # печатаем дерево с заданными параметрами