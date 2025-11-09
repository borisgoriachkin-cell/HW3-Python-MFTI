import time
import requests
import schedule
from bs4 import BeautifulSoup

def get_book_data(book_url: str) -> dict:
    """
    Получает все основные данные о книге с одной страницы каталога Books to Scrape.

    Аргументы:
        book_url (str): URL страницы книги.

    Возвращает:
        dict: Словарь с подробной информацией о книге, включая название, цену, рейтинг,
              количество в наличии, описание и дополнительные характеристики из таблицы Product Information.
    """

    # НАЧАЛО ВАШЕГО РЕШЕНИЯ
    response = requests.get(book_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    # Название книги
    title = soup.h1.text

    # Цена
    price = soup.select_one('.price_color').text

    # В наличии
    availability = soup.select_one('.availability').text.strip()

    # Рейтинг (находится в виде класса, например: <p class="star-rating Three">)
    rating_tag = soup.select_one('.star-rating')
    rating = rating_tag['class'][1] if rating_tag else None

    # Описание (далеко не всегда есть; бывает во втором <p> после <div id="product_description">)
    desc_tag = soup.find('div', id='product_description')
    if desc_tag:
        description = desc_tag.find_next_sibling('p').text
    else:
        description = ''

    # Таблица "Product Information"
    product_table = soup.find('table', class_='table table-striped')
    product_info = {}
    if product_table:
        for row in product_table.find_all('tr'):
            key = row.th.text.strip()
            value = row.td.text.strip()
            product_info[key] = value

    # Итоговый словарь
    result = {
        'title': title,
        'price': price,
        'availability': availability,
        'rating': rating,
        'description': description,
        'product_info': product_info
    }
    return result

    # КОНЕЦ ВАШЕГО РЕШЕНИЯ

    from urllib.parse import urljoin
import json
def scrape_books(is_save=True):
    """
    Собирает данные о всех книгах с сайта Books to Scrape.
    Аргументы:
        save (bool): Если True, сохраняет результат в файл 'books_data.txt'.
    Возвращает:
        list: Список словарей с информацией о книгах.
    """
    # НАЧАЛО ВАШЕГО РЕШЕНИЯ
    books = []
    page_number = 1
    is_save = True
    while page_number < 200:
        url = f'http://books.toscrape.com/catalogue/page-{page_number}.html'
        response = requests.get(url)
        if response.status_code != 200:
            break
        soup = BeautifulSoup(response.text, 'html.parser')
        book_tags = soup.select('h3 a')
#    print(book_tags) # данная строка должна отработать всегда
        try:
            book_links = [urljoin('http://books.toscrape.com/catalogue/', tag['href']) for tag in book_tags]
#        print(book_links)
        except Exception as e:
            print('Ошибка при формировании book_links:', e)
        for link in book_links:
            try:
                book_data = get_book_data(link)
#            print(book_data)
                books.append(book_data)
#                print(len(books))
            except Exception as e:
                print(f"Ошибка при парсинге {link}: {e}")
#    print('page', page_number, 'book_links:', len(book_links))
        page_number += 1

#    print(f"Total books found: {len(books)}")
        if is_save:
            with open('books_data.txt', 'w', encoding='utf-8') as f:
                json.dump(books, f, ensure_ascii=False, indent=2)
    return books
    # КОНЕЦ ВАШЕГО РЕШЕНИЯ
#print('done')    
