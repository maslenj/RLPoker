import numpy as np

import torch
import rlcard

from games.holdem.translate_state import state_to_DQN
from games.holdem.holdem_game import HoldemPoker


class HoldemDQNAgent:

    def __init__(self, filepath):
        self.dqn = torch.load('../agents/holdem/plain_dqn_logs/model.pth')
        self.dqn = torch.load(filepath)

    def get_DQN_values(self, state):
        env = rlcard.make(
            'limit-holdem',
            config={
                'seed': 17,
            }
        )

        DQN_state = env._extract_state(state)
        return self.dqn.predict(DQN_state)

    def get_action(self, state: HoldemPoker):
        possible_actions = state.get_legal_actions()
        q_values = self.get_DQN_values(state_to_DQN(state.get_state()))
        action_map = {0: 'call', 1: 'raise', 2: 'fold', 3: 'call'}
        selected_action = action_map[np.argmax(q_values)]
        return selected_action if selected_action in possible_actions else None
