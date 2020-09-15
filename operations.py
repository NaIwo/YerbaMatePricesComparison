from bs4 import BeautifulSoup
import re 
from urllib.parse import urlparse
import requests

class Operations():
    def get_response(self, url, name):
        try:
            return requests.get(url).content
        except:
            parsed_uri = urlparse(url)
            shop = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
            print('Something went wrong with \'{}\' product on \'{}\' :('.format(
                ' '.join(name), shop[8:-1]))
            return None

    def get_count(self, soup, counter, pagination):
        try:
            return int(soup.find_all('li', class_= pagination)[-1].text) + counter
        except:
            return counter + 1

    def get_weight(self, name):
        try:
            local_weight = float(re.sub("[,]", '.', re.sub("[^0-9,]", "", name)))
            if re.search(r"\d+ *kg", name) is not None:
                local_weight = local_weight * 1000
            return local_weight
        except IndexError:
            return 0.0
        except:
            print(re.sub("[,]", '.', re.sub("[^0-9,]", "", name)))

    def get_name(self, local_name):
        try:
            indexes = re.search(r"\d", local_name)
            local_name = local_name[:indexes.start()].split()
            return local_name
        except AttributeError:
            return local_name

    def get_price(self, price):
        try:
            local_price = float(re.sub("[,]", '.', re.sub("[^0-9,]", "", price)))
            return local_price
        except ValueError:
            return 0.0
    

    def find(self, items, user_name, tags, KEY_WORDS, title = False):
        out = list()
        for item in items:

            if 'category' in KEY_WORDS:
                if item.find('a', class_ = KEY_WORDS['category']).text.strip() != 'Yerba Mate':
                    continue

            name = item.find(tags[0], class_ = KEY_WORDS['name'])
            price = item.find(tags[1], class_ = KEY_WORDS['price'])

            if title:
                local_weight = self.get_weight(name.get('title').lower())
                        
                local_name = self.get_name(name.get('title').lower())

            else:
                local_weight = self.get_weight(name.text.lower())
                        
                local_name = self.get_name(name.text.lower())

            local_price = self.get_price(price.text)
            

            matching = len(list(set(local_name).intersection(user_name)))
            if  matching >= len(user_name):
                out.append([local_name, local_weight, local_price])
        return out