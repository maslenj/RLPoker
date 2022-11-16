import numpy as np


class LeducPoker:
    DECK_CARDS = ['HK', 'SK', 'HQ', 'SQ', 'HJ', 'SJ']
    HAND_RANKS = {
        'KK': 0,
        'QQ': 1,
        'JJ': 2,
        'KQ': 3,
        'JK': 3,
        'JQ': 3
    }

    def __init__(self, state=None, player_0_bankroll=100, player_1_bankroll=100):
        self.deck = LeducPoker.DECK_CARDS.copy()
        np.random.shuffle(self.deck)

        if state:
            '''
            'raw_obs': 
            {
                'hand': 'SQ', 
                'public_card': 'HJ', 
                'all_chips': [2, 2], 
                'my_chips': 2, 
                'legal_actions': ['raise', 'fold', 'check'], 
                'current_player': 1}, 
                'raw_legal_actions': ['raise', 'fold', 'check'], 
                'action_record': [(1, 'call'), (0, 'check')]
            }
            '''
            self.players = [
                {
                    'hand': state['raw_obs']['hand'],
                    'bankroll': state['raw_obs']['my_chips']
                }
            ]
        self.players = [
            {
                'hand': self.deck.pop(),
                'bankroll': player_0_bankroll
            },
            {
                'hand': self.deck.pop(),
                'bankroll': player_1_bankroll
            }
        ]
        self.round = 0
        self.num_raises = 0
        self.pot = 0
        self.to_call = 0
        self.community_card = self.deck.pop()
        self.to_play = 0
        self.is_game_over = False

    def get_legal_actions(self):
        legal_actions = ['call', 'fold']
        if self.num_raises < 2:
            legal_actions.append('raise')
        return legal_actions

    def step(self, action):
        assert action in self.get_legal_actions()
        raise_amount = 2 if self.round == 0 else 4
        if action == 'raise':
            self.players[self.to_play]['bankroll'] -= raise_amount + self.to_call
            self.pot += raise_amount + self.to_call
            self.to_call = raise_amount
            self.num_raises += 1
        elif action == 'call':
            self.players[self.to_play]['bankroll'] -= self.to_call
            self.pot += self.to_call
            self.to_call = 0
            if self.to_play == 1 or self.num_raises > 0:
                self.round += 1
                self.num_raises = 0
        elif action == 'fold':
            self.players[(self.to_play + 1) % 2]['bankroll'] += self.pot
            self.is_game_over = True

        self.to_play = (self.to_play + 1) % 2
        if self.round == 2:
            # showdown
            self.is_game_over = True
            scores = [LeducPoker.HAND_RANKS[LeducPoker._create_hand(self.players[i]['hand'], self.community_card)]
                      for i in range(2)]
            if scores[0] < scores[1]:
                # player 0 wins
                self.players[0]['bankroll'] += self.pot
            elif scores[0] > scores[1]:
                # player 1 wins
                self.players[1]['bankroll'] += self.pot
            else:
                # split pot
                self.players[0]['bankroll'] += self.pot / 2
                self.players[1]['bankroll'] += self.pot / 2

    @staticmethod
    def _create_hand(hold_card, community_card):
        hand = ""
        sorted_hand = [hold_card[1], community_card[1]]
        sorted_hand.sort()
        for card in sorted_hand:
            hand += card
        return hand
