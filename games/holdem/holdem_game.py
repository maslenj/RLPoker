from pokerlib import HandParser
from pokerlib.enums import Value, Suit
import random


class HoldemPoker:
    DECK = ['2s', '2h', '2c', '2d', '3s', '3h', '3c', '3d', '4s', '4h', '4c', '4d', '5s', '5h', '5c', '5d',
            '6s', '6h', '6c', '6d', '7s', '7h', '7c', '7d', '8s', '8h', '8c', '8d', '9s', '9h', '9c', '9d',
            'Ts', 'Th', 'Tc', 'Td', 'Js', 'Jh', 'Jc', 'Jd', 'Qs', 'Qh', 'Qc', 'Qd', 'Ks', 'Kh', 'Kc', 'Kd',
            'As', 'Ah', 'Ac', 'Ad']
    PLAYER_0_WIN = 0
    PLAYER_1_WIN = 1
    SPLIT_POT = 2
    RankDict = {
        'A': Value.ACE,
        '2': Value.TWO,
        '3': Value.THREE,
        '4': Value.FOUR,
        '5': Value.FIVE,
        '6': Value.SIX,
        '7': Value.SEVEN,
        '8': Value.EIGHT,
        '9': Value.NINE,
        'T': Value.TEN,
        'J': Value.JACK,
        'Q': Value.QUEEN,
        'K': Value.KING,
    }
    SuitDict = {
        's': Suit.SPADE,
        'h': Suit.HEART,
        'd': Suit.DIAMOND,
        'c': Suit.CLUB,
    }

    def __init__(self, bankrolls=(100, 100)):
        self.num_players = 2
        self.deck = self.DECK.copy()
        self.community_cards = []
        self.round_number = 0
        self.bet_number = 0
        self.pot = 0
        self.calling_amount = 0
        self.raise_amount = 5
        self.start_player = 0
        self.current_player = 0
        self.num_raises = 0
        self.game_over = False
        self.players = [
            {
                'hand': [],
                'bankroll': bankrolls[i]
            } for i in range(self.num_players)
        ]

    def get_legal_actions(self):
        actions = ['call', 'raise', 'fold']
        if self.num_raises > 1:
            actions.remove('raise')
        if self.is_game_over():
            actions = []
        return actions

    def game_step(self):
        if self.round_number == 4:
            result = self.decide_winner()
            if result == HoldemPoker.PLAYER_0_WIN:
                self.players[0]['bankroll'] += self.pot
            elif result == HoldemPoker.PLAYER_1_WIN:
                self.players[1]['bankroll'] += self.pot
            else:
                self.players[0]['bankroll'] += self.pot / 2
                self.players[1]['bankroll'] += self.pot / 2
            self.game_over = True
        if self.round_number == 0:
            for p in self.players:
                for i in range(2):
                    p['hand'].append(self.deal_card())
        elif self.round_number == 1:
            for i in range(3):
                self.community_cards.append(self.deal_card())
        else:
            self.community_cards.append(self.deal_card())

    def make_move(self, action):
        if action not in self.get_legal_actions():
            print("Illegal action")
            return
        if action == "call":
            self.pot += self.calling_amount
            self.players[self.current_player]['bankroll'] -= self.calling_amount
            self.calling_amount = 0
            self.current_player = (self.current_player + 1) % 2
            if self.bet_number > 0:
                self.round_number += 1
                self.game_step()
                self.bet_number = 0
                self.num_raises = 0
                return
            self.bet_number += 1
        elif action == 'fold':
            self.players[(self.current_player + 1) % 2]['bankroll'] += self.pot
            self.pot = 0
            self.game_over = True
            return
        else:
            # Raise
            self.pot += self.raise_amount + self.calling_amount
            self.players[self.current_player]['bankroll'] -= self.calling_amount + self.raise_amount
            self.calling_amount = self.raise_amount
            self.bet_number += 1
            self.current_player = (self.current_player + 1) % 2
            self.num_raises += 1

    def new_game(self):
        self.deck = self.DECK.copy()
        self.community_cards = []
        self.round_number = 0
        self.start_player = (self.start_player + 1) % 2
        self.bet_number = 0
        self.pot = 2 * self.raise_amount
        self.calling_amount = 0
        self.current_player = self.start_player
        self.num_raises = 0
        self.game_over = False
        for p in self.players:
            p['hand'] = []
            p['bankroll'] -= self.raise_amount
        self.game_step()

    # todo: Rob
    def is_game_over(self):
        return self.game_over

    def decide_winner(self):
        """
        Purpose: Computes the winner of the game and returns value.
        :return: The decision of the game
        """

        # alias dictionaries
        RankDict = HoldemPoker.RankDict
        SuitDict = HoldemPoker.SuitDict

        # build hands and use library to decide result
        hands = [HandParser([
            (RankDict[self.players[i]['hand'][0][0]], SuitDict[self.players[i]['hand'][0][1]]),
            (RankDict[self.players[i]['hand'][1][0]], SuitDict[self.players[i]['hand'][1][1]])
        ]) for i in range(2)]
        board = [
            (RankDict[self.community_cards[i][0]], SuitDict[self.community_cards[i][1]])
            for i in range(len(self.community_cards))
        ]
        hands[0] += board  # add the board to hand1
        hands[1] += board  # add the board to hand2
        hands[0].parse()
        hands[1].parse()

        # return result
        if hands[0] > hands[1]:
            return HoldemPoker.PLAYER_0_WIN
        elif hands[1] > hands[0]:
            return HoldemPoker.PLAYER_1_WIN
        else:
            return HoldemPoker.SPLIT_POT

    # todo: Rob
    def deal_card(self):
        card = random.choice(self.deck)
        self.deck.remove(card)
        return card

    # todo: Rob
    def input_state(self, state):
        self.deck, self.community_cards, self.round_number, \
        self.bet_number, self.pot, \
        self.calling_amount, self.start_player, \
        self.current_player, self.num_raises, \
        self.players = state

    # todo: Rob
    def print_state(self):
        stage = {0: 'Pre-flop', 1: 'Flop', 2: 'River', 3: 'Turn'}
        print("-----------------------------")
        print("Community cards:", self.community_cards)
        print("Round number:", self.round_number)
        print(f"Stage: {stage[self.round_number]}")
        print("Pot:", self.pot)
        print("Calling amount:", self.calling_amount)
        print("Bet number: ", self.bet_number)
        print("Current player: ", self.current_player)
        for i, player in enumerate(self.players):
            print("-----------------------------")
            print(f"Player: {i}")
            print("Hand:", player['hand'])
            print("Bankroll:", player['bankroll'])
        print("-----------------------------")


def main():
    P = HoldemPoker()
    while True:
        P.print_state()
        action = input()
        P.make_move(action)


if __name__ == '__main__':
    main()
