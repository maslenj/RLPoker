import pandas as pd
from pokerlib import HandParser
from games.holdem.holdem_game import HoldemPoker
import os
import random

HUMAN_HAND = 5
COMPUTER_HAND = 6
FLOP_CARDS = 7
TURN_CARD = 8
RIVER_CARD = 9
POSITION = 10
PRE_FLOP_ACTIONS = 11
FLOP_ACTIONS = 12
TURN_ACTIONS = 13
RIVER_ACTIONS = 14


def rank_hand(player_hand, game_board, sampling_amount=100):
    deck = HoldemPoker.DECK.copy()
    for card in game_board + player_hand:
        deck.remove(card)
    rank_dict = HoldemPoker.RankDict
    suit_dict = HoldemPoker.SuitDict

    board = [
        (rank_dict[game_board[i][0]], suit_dict[game_board[i][1]])
        for i in range(len(game_board))
    ]
    player_hand = HandParser([
        (rank_dict[player_hand[0][0]], suit_dict[player_hand[0][1]]),
        (rank_dict[player_hand[1][0]], suit_dict[player_hand[1][1]])
    ])
    player_hand += board
    player_hand.parse()

    # randomly sample 1000 hands and record how many we are better than
    num_wins = 0
    num_samples = sampling_amount
    for i in range(num_samples):
        deck_copy = deck.copy()
        card_1 = random.choice(deck_copy)
        deck_copy.remove(card_1)
        card_2 = random.choice(deck_copy)
        deck_copy.remove(card_2)
        hand = HandParser([
            (rank_dict[card_1[0]], suit_dict[card_1[1]]),
            (rank_dict[card_2[0]], suit_dict[card_2[1]])
        ])
        hand += board
        hand.parse()
        if player_hand > hand:
            num_wins += 1
        elif player_hand == hand:
            num_wins += 0.5

    return num_wins / num_samples


def main():
    results = []

    for filename in os.listdir("../AIVAT_analysis"):
        print(filename)
        df = pd.read_csv(f"../AIVAT_analysis/{filename}")
        for row in df.values:
            # extract data from row
            human_hand = [row[HUMAN_HAND][1:][2 * i:2 * i + 2] for i in range(2)]
            computer_hand = [row[COMPUTER_HAND][1:][2 * i:2 * i + 2] for i in range(2)]
            flop_cards = [row[FLOP_CARDS][1:][2 * i:2 * i + 2] for i in range(3)]
            turn_card = row[TURN_CARD][1:]
            river_card = row[RIVER_CARD][1:]
            human_position = row[POSITION]
            pre_flop_actions_str = row[PRE_FLOP_ACTIONS].strip(' ')
            flop_actions_str = row[FLOP_ACTIONS].strip(' ')
            turn_actions_str = row[TURN_ACTIONS].strip(' ')
            river_actions_str = row[RIVER_ACTIONS].strip(' ')

            # check if hand reached showdown
            if len(river_actions_str) > 0 and river_actions_str[-1].lower() != 'f':
                # hand reached showdown
                bb_hand = human_hand if human_position == 'bb' else computer_hand
                sb_hand = computer_hand if human_position == 'bb' else human_hand
                bb_raises = pre_flop_actions_str.count('R') + flop_actions_str.count('R') + turn_actions_str.count('R') + \
                    river_actions_str.count('R')
                sb_raises = pre_flop_actions_str.count('r') + flop_actions_str.count('r') + turn_actions_str.count('r') + \
                    river_actions_str.count('r')
                board = flop_cards + [turn_card] + [river_card]
                results.append(str(bb_raises) + ',' + str(rank_hand(bb_hand, board)) + '\n')
                results.append(str(sb_raises) + ',' + str(rank_hand(sb_hand, board)) + '\n')

    with open("hand_modeling_data.csv", 'w') as f:
        for result in results:
            f.write(result)


if __name__ == '__main__':
    main()
