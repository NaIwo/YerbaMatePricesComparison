import numpy as np
import sys

def Levenshtein_distance(first, second):
    first = ' ' + ' '.join(sorted(first.lower().split()))
    second = ' ' + ' '.join(sorted(second.lower().split()))
    first_len = len(first)
    second_len = len(second)

    matrix = np.array([[-1] * first_len] * second_len)
    matrix[0] = [i for i in range(first_len)]
    matrix[:, 0] = [i for i in range(second_len)]

    for i in range(1, second_len):
        for j in range(1, first_len):
            matrix[i, j] = min(matrix[i-1, j-1] + (0 if second[i]==first[j] else 1),
                                matrix[i-1, j] + 1, matrix[i, j-1] + 1)
    return matrix[-1,-1]
            

def main():
    distance = Levenshtein_distance(sys.argv[1], sys.argv[2])
    print(distance)

if __name__ == "__main__":
    main()