import numpy as np
import random


class HoldemPoker:
    SUITS = ['s', 'h', 'c', 'd']
    RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    DECK_CARDS = [x + y for x in RANKS for y in SUITS]

    def __init__(self, bankrolls=(100, 100)):
        self.num_players = 2
        self.deck = self.DECK_CARDS.copy()
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

    # todo: Rob
    def is_game_over(self):
        return self.round_number == 4

    # todo: Jimmy
    def decide_winner(self):
        pass

    # todo: Rob
    def deal_card(self):
        card = random.choice(self.deck)
        self.deck.remove(card)
        return card

    # todo: Rob
    def input_state(self, state):
        self.community_cards, self.round_number, \
          self.round_history, self.pot, \
          self.calling_amount, self.players = state

    # todo: Rob
    def print_state(self):
        print("-----------------------------")
        print("Community cards:", self.community_cards)
        print("Round number:", self.round_number)
        print("Round history:", self.round_history)
        print("Pot:", self.pot)
        print("Calling amount:", self.calling_amount)
        for i, player in enumerate(self.players):
            print("-----------------------------")
            print(f"Curr Player: {i}")
            print("Hand:", player['hand'])
            print("Bankroll:", player['bankroll'])
        print("-----------------------------")
