from bs4 import BeautifulSoup
import re 
from operations import Operations

KEY_WORDS = dict()
KEY_WORDS['name'] = "product__name"
KEY_WORDS['price'] = 'price'
KEY_WORDS['pagination'] = 'pagination__element --item'
KEY_WORDS['box'] = 'product col-12 col-sm-4 col-md-3 pt-3 pb-md-3 mb-3 mb-sm-0'


def poyerbani(websites):
    final = list()
    operation = Operations()
    for url, user_name in websites:
        result = operation.get_response(url, user_name)
        if result is None:
            return []

        soup = BeautifulSoup(result, 'html.parser')
        count = operation.get_count(soup, 0, KEY_WORDS['pagination'])
        if count == 1:
            items = soup.find_all('div', class_ = KEY_WORDS['box'])

            final += operation.find(items, user_name, ['a', 'strong'], KEY_WORDS)
        else:
            for i in range(0, count):
                local_url = url + '&counter=' + str(i)
                result = operation.get_response(local_url, user_name)
                soup = BeautifulSoup(result, 'html.parser')
                items = soup.find_all('div', class_ = KEY_WORDS['box'])

                final += operation.find(items, user_name, ['a', 'strong'], KEY_WORDS)
    return final
