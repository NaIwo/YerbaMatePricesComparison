from bs4 import BeautifulSoup
import re 
from operations import Operations

KEY_WORDS = dict()
KEY_WORDS['box'] = re.compile(r'product_wrapper.*')
KEY_WORDS['price'] = 'price'
KEY_WORDS['name'] = 'product-name'
KEY_WORDS['size'] = 'sizes'
KEY_WORDS['selection'] = 'select_button'
KEY_WORDS['pagination'] = 'pagination pull-right'

def get_count(soup, counter):
    try:
        return int(soup.find_all('ul', class_= KEY_WORDS['pagination']).findChildren()[-2].text) + counter
    except:
        return counter + 1

def get_weight(name):
    try:
        regex = re.findall(r"[0-9]+,?[0-9]* ?[x]? ?[0-9]*", name)
        if regex[0].find('x') != -1:
            index = regex[0].find('x')
            local_weight = float(regex[0][:index-1]) * float(regex[0][index + 2:])
        else:
            local_weight = float(regex[0])

        if re.search(r"\d+ *kg", name) is not None:
            local_weight = local_weight * 1000.0
        return local_weight

    except IndexError:
        return 0.0
    except ValueError:
        return 0.0

def find(items, operation, user_name):
    out = list()
    for item in items:
        name = item.find('a', class_ = KEY_WORDS['name'])
        price = item.find("span", class_ = KEY_WORDS['price'])

        size = item.find('div', class_ = KEY_WORDS['size'])
            
        #check if product contain size to chose
        if size is not None:

            selectons = size.find_all('span', class_ = KEY_WORDS['selection'])
            for selected in selectons:
                local_price = operation.get_price(selected.get('data-price'))
                local_weight = operation.get_weight(selected.text.lower())
                local_name = operation.get_name(name.text.lower())
                        
                matching = len(list(set(local_name).intersection(user_name)))
                if  matching >= len(user_name):
                    out.append([local_name, local_weight, local_price])
                            
        #if size appear only in product name
        else:
            local_weight = get_weight(name.text.lower())
            local_name = operation.get_name(name.text.lower())
            local_price = operation.get_price(price.text)

            matching = len(list(set(local_name).intersection(user_name)))
            if  matching >= len(user_name):
                out.append([local_name, local_weight, local_price])
    return out

def yerbamarket(websites):  
    final = list()
    operation = Operations()

    for url, user_name in websites:
        result = operation.get_response(url, user_name)
        if result is None:
            return []

        soup = BeautifulSoup(result, 'html.parser')
        count = get_count(soup, 0)
        if count == 1:
            items = soup.find_all("div", class_ = KEY_WORDS['box'])
            final += find(items, operation, user_name)
        else:
            for i in range(0, count):
                local_url = url + '?counter=' + str(i)
                result = operation.get_response(local_url, user_name)
                soup = BeautifulSoup(result, 'html.parser')
                items = soup.find_all("div", class_ = KEY_WORDS['box'])
                final += find(items, operation, user_name)
    return final
