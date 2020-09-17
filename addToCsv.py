import pandas as pd
import sys 
import os

DATASET_CSV = 'YerbaMataDataset.csv'


def remove_banned_words(results):
    ban = read_ban_words()
    final = list()
    for result in results:
        matching = len(list(set(ban).intersection(result.split())))
        if matching == 0:
            final.append(result)
    return final

def read_ban_words():
    ban = list()
    try:
        with open('ban_words.txt') as file:
            ban = [line.lower().strip().rstrip('\n') for line in file]
    except:
        pass
    return ban

def add_to_csv(name):
    directory = os.path.join(os.getcwd(), DATASET_CSV)
    dataset = pd.read_csv(directory).values[:,1].tolist()
    dataset = remove_banned_words(dataset)
    dataset.append(name)
    dataset = pd.DataFrame(sorted(list(set(dataset))))
    dataset.to_csv(directory)

def main():
    name = sys.argv[1]
    add_to_csv(name)

if __name__ == "__main__":
    main()