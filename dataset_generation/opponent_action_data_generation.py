import json
import numpy as np
import pickle

from dataset import one_hot_action_encoding
from sklearn.linear_model import LogisticRegression


def main():
    input_features = []
    labels = []
    label_dict = {'call': [], 'raise': [], 'fold': []}
    action_map = {'call': 0, 'raise': 1, 'fold': 2}
    with open('../data.json', 'r') as f:
        line = f.readline()
        while line:
            example = json.loads(line)
            # Assuming it's stored as a dictionary of state and action
            state, action = example['state'], example['action']
            if action == 'check':
                action = 'call'
            # Input feature represented as (round_num, calling_amount, pot)
            # Label represented as binary encoding, either 0 or 1
            input_features.append([len(state['community_cards']), state['calling_amount'], state['pot']])
            labels.append(np.argmax(one_hot_action_encoding(action)[:-1]))
            # one_hot = one_hot_action_encoding(action)
            # for class_name in label_dict:
            #     encoding_index = action_map[class_name]
            #     label_dict[class_name].append(one_hot[encoding_index])
            line = f.readline()

    print(len(input_features))
    print(labels[:10])
    print(input_features[:10])

    model = LogisticRegression(random_state=13, multi_class='multinomial').fit(np.array(input_features), np.array(labels))
    filename = 'ActionModel.sav'
    pickle.dump(model, open(filename, 'wb'))


if __name__ == '__main__':
    main()
