from bs4 import BeautifulSoup
import re 

KEY_WORDS = dict()
KEY_WORDS['name'] = "productname"
KEY_WORDS['price'] = 'price f-row'

def ymt24(websites):
    final = []
    for result, weight, user_name in websites:
        soup = BeautifulSoup(result, 'html.parser')
        names = soup.find_all("span", class_ = KEY_WORDS['name'])
        prices = soup.find_all("div", class_ = KEY_WORDS['price'])
        for name, price in zip(names, prices):
            try:
                local_weight = int(re.sub('[^0-9]', '', name.text.lower()))
                if re.search(r"\d+ *kg", name.text.lower()) is not None:
                    local_weight = local_weight * 1000
                
                local_name = name.text.lower()
                indexes = re.search(r"\d", local_name)
                local_name = local_name[:indexes.start()].split()

                local_price = float(re.sub("[,]", '.', re.sub("[^0-9,]", "", price.findChildren()[1].text)))
                matching = len(list(set(local_name).intersection(user_name)))
                if  matching >= len(user_name):
                    final.append([local_name, local_weight, local_price])
            except:
                pass
    return final
