from bs4 import BeautifulSoup
import re 

KEY_WORDS = dict()
KEY_WORDS['name'] = 'shop-item'
KEY_WORDS['price'] = 'price'

def dobreziele(websites):
    final = []
    for result, weight, user_name in websites:
        soup = BeautifulSoup(result, 'html.parser')
        items = soup.find_all("div", class_ = KEY_WORDS['name'])
        for item in items:
            name = item.find('a', href = True).get('title')
            price = item.find("span", class_ = KEY_WORDS['price'])
            try:
                regex = re.findall(r"[0-9]+ ?[x]? ?[0-9]*", name)
                if regex[0].find('x') != -1:
                    index = regex[0].find('x')
                    local_weight = int(regex[0][:index-1]) * int(regex[0][index + 2:])
                else:
                    local_weight = int(regex[0])
                if local_weight < 10:
                    local_weight *= 1000
                local_name = name.lower()
                indexes = re.search(r"\d", local_name)
                local_name = local_name[:indexes.start()].split()

                local_price = float(re.sub("[,]", '.', re.sub("[^0-9,]", "", price.text)))
                matching = len(list(set(local_name).intersection(user_name)))
                if  matching >= len(user_name):
                    final.append([local_name, local_weight, local_price])
            except:
                pass
    return final
