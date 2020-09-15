from bs4 import BeautifulSoup
import re 
from urllib.parse import urlparse
import requests
from operations import Operations

KEY_WORDS = dict()
KEY_WORDS['name'] = "product__name"
KEY_WORDS['price'] = 'price'
KEY_WORDS['box'] = 'product col-6 col-sm-4 pt-3 pb-md-3'
KEY_WORDS['pagination'] = 'pagination__element --item'



def herbatkowo(websites):
    final = list()
    operation = Operations()

    for url, _, user_name in websites:
        result = operation.get_response(url, user_name)
        if result is None:
            return []
        soup = BeautifulSoup(result, 'html.parser')
        count = operation.get_count(soup, 0, KEY_WORDS['pagination'])

        for i in range(0, count):
            local_url = url + '?counter=' + str(i)
            result = requests.get(local_url).content
            soup = BeautifulSoup(result, 'html.parser')
            items = soup.find_all('div', class_ = KEY_WORDS['box'])

            final += operation.find(items, user_name, ['a', 'strong'], KEY_WORDS) 

        
    return final
