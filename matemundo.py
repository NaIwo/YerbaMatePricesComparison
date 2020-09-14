from bs4 import BeautifulSoup
import re 

KEY_WORDS = dict()
KEY_WORDS['name'] = "product__name"
KEY_WORDS['price'] = 'product__prices'

def matemundo(websites):
    final = []
    for result, weight, user_name in websites:
        soup = BeautifulSoup(result, 'html.parser')
        names = soup.find_all("a", class_ = KEY_WORDS['name'])
        prices = soup.find_all("div", class_ = KEY_WORDS['price'])
        for name, price in zip(names, prices):
            try:
                local_weight = str(re.sub('[^0-9]', '', name.text))
                if local_weight[0] == '0':
                    local_weight = local_weight[0] + '.' + local_weight[1:]
                local_weight = float(local_weight)
                if re.search(r"\d+ *kg", name.text.lower()) is not None:
                    local_weight = local_weight * 1000
                
                local_name = name.text.lower()
                indexes = re.search(r"\d", local_name)
                local_name = local_name[:indexes.start()].split()

                local_price = float(re.sub("[,]", '.', re.sub("[^0-9,]", "", price.findChildren()[0].text)))
        
                matching = len(list(set(local_name).intersection(user_name)))
                if  matching >= len(user_name):
                    final.append([local_name, local_weight, local_price])
            except:
                pass
    return final
