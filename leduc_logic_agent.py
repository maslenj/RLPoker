import numpy as np


class LogicAgent(object):
    def __init__(self):
        self.num_actions = 4
        self.use_raw = False

    # testing policy
    @staticmethod
    def step(state):
        print(state)
        return np.random.choice(list(state['legal_actions'].keys()))

    # training policy
    def eval_step(self, state):
        return self.step(state), {}
