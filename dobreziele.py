from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse
import requests
from operations import Operations

KEY_WORDS = dict()
KEY_WORDS['name'] = 'shop-item'
KEY_WORDS['price'] = 'price'



def get_weight(name):
    regex = re.findall(r"[0-9]+ ?[x]? ?[0-9]*", name)
    try:
        if regex[0].find('x') != -1:
            index = regex[0].find('x')
            local_weight = float(regex[0][:index-1]) * int(regex[0][index + 2:])
        else:
            local_weight = float(regex[0])

        if re.search(r"\d+ *kg", name.lower()) is not None:
            local_weight = local_weight * 1000
        return local_weight
    except IndexError:
        return 0.0


def dobreziele(websites):
    final = list()
    operation = Operations()
    for url, _, user_name in websites:

        result = operation.get_response(url, user_name)
        if result is None:
            return []

        soup = BeautifulSoup(result, 'html.parser')
        items = soup.find_all("div", class_=KEY_WORDS['name'])

        for item in items:
            name = item.find('a', href=True).get('title')
            price = item.find("span", class_=KEY_WORDS['price'])

            local_weight = get_weight(name)
            local_name = operation.get_name(name.lower())
            local_price = float(re.sub("[,]", '.', re.sub("[^0-9,]", "", price.text)))

            matching = len(list(set(local_name).intersection(user_name)))
            if matching >= len(user_name):
                final.append([local_name, local_weight, local_price])

    return final
