from bs4 import BeautifulSoup
import re 

KEY_WORDS = dict()
KEY_WORDS['wrapper'] = 'product_wrapper'
KEY_WORDS['price'] = 'price'
KEY_WORDS['name'] = 'product-name'
KEY_WORDS['size'] = 'sizes'
KEY_WORDS['selection'] = 'select_button'

def yerbamarket(websites):  
    final = []
    for result, weight, user_name in websites:
        soup = BeautifulSoup(result, 'html.parser')
        items = soup.find_all("div", class_ = KEY_WORDS['wrapper'])
        
        for item in items:
            name = item.find('a', class_ = KEY_WORDS['name'])
            price = item.find("span", class_ = KEY_WORDS['price'])
            size = item.find('div', class_ = KEY_WORDS['size'])
            try:
                if size is not None:
                    selectons = size.find_all('span', class_ = KEY_WORDS['selection'])
                    for selected in selectons:
                        local_price = selected.get('data-price')
                        local_price = float(re.sub("[,]", '.', re.sub("[^0-9,]", "", local_price)))

                        local_weight = selected.text
                        local_weight = int(re.sub('[^0-9]', '', local_weight))
                        if re.search(r"\d+ *kg", selected.text.lower()) is not None:
                            local_weight = local_weight * 1000

                        local_name = name.text.lower()
                        
                        indexes = re.search(r"\d", local_name)
                        if indexes is not None:
                            local_name = local_name[:indexes.start()].split() 
                        else:
                            local_name = local_name.split() 
                        
                        matching = len(list(set(local_name).intersection(user_name)))
                        if  matching >= len(user_name):
                            final.append([local_name, local_weight, local_price])
                else:
                    local_name = name.text.lower()
                    regex = re.findall(r"[0-9]+,?[0-9]* ?[x]? ?[0-9]*", local_name)

                    if regex[0].find('x') != -1:
                        index = regex[0].find('x')
                        local_weight = int(regex[0][:index-1]) * int(regex[0][index + 2:])
                    else:
                        local_weight = int(regex[0])
                    if re.search(r"\d+ *kg", name.text.lower()) is not None:
                        local_weight = local_weight * 1000

                    indexes = re.search(r"\d", local_name)
                    if indexes is not None:
                        local_name = local_name[:indexes.start()].split() 
                    else:
                        local_name = local_name.split()

                    local_price = float(re.sub("[,]", '.', re.sub("[^0-9,]", "", price.text)))

                    matching = len(list(set(local_name).intersection(user_name)))
                    if  matching >= len(user_name):
                        final.append([local_name, local_weight, local_price])
            except:
                pass
    return final
