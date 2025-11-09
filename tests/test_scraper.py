import pytest

# Импорт вашей функции scrape_books
from ваш_модуль import scrape_books

def test_books_list_type():
    books = scrape_books(is_save=False)
    assert isinstance(books, list), "Результат должен быть списком"

def test_dict_structure():
    books = scrape_books(is_save=False)
    assert len(books) > 0, "Список должен быть непустым"
    for book in books:
        assert isinstance(book, dict), "Каждый элемент должен быть словарём"
        required_keys = {'title', 'price', 'link'}
        assert required_keys.issubset(book.keys()), "Отсутствуют нужные ключи"

def test_title_validity():
    books = scrape_books(is_save=False)
    for book in books:
        assert type(book['title']) is str and len(book['title']) > 0, "Заголовок книги невалиден"

def test_books_count():
    books = scrape_books(is_save=False)
    # Ожидаем, что количество книг на первой странице не менее 10 (можно скорректировать)
    assert len(books) >= 10, "Собрано слишком мало книг"
