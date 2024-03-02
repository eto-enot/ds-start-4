from functools import wraps
import time
import typing


def benchmark(func):
    """
    Декоратор, выводящий время, которое заняло выполнение декорируемой функции
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter() 
        result = func(*args, **kwargs)
        tm = time.perf_counter() - start
        print(f"Время выполнения функции {func.__name__}: {tm:.17f}")
        return result

    return wrapper


def logging(func):
    """
    Декоратор, который выводит параметры с которыми была вызвана функция
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"Функция вызвана с параметрами: {args}, {kwargs}")
        return result

    return wrapper


def counter(func):
    """
    Декоратор, считающий и выводящий количество вызовов декорируемой функции
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        # кол-во вызовов храним в объекте декоратора
        wrapper.count += 1
        print(f"Функция была вызывана {wrapper.count} раз")
        return result

    # задаем начальное значение счетчика в декораторе
    wrapper.count = 0
    return wrapper


def memo(func):
    """
    Декоратор, запоминающий результаты исполнения функции func,
    чьи аргументы args должны быть хешируемыми
    """

    @wraps(func)
    def fmemo(*args):
        # проверяем, что переданные аргументы хэшируемые
        if all(isinstance(arg, typing.Hashable) for arg in args):
            # если да, то их можно использовать как ключ в словаре fmemo.cache
            if args in fmemo.cache:
                # если аргумент уже в кэше, возвращаем сохраненное значение
                result = fmemo.cache[args]
            else:
                # иначе сохраняем результат ф-ии и возвращаем его
                result = fmemo.cache[args] = func(*args)
            return result
        else:
            # если аргументы не хэшируемые, просто вызываем ф-ю
            return func(*args)

    fmemo.cache = {}
    return fmemo
