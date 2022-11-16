import numpy as np


class HoldemPoker:
    DECK_CARDS = ['As', 'Ah', 'Ac', 'Ad']

    def __init(self, bankrolls=(100, 100)):
        self.num_players = 2
        self.community_cards = []
        self.round_number = 0
        self.round_history = ('r', 'r')
        self.pot = 0
        self.calling_amount = 0
        self.players = [
            {
                'hand': [],
                'bankroll': bankrolls[i]
            } for i in range(self.num_players)
        ]

    # todo:
    def is_game_over(self):
        pass

    # todo: Jimmy
    def decide_winner(self):
        pass

    # todo:
    def deal_card(self):
        pass

    # todo:
    def input_state(self, state):
        pass

    # todo:
    def print_state(self):
        pass
