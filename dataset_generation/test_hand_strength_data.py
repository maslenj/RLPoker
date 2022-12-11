import numpy as np
import pandas as pd


def main():
    df = pd.read_csv("hand_modeling_data.csv")
    raise_dict = {}
    for row in df.values:
        num_raises = row[0]
        hand_strength = row[1]
        if num_raises not in raise_dict:
            raise_dict[num_raises] = []
        raise_dict[num_raises].append(hand_strength)
    for i in range(6):
        print(i, np.average(raise_dict[i]))


if __name__ == '__main__':
    main()