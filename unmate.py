from bs4 import BeautifulSoup
import re 
from urllib.parse import urlparse
import requests
from operations import Operations

KEY_WORDS = dict()
KEY_WORDS['box'] = 'product-single--un'
KEY_WORDS['name'] = "product-single--un-product"
KEY_WORDS['price'] = 'product-single--un-price-actual'
KEY_WORDS['category'] = 'product-single--un-category'
KEY_WORDS['pagination'] = 'pagination--un__item uk-margin-remove'



def unmate(websites):
    final = list()
    operation = Operations()

    for url, _, user_name in websites:
        result = operation.get_response(url, user_name)
        if result is None:
            return []

        soup = BeautifulSoup(result, 'html.parser')
        count = operation.get_count(soup, 1, KEY_WORDS['pagination'])
        
        for i in range(1, count):
            local_url = url + '&page=' + str(i)

            result = requests.get(local_url).content
            soup = BeautifulSoup(result, 'html.parser')
            items = soup.find_all('article', class_ = KEY_WORDS['box'])

            final += operation.find(items, user_name, ['a', 'span'], KEY_WORDS) 
    return final
