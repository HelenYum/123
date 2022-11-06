import requests
from bs4 import BeautifulSoup
import csv

CSV = 'card.csv'
HOST = "https://myfin.by"
URL = "https://myfin.by/karty"
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
}

def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=";") # delimiter - разделитель
        writer.writerow(['Card name', 'Link product', 'Bank', 'Image card link'])  #указываем заголовки столбцов в которые будем записывать данные

        for item in items: # записываем строки в верные столбцы
            writer.writerow([item['title'], item['link_product'], item['bank'], item['card_image']])

def get_html(url, params=""):
    request = requests.get(url, headers=HEADERS, params=params)
    return request


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='products__product-main-info')
    cards = []

    for item in items:
        cards.append(
            {
                'title': item.find('div', class_='products__product-product-name').get_text(strip=True),
                'link_product': HOST + item.find('div', class_='products__product-product-name').find('a').get('href'),
                'bank': item.find('div', class_='products__product-bank-name').get_text(strip=True),
                'card_image': HOST + item.find('div', class_='products__product-logo').find('img').get('src')
                # конкатенируем ссылку
            }
        )
    return cards


def parser():
    PAGENATION = int(input("Enter the number of pages to parse: ").strip())
    html = get_html(URL)
    if html.status_code == 200:
        cards = []
        for page in range(1, PAGENATION):
            print(f'Parsing....  {page} page')
            html = get_html(URL, params={'page': page})
            cards.extend(get_content(html.text))
            save_file(cards, CSV)

    else:
        print("Error")

# html = get_html(URL)
# print(get_content(html.text))

# products__product    products__product--extended
parser()