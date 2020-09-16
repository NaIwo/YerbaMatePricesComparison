from bs4 import BeautifulSoup
import re 
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
    
    for url, user_name in websites:
        result = operation.get_response(url, user_name)
        if result is None:
            continue

        soup = BeautifulSoup(result, 'html.parser')
        count = operation.get_count(soup, 1, KEY_WORDS['pagination'])
        
        for i in range(1, count):
            local_url = url + '&page=' + str(i)

            result = operation.get_response(local_url, user_name)
            soup = BeautifulSoup(result, 'html.parser')
            items = soup.find_all('article', class_ = KEY_WORDS['box'])

            final += operation.find(items, user_name, ['a', 'span'], KEY_WORDS) 
    return final
