import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def build_raise_dictionary():
    df = pd.read_csv("../dataset_generation/hand_modeling_data.csv")
    raise_dict = {}
    for row in df.values:
        num_raises = row[0]
        hand_strength = row[1]
        if num_raises not in raise_dict:
            raise_dict[num_raises] = []
        raise_dict[num_raises].append(hand_strength)
    return raise_dict


def main():
    raise_dict = build_raise_dictionary()
    raises = 1
    plt.hist(raise_dict[raises], bins=10)
    plt.show()

    print("mean:", np.mean(raise_dict[raises]))
    print("sd:", np.std(raise_dict[raises]))

    # for i in range(6):
    #     plt.hist()
    #     print(i, np.average(raise_dict[i]))


if __name__ == '__main__':
    main()