import numpy as np


class MCTSAgent(object):
    def __init__(self):
        self.num_actions = 4
        self.use_raw = False

    # testing policy
    @staticmethod
    def step(state):
        # create Q table
        Q = {}
        # create T table (number of times each state has been visited)
        T = {}
        # create N table (number of times each state-action pair
        # has been visited)
        N = {}

        return np.random.choice(list(state['legal_actions'].keys()))

    # training policy
    def eval_step(self, state):
        # this agent does not do any learning
        return self.step(state), {}



