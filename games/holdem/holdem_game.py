from pokerlib import HandParser
from pokerlib.enums import Value, Suit


class HoldemPoker:
    SUITS = ['s', 'h', 'c', 'd']
    RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    DECK_CARDS = [x + y for x in RANKS for y in SUITS]
    PLAYER_0_WIN = 0
    PLAYER_1_WIN = 1
    SPLIT_POT    = 2
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
