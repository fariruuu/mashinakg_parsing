import requests
import csv
from bs4 import BeautifulSoup as bs


def get_html(url):
    response = requests.get(url)
    return response.text  # GET запрос на заданный URL и возвращает HTML код в виде текста

def get_total_pages(html):
    soup = bs(html, 'lxml')
    page_list = soup.find('ul', class_="pagination").find_all('a')[-1].attrs.get('data-page')
    if page_list is not None:
        return int(page_list)
    else:
        return 0  # использован BeautifulSoup для нахождения и извлечения количества страниц  на сайте,т.е пагинация
# Если пагинация не будет найдена возвращает 1

def get_data(html):
    soup = bs(html, 'lxml')
    carlist = soup.find('div', class_='table-view-list').find_all('div', class_='list-item list-label')

# извлечение информации о машинах с каждой страницы

    for cars in carlist:
        try:
            title = cars.find('div', class_="block title").find('h2').text.strip()
        except AttributeError:
            title = ''

        try:
            pricebucks = cars.find('div', class_='price').find('strong').text.split()
            pricebucks = ' '.join(pricebucks)
        except AttributeError:
            pricebucks = ''

        try:
            price = cars.find('div', class_='price').find('p').text.replace(pricebucks, '').split()
            price = ' '.join(price)
        except AttributeError:
            price = ''

        try:
            image = cars.find('div', class_='thumb-item-carousel').find('img').attrs.get('data-src')
        except:
            image = ''

        try:
            description = cars.find('div', class_='block info-wrapper item-info-wrapper').text.split()
            description = ''.join(description)
        except AttributeError:
            description = ''

        product_dict = {
            'title': title,
            'pricebucks': pricebucks,
            'price': price,
            'image': image,
            'description': description
        }

        write_to_csv(product_dict)

# запись данных машин в csv файл

def main():
    url = 'https://www.mashina.kg/search/all/'
    html = get_html(url)
    get_data(html)
    number = get_total_pages(html)
    
    for i in range(2, number + 1):
        url_with_page = url + f'?page={str(i)}'
        print(url_with_page)  # Выводим URL каждой страницы для проверки
        html = get_html(url_with_page)
        get_data(html)

def write_to_csv(data):
    with open('data.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow([data['title'], data['pricebucks'], data['price'], data['image'], data['description']])
        # writerow принимает список значений, которые будут записаны в строку CSV-файла.
main()

