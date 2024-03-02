import requests
import re

from decorators import benchmark, counter, logging, memo

BOOK_PATH = 'https://www.gutenberg.org/files/2638/2638-0.txt'
BOOK_PATH2 = 'https://www.gutenberg.org/files/5827/5827-8.txt'

@counter
@logging
@benchmark
def word_count(word, url=BOOK_PATH):
    """
    Функция для посчета указанного слова на html-странице
    """

    # отправляем запрос в библиотеку Gutenberg и забираем текст
    raw = requests.get(url).text

    # заменяем в тексте все небуквенные символы на пробелы
    processed_book = re.sub('[\W]+' , ' ', raw).lower()

    # считаем
    cnt = len(re.findall(word.lower(), processed_book))

    return f"Cлово {word} встречается {cnt} раз"


print(word_count('whole'))
print(word_count('knowledge', url=BOOK_PATH2))


# вариант без кэширования
# используется вложенная ф-я _fib, чтобы замерять время выполнения в целом, а не каждого рекурсивного вызова
@benchmark
def fib(n):
    def _fib(n):
        if n < 2:
            return n
        return _fib(n-2) + _fib(n-1)
    
    return _fib(n)

# измеряем время выполнения
result1 = fib(30)

# вариант с кэшированием
# такая же вложенная ф-я, но результаты промежуточных рекурсивных вызовов будут запомнены
@benchmark
def fib_cached(n):
    @memo
    def _fib(n):
        if n < 2:
            return n
        return _fib(n-2) + _fib(n-1)
    
    return _fib(n)

# измеряем время выполнения с кэшированием
# время выполнения должно значительно уменьшиться
result2 = fib_cached(30)

# проверяем, что результаты сходятся
assert result1 == result2
