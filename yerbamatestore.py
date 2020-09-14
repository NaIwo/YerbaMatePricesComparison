from bs4 import BeautifulSoup
import re 


def yerbamatestore(websites):
    final = []

    for result, weight, user_name in websites:
        names = []
        prices = []
        soup = BeautifulSoup(result, 'html.parser')
        try:
            script = soup.find("script", text=re.compile("var\s+dataLayerProducts")).string.split('\n')
        except:
            continue
        for i in range(len(script) - 1):
            if  script[i].strip()[:6] == '\'name\'' and script[i+1].strip()[:7] == '\'price\'':
                names.append(re.sub('\'', '', re.sub(' +', ' ', re.sub(':', '', script[i].strip())))[5:-1])
                prices.append(re.sub('\'', '', re.sub(' +', ' ', re.sub(':', '', script[i+1].strip())))[6:-1])
        assert len(names) == len(prices)
        for name, price in zip(names, prices):      
            try:
                local_weight = int(re.sub('[^0-9]', '', name))
                if re.search(r"\d+ *kg", name.lower()) is not None:
                    local_weight = local_weight * 1000
                
                local_name = name.lower()
                indexes = re.search(r"\d", local_name)
                local_name = local_name[:indexes.start()].split()

                local_price = float(price)
                
                matching = len(list(set(local_name).intersection(user_name)))
                if  matching >= len(user_name):
                    final.append([local_name, local_weight, local_price])
            except:
                pass
    return final
