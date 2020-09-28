from bs4 import BeautifulSoup
import re
from operations import Operations

KEY_WORDS = dict()
KEY_WORDS['name'] = 'shop-item'
KEY_WORDS['price'] = 'price'


def dobreziele(websites):
    final = list()
    operation = Operations()
    for url, user_name in websites:

        result = operation.get_response(url, user_name)
        if result is None:
            return []

        soup = BeautifulSoup(result, 'html.parser')
        items = soup.find_all("div", class_=KEY_WORDS['name'])

        for item in items:
            name = item.find('a', href=True).get('title')
            price = item.find("span", class_=KEY_WORDS['price'])

            local_weight = operation.get_weight(name.lower(), with_regex = True)
            local_name = operation.get_name(name.lower())

            for child in price.find_all("span"):
                child.decompose()
            local_price = operation.get_price(price.get_text())

            matching = len(list(set(local_name).intersection(user_name)))
            if matching >= len(user_name):
                final.append([local_name, local_weight, local_price])

    return final
