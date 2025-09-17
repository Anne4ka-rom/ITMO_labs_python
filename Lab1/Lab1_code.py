# создаём функцию target с исходным списком nums и числом, которое нужно получить target
def target(nums: list[int], target: int): 
    l = [] # создаём список, в который будем заносить списки индексов
    for num in nums: # цикл: пока число num в списке чисел nums
        if isinstance(num, int) and isinstance(target, int): # проверяем, что число num и число target - целые
            m = target - num # находим число m, которое в сумме с числом num даёт target
            if m in nums: # прооверяем, что число num в списке чисел nums
                index_num = nums.index(num) # находим индекс числа num в списке nums
                nums[index_num] = -10 ** 9 - 1 # заменяем число num в списке nums на число меньше минимума (по условию минимум: -10**9)
                if m in nums: # делаем ещё одну проверку, что число m в списке nums(так мы исключаем, что число m и число num имеют один и тот же индекс)
                    index_m = nums.index(m) # находим индекс числа m в списке nums
                    if index_m != index_num: # проверяем, что индекс числа m не равен индексу числа num
                        l.append([index_num, index_m]) # добавляем список полученных индексов в большой список l
    if len(l) > 0: # проверяем, что в списке l лежит больше 0 списков индексов
        return min(l) # возвращаем минимальную пару индексов
    else:
        return None # возвращаем None
    
                

result = target([3,3, 3, 3], 6) # результат записываем в переменную result
print(result) # выводим результат