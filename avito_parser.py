import requests
from bs4 import BeautifulSoup
import csv



def get_html(url):
    r = requests.get(url)
    return r.text


def get_pages_amount(html):
    soup = BeautifulSoup(html, 'lxml')

    pages = soup.find_all('span', class_ = "pagination-item-1WyVp")[-2].get('data-marker')
    total_pages = int(pages.split('(')[1].split(')')[0])
    return total_pages


def main():
    url =  'https://www.avito.ru/kazan/noutbuki?p=1&q=macbook'
    base_url = 'https://www.avito.ru/kazan/noutbuki?'
    page_part = 'p='
    query_part = '&q=macbook'

    total_pages = get_pages_amount(get_html(url))
    for i in range(1, total_pages):
        url_gen = base_url + page_part + str(i) + query_part
        get_page_data(get_html(url_gen))


def write_csv(data):
    with open('avito.csv', 'a') as f:
        writer = csv.writer(f)

        writer.writerow( (data['title'],
                          data['price'],
                          data['metro'],
                          data['url']) )

def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')

    ads = soup.find('div', class_ = 'index-root-2c0gs').find_all('div', class_ = 'item__line')

    for ad in ads:
        # class="description item_table-description"
        #title, price, metro, url
        name = ad.find('div', class_ = 'description item_table-description').find('span', class_ = "snippet-link-name").text.strip().lower()
        if 'macbook' in name:
            try:
                # title = str(ad.find('div', class_ = 'description item_table-description').find('span', class_ = "snippet-link-name").contents[0])
                title = ad.find('div', class_ = 'description item_table-description').find('span', class_ = "snippet-link-name").text.strip()
            except:
                title = ''

            try:
                url = 'https://www.avito.ru' + ad.find('div', class_ = 'description item_table-description').find('h3').find('a').get('href')
            except:
                url = ''

            try:
                price = ad.find('div', class_ = "snippet-price-row").find('meta', itemprop = "price").get('content')
            except:
                price = ''

            try:
                metro = ad.find('div', class_ = "item-address-georeferences").find('span', class_ = "item-address-georeferences-item__content").text.strip()
            except:
                metro = ''

            data = {'title': title,
                    'price': price,
                    'metro': metro,
                    'url': url}

            write_csv(data)
        else:
            continue



if __name__ == '__main__':
    main()


