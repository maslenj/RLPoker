from pprint import pprint
import json
import copy

"""
State:
    - Player's cards
    - Observable cards (if any)
    - Total pot
    - Calling amount
    - Current bankroll
    - Opponent's bankroll

Actions:
    - Call, amount
    - Check, amount
    - Bet, amount
    - Fold, amount
"""


def gen_episode(p, hand):
    player = hand['players'][p]
    opp_p = (p - 1) * -1
    ep = []
    pots = []
    for stage in ['f', 't', 'r', 's']:
        p = [h for h in hand['pots'] if h['stage'] == stage][0]
        pots.append((p['num_players'], p['size']))

    S = {'a_cards': player['pocket_cards'], 'o_cards': [], 'pot': None, 'call': None,
         'curr_bank': player['bankroll'],
         'opp_bank': hand['players'][opp_p]['bankroll']}

    for i, bet_round in enumerate(player['bets']):
        S = copy.deepcopy(S)
        A = bet_round
        S['curr_bank'] = player['bankroll']
        S['opp_bank'] = hand['players'][opp_p]['bankroll']
        if bet_round['stage'] == 'p':
            S['o_cards'] = []
            S['pot'] = pots[0]
            if pots[0][0] == 0:
                S['call'] = min(player['bankroll'], hand['players'][opp_p]['bankroll'])
            else:
                S['call'] = pots[0][1] / pots[0][0]
            R = 0
            ep.append((S, A, R))
        elif bet_round['stage'] == 'f':
            S['o_cards'] = hand['board'][:3]
            S['pot'] = pots[1]
            if pots[1][0] == 0:
                # print(ep)
                S['call'] = min(player['bankroll'], hand['players'][opp_p]['bankroll'])
            else:
                S['call'] = pots[1][1] / pots[1][0]
            R = 0
            ep.append((S, A, R))
        elif bet_round['stage'] == 't':
            S['o_cards'] = hand['board'][:4]
            S['pot'] = pots[2]
            if pots[2][0] == 0:
                # print(ep)
                S['call'] = min(player['bankroll'], hand['players'][opp_p]['bankroll'])
            else:
                S['call'] = pots[2][1] / pots[2][0]
            R = 0
            ep.append((S, A, R))
        elif bet_round['stage'] == 'r':
            S['o_cards'] = hand['board'][:]
            S['pot'] = pots[3]
            if pots[3][0] == 0:
                # print(ep)
                S['call'] = min(player['bankroll'], hand['players'][opp_p]['bankroll'])
            else:
                S['call'] = pots[3][1] / pots[3][0]
            R = player['winnings']
            ep.append((S, A, R))

    return ep


def generate_episodes(filename):
    episodes = []  # Format is State, action, reward
    try:
        with open(filename, 'r') as f:
            # print('#' * 60)
            # actions = {'B': 'blind', 'k': 'check', 'b': 'bet', 'c': 'call', '-': 'All-in', 'r': 'raise'}
            line = f.readline()
            while line:
                hand = json.loads(line)
                if len(hand['players']) < 3:
                    eps = [gen_episode(0, hand), gen_episode(1, hand)]
                    for e in eps:
                        if e is not None:
                            episodes.append(e)

                # print('#' * 60)
                line = f.readline()
        print(len(episodes))
        print('Episodes generated.')
    except KeyboardInterrupt:
        print('Interrupted.')
    return episodes


def main():
    generate_episodes("hands_valid.json")


if __name__ == '__main__':
    main()
