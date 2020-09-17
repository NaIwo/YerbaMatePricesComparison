import re
from shops import Shops
import threading
import sys
import os
from unmate import *
from ymt24 import *
from matemundo import *
from dobreziele import *
from poyerbani import *
from herbatkowo import *
from yerbamarket import *
from yerbanot import *
from yerbamatestore import *
import pandas as pd
from Levenshtein import Levenshtein_distance
from operations import Operations
from addToCsv import add_to_csv

ORDER = 'order.txt'
BANNED_WORDS = 'ban_words.txt'
RESULTS = 'results.txt'
DATASET_CSV = 'YerbaMataDataset.csv'

def read_dataset(wd):
    return pd.read_csv(os.path.join(wd, DATASET_CSV)).iloc[1:,1]

def ask_user(name, user_name):
    answer = input('Do you had mind \'{}\' instead of \'{}\'? (y/n):  '.format(name, user_name))
    if answer == 'y':
        return True
    else:
        answer = input('Do you want to add to database \'{}\'? (y/n):  '.format(user_name))
        if answer == 'y':
            add_to_csv(user_name)
        return False

def check_correctness(name, dataset):
    minimum = float('inf')
    name = ' '.join(name)
    final_name = name
    border = 8
    for data in dataset:
        temp = Levenshtein_distance(name, data)
        if temp < minimum and temp < border:
            if len(name.split()) >= len(data.split()):
                minimum = temp
                final_name = data
    if len(list(set(name.split()).intersection(final_name.split()))) == len(name.split()):
        return name.split()

    if ask_user(final_name, name):
        return final_name.split()
    else:
        return name.split()


def read_product():
    products = list()
    dataset = read_dataset(os.getcwd())
    operation = Operations()
    with open(ORDER) as file:
        temp = [line.lower().strip().rstrip('\n') for line in file]
    for product in temp:
        name = operation.get_name(product)
        name = check_correctness(name, dataset)

        weight = operation.get_weight(product)
        products.append((name, weight))
    return products

def run_threads(threads):
    print('Searching in progress...')
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    

def main():
    try:
        drop_file = sys.argv[1]
        if drop_file is not None:
            ORDER = drop_file
    except:
        pass
    products = read_product()
    threads = list()
    shops_list = list()

    shops_list.append(Shops('https://un-mate.pl/szukaj?criteria%5Bsearch%5D%5Bvalue%5D=', name = 'unmate', products=products, func = unmate, ban = BANNED_WORDS))
    shops_list.append(Shops('https://ymt24.pl/pl/searchquery/', name = 'ymt24', products=products, func = ymt24, ban = BANNED_WORDS))
    shops_list.append(Shops('https://www.matemundo.pl/search.php?text=', name = 'matemundo', products=products, func = matemundo, ban = BANNED_WORDS))
    shops_list.append(Shops('https://dobreziele.pl/szukaj?k=', name = 'dobreziele', products=products, func = dobreziele, ban = BANNED_WORDS))
    shops_list.append(Shops('https://www.poyerbani.pl/search.php?text=', name = 'poyerbani', products=products, func = poyerbani, ban = BANNED_WORDS))
    shops_list.append(Shops('https://www.herbatkowo.com.pl/search.php?text=', name = 'herbatkowo', products=products, func = herbatkowo, ban = BANNED_WORDS))
    shops_list.append(Shops('https://www.yerbamarket.com/search.php?text=', name = 'yerbamarket', products=products, func = yerbamarket, ban = BANNED_WORDS))
    shops_list.append(Shops('https://yerbanot.com/?s=', name = 'yerbanot', products=products, func = yerbanot, ban = BANNED_WORDS, postfix = '&post_type=product'))
    shops_list.append(Shops('https://www.yerbamatestore.pl/s?q=', name = 'yerbamatestore', products=products, func = yerbamatestore, ban = BANNED_WORDS))

    for shop in shops_list:
        threads.append(threading.Thread(target=shop.get_expenses))

    run_threads(threads)

    shops_list = sorted(shops_list, key = lambda shops : shops.price)
    shops_list = sorted(shops_list, key = lambda shops : shops.percent, reverse=True)

    with open(RESULTS, 'w') as file:
        for shop in shops_list:
            file.write(shop.print_information())
        

if __name__ == "__main__":
    main()
    input("\n\nPress any button to continue...") 