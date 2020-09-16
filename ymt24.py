from bs4 import BeautifulSoup
import re 
from operations import Operations

KEY_WORDS = dict()
KEY_WORDS['name'] = "productname"
KEY_WORDS['price'] = 'price f-row'
KEY_WORDS['box'] = 'product-inner-wrap'
KEY_WORDS['pagination'] = 'paginator'

def get_count(soup, counter):
    try:
        ul = soup.find('ul', class_= KEY_WORDS['pagination']).find_all('li')[-2]
        return int(ul.text) + counter
    except:
        return counter + 1

def find(items, user_name, operation):
        out = list()
        for item in items:
            name = item.find('span', class_ = KEY_WORDS['name'])
            price = item.find('div', class_ = KEY_WORDS['price'])

            local_weight = operation.get_weight(name.text.lower()) 
            local_name = operation.get_name(name.text.lower())
            local_price = operation.get_price(price.find('em').text.lower())
            

            matching = len(list(set(local_name).intersection(user_name)))
            if  matching >= len(user_name):
                out.append([local_name, local_weight, local_price])
        return out

def ymt24(websites):
    final = list()
    operation = Operations()

    for url, user_name in websites:
        result = operation.get_response(url, user_name)
        if result is None:
            return []

        soup = BeautifulSoup(result, 'html.parser')
        count = get_count(soup, 1)

        for i in range(1, count):
            local_url = url + '/' + str(i)

            result = operation.get_response(local_url, user_name)
            soup = BeautifulSoup(result, 'html.parser')
            items = soup.find_all('div', class_ = KEY_WORDS['box'])

            final += find(items, user_name, operation)

    return final
