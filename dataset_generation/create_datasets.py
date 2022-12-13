import random


def create_datasets(filepath):

    with open(filepath, 'r') as f:
        line = f.readline()
        data = []
        while line:
            data.append(line)
            line = f.readline()

    # We will use 70% train, 20% validation, 10% test
    split = 0.7
    val_split = 0.9

    random.shuffle(data)
    print(len(data))

    train_data = data[:int(split*len(data))]
    val_data = data[int(split*len(data)):int(val_split*len(data))]
    test_data = data[int(val_split)*len(data):]

    with open('../dataset/train.json', 'w') as f:
        f.writelines(train_data)
        f.close()

    with open('../dataset/val.json', 'w') as f:
        f.writelines(val_data)
        f.close()

    with open('../dataset/test.json', 'w') as f:
        f.writelines(test_data)
        f.close()


def main():
    create_datasets('../dataset/data.json')


if __name__ == '__main__':
    main()
