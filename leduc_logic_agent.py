import numpy as np


class LogicAgent(object):
    def __init__(self):
        self.num_actions = 4
        self.use_raw = False

    # testing policy
    @staticmethod
    def step(state):
        # raise if we have a kind and fold otherwise
        if state['raw_obs']['hand'] == 'HK' or state['raw_obs']['hand'] == 'SK':
            if 'raise' in state['raw_obs']['legal_actions']:
                return state['raw_obs']['legal_actions'].index('raise')
            else:
                return state['raw_obs']['legal_actions'].index('call')
        else:
            return np.random.choice(list(state['legal_actions'].keys()))

    # training policy
    def eval_step(self, state):
        # this agent does not do any learning
        return self.step(state), {}
