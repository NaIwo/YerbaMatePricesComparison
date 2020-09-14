from urllib.parse import urlparse
import requests

class Shops():
    def __init__(self, url, name, products, func, ban, postfix = ''):
        self.url = url
        self.func = func
        self.name = name
        self.products = products
        self.banned_words = ban
        self.results = None
        self.price = None
        self.percent = 0.0
        self.postfix = postfix

    def print_information(self):
        big_string = ''
        big_string += '-' * 20  + '\nTotal price: {}'.format(self.price) + '\nPercent of found: {0:.{1}f}%'.format(self.percent, 1) + '\nFound products: \n'
        for result in self.results:
            big_string += '\t-{}\n'.format(result)

        print('-' * 20)
        print(self.name + ': ')
        print('Total price: {}'.format(self.price))
        print('Percent of found: {0:.{1}f}%'.format(self.percent, 1))
        print('Found products: ')
        for result in self.results:
            print('\t-' + result)
        return big_string

    def get_expenses(self):

        requests_tab = list()
        
        for name, weight in self.products:
            local_url = self.url +  '+'.join(name) + self.postfix
            try:
                request = requests.get(local_url).content
                requests_tab.append((request, weight, name))
            except:
                parsed_uri = urlparse(self.url)
                shop = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
                print('Something went wrong with \'{}\' product on \'{}\' :('.format(' '.join(name), shop[8:-1]))

        if requests_tab is not None:
            results = self.func(requests_tab)
            if results is not None:
                results = self.remove_banned_words(results)
                results, price, items_find = self.get_min_prices(results)
                
                self.percent = items_find / len(self.products) * 100
                self.results, self.price = results, price
                
    def get_min_prices(self, inputs):
        price = 0.0
        results = list()
        items_find = 0
        
        for product in self.products:
            max_el = None
            length = 100
            maxMatch = 0
            for inp in inputs:
                matching = len(list(set(inp[0]).intersection(product[0])))
                if matching != 0:
                    if matching > maxMatch and int(product[1]) % int(inp[1]) == 0:
                        maxMatch = matching
                        max_el = inp
                        length = len(inp[0])
                    elif matching == maxMatch and int(product[1]) % int(inp[1]) == 0:
                        if len(inp[0]) < length:
                            maxMatch = matching
                            max_el = inp
                            length = len(inp[0])
                        elif (int(product[1]) / int(inp[1])) * float(inp[2]) < (int(product[1]) / int(max_el[1])) * float(max_el[2]):
                            maxMatch = matching
                            max_el = inp
                            length = len(inp[0])
            
            if max_el is not None:
                items_find += 1
                times = int(int(product[1]) / int(max_el[1]))
                price += times * float(max_el[2])
                result = '{} : {}g * {} - {} pln.'.format(' '.join(max_el[0]), int(max_el[1]), times, round(times * max_el[2], 2))
                results.append(result)        
            
        return results, round(price, 2), items_find



    def remove_banned_words(self, results):
        ban = self.read_ban_words()
        final = list()
        for result in results:
            matching = len(list(set(ban).intersection(result[0])))
            if matching == 0:
                final.append(result)
        return final


    def read_ban_words(self):
        ban = list()
        try:
            with open(self.banned_words) as file:
                ban = [line.lower().strip().rstrip('\n') for line in file]
        except:
            pass
        return ban