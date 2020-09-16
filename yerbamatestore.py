from bs4 import BeautifulSoup
import re 
from operations import Operations


def yerbamatestore(websites):
    final = list()

    for url, user_name in websites:
        names = list()
        prices = list()
        operation = Operations()

        result = operation.get_response(url, user_name)
        if result is None:
            return []

        soup = BeautifulSoup(result, 'html.parser')
        try:
            script = soup.find("script", text=re.compile("var\s+dataLayerProducts")).string.split('\n')
        except:
            continue

        for i in range(len(script) - 1):
            if  script[i].strip()[:6] == '\'name\'' and script[i+1].strip()[:7] == '\'price\'':
                names.append(re.sub('\'', '', re.sub(' +', ' ', re.sub(':', '', script[i].strip())))[5:-1])
                prices.append(re.sub('\'', '', re.sub(' +', ' ', re.sub(':', '', script[i+1].strip())))[6:-1])
        try:
            assert len(names) == len(prices)
        except AssertionError:
            continue
            
        for name, price in zip(names, prices):      
            local_weight = operation.get_weight(name.lower())
            local_name = operation.get_name(name.lower())
            local_price = float(price)
                
            matching = len(list(set(local_name).intersection(user_name)))
            if  matching >= len(user_name):
                final.append([local_name, local_weight, local_price])

    return final
