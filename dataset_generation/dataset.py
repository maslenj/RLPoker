import json
import numpy as np

import torch
from torch.utils.data import Dataset
import rlcard
from games.holdem.translate_state import *


# state = {'agent_hand': self.players[self.current_player]['hand'],
#                  'community_cards': self.community_cards,
#                  'pot': self.pot,
#                  'legal_actions': self.get_legal_actions(),
#                  'calling_amount': self.calling_amount,
#                  'round_raises': self.round_raises,
#                  }

def one_hot_action_encoding(action):
    if action == 'call':
        return np.array([1, 0, 0, 0])
    if action == 'raise':
        return np.array([0, 1, 0, 0])
    if action == 'fold':
        return np.array([0, 0, 1, 0])
    if action == 'check':
        return np.array([0, 0, 0, 1])


class PokerHandDataset(Dataset):
    def __init__(self, path):

        self.path = path
        self.x = []
        self.y = []

        self.env = rlcard.make(
            'limit-holdem',
            config={
                'seed': 17,
            }
        )
        with open(self.path, 'r') as f:
            line = f.readline()
            while line:
                example = json.loads(line)
                # Assuming it's stored as a dictionary of state and action
                state, action = example['state'], example['action']
                DQN_state = state_to_DQN(state)
                input_feature = self.env._extract_state(DQN_state)['obs']
                input_feature = np.expand_dims(input_feature, axis=0)
                self.x.append(input_feature)
                self.y.append(one_hot_action_encoding(action))
                line = f.readline()

    def __len__(self):
        return len(self.x)

    def __getitem__(self, idx):
        return torch.from_numpy(self.x[idx]).float(), torch.from_numpy(self.y[idx]).float()
