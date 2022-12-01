import random
from numpy import sqrt, log

import os
import argparse

import torch

import rlcard
from rlcard.agents import DQNAgent
from rlcard.agents.dqn_agent import Estimator
from rlcard.agents.dqn_agent import EstimatorNetwork
from rlcard.utils import (
    get_device,
    set_seed,
    tournament,
    reorganize,
    Logger,
    plot_curve,
)

from games.holdem.translate_state import state_to_DQN
from games.holdem.holdem_game import HoldemPoker


def get_DQN_values(state):
    env = rlcard.make(
        'limit-holdem',
        config={
            'seed': 17,
        }
    )

    DQN_state = env._extract_state(state)
    agent = torch.load("./agents/holdem/logs/model.pth")
    return agent.predict(DQN_state)


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
        for card in state.community_cards:
            deck.remove(card)
        card1 = random.choice(deck)
        deck.remove(card1)
        card2 = random.choice(deck)
        deck.remove(card2)
        return [card1, card2]

    def get_action(self, state: HoldemPoker):
        num_iterations = 100
        Q = {}
        N = {}
        T = {}
        for itr in range(num_iterations):
            model_game = state.__copy__()
            initial_bankroll = model_game.players[0]["bankroll"]
            path = []
            while not model_game.is_game_over():
                # make move
                # initialize new Q values
                actions = model_game.get_legal_actions()
                S = model_game.serialize()
                s_test = model_game.get_state()
                print(get_DQN_values(state_to_DQN(s_test)))
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
                A = random.choice(candidate_actions)
                model_game.make_move(A)
                path.append((S, A))
                # check for terminal state and store results
                if model_game.is_game_over():
                    break

                # opponent make move
                opponent_action = self.opponent_action_model(model_game)
                model_game.make_move(opponent_action)
            final_bankroll = model_game.players[0]['bankroll']
            R = final_bankroll - initial_bankroll
            for SA in path:
                Q[SA] = Q[SA] + (1 / N[SA]) * (R - Q[SA])
        # pick best action greedily
        S = state.serialize()
        actions = state.get_legal_actions()
        best_action = actions[0]
        for action in actions:
            if Q[(S, action)] > Q[(S, best_action)]:
                best_action = action
        return best_action
