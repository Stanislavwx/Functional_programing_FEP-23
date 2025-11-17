from itertools import islice
from streams import naturals, fib_stream, take, drop, sliding_window, moving_average, accumulate_sum

def demo():
    print("Перші 10 натуральних з 1:", list(islice(naturals(1), 10)))
    print("Перші 10 чисел Фібоначчі:", list(islice(fib_stream(), 10)))

    # Приклад take/drop над одним потоком
    xs = naturals(1)
    print("Перші 5 елементів:", take(5, xs))         # зсуває ітератор до 6
    print("Наступні 3 елементи:", take(3, xs))       # продовжуємо від 6

    # Пропустити перші 10 і взяти наступні 5
    ys = take(5, drop(10, naturals(0)))
    print("Пропустили 10, взяли 5:", ys)

    # Суми за ковзним вікном на натуральних
    win2 = sliding_window(naturals(1), 2)
    first5_window_sums = list(islice((sum(w) for w in win2), 5))
    print("Перші 5 сум вікна (k=2) над натуральними:", first5_window_sums)

    # Рухоме середнє на скінченному списку
    print("Рухоме середнє k=3 для [1,2,3,4,5]:", list(moving_average([1,2,3,4,5], 3)))

    # Префіксні суми через accumulate
    print("Префіксні суми для [1,2,3,4]:", list(accumulate_sum([1,2,3,4])))

if __name__ == "__main__":
    demo()
