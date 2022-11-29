import math
import random
import numpy as np
from numpy import sqrt, log

from games.holdem.holdem_game import HoldemPoker


class HoldemMCTSAgent:
    c = 1

    @staticmethod
    def opponent_action_model(state: HoldemPoker):
        return random.choice(state.get_legal_actions())

    @staticmethod
    def opponent_hand_model(state: HoldemPoker):
        # assuming that we are player 1
        deck = HoldemPoker.DECK.copy()
        deck.remove(state.players[0]['hand'][0])
        deck.remove(state.players[0]['hand'][1])
        card1 = random.choice(deck)
        deck.remove(card1)
        card2 = random.choice(deck)
        deck.remove(card2)
        return [card1, card2]

    def get_action(self, state: HoldemPoker):
        num_iterations = 1000
        Q = {}
        N = {}
        T = {}
        for itr in range(num_iterations):
            model_game = HoldemPoker(state)
            while not model_game.is_game_over():
                # make move
                # initialize new Q values
                actions = model_game.get_legal_actions()
                S = model_game.serialize()
                if S not in T:
                    T[S] = 0
                T[S] += 1
                for A in actions:
                    if (S, A) not in Q:
                        Q[(S, A)] = 0
                    if (S, A) not in N:
                        N[(S, A)] = 0
                    N[(S, A)] += 1
                action_values = [Q[(S, A)] + self.c * sqrt(log(T[S]) / N[S, A]) for A in actions]
                best_val = max(action_values)
                candidate_actions = []
                for i in range(len(actions)):
                    if action_values[i] == best_val:
                        candidate_actions.append(actions[i])
                action = random.choice(candidate_actions)
                model_game.make_move(action)

                # check for terminal state and store results
                # opponent make move
                # check for terminal state and store results
                pass
        pass
