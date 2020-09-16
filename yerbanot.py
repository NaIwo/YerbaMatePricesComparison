from bs4 import BeautifulSoup
import re 
from operations import Operations

KEY_WORDS = dict()
KEY_WORDS['name'] = "product-title"
KEY_WORDS['price'] = 'price'
KEY_WORDS['pagination'] = 'page-numbers'
KEY_WORDS['box'] = re.compile('product-grid-item.*')
#KEY_WORDS['box2'] = re.compile('single-product-page.*')
KEY_WORDS['box2'] = 'container-none'


def yerbanot(websites):
    final = list()
    operation = Operations()

    for url, user_name in websites:
        result = operation.get_response(url, user_name)
        if result is None:
            return []
        soup = BeautifulSoup(result, 'html.parser')
        count = operation.get_count(soup, 1, KEY_WORDS['pagination'], tag = 'a', num = -2)

        for i in range(1, count):
            index = re.search(r'\/\?', url).start()
            local_url = url[:index] + '/page/' + str(i) + url[index:]
            result = operation.get_response(local_url, user_name)
            soup = BeautifulSoup(result, 'html.parser')
            items = soup.find_all('div', {'class' : KEY_WORDS['box']}) 
            if len(items) == 0:
                items = soup.find_all('div', {'class' : KEY_WORDS['box2']}) 
            final += operation.find(items, user_name, ['h3', 'span'], KEY_WORDS) 

    return final
