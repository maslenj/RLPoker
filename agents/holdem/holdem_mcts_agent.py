import math
import random
import pickle
import numpy as np
import torch
import rlcard

from dataset_generation.test_hand_strength_data import build_raise_dictionary
from dataset_generation.hand_strength_data_generation import rank_hand
from games.holdem.translate_state import state_to_DQN
from games.holdem.holdem_game import HoldemPoker


def get_dqn_values(state, agent):
    env = rlcard.make(
        'limit-holdem',
        config={
            'seed': 17,
        }
    )
    DQN_state = env._extract_state(state)
    return agent.predict(DQN_state)


class HoldemMCTSAgent:
    c = 1

    def __init__(self, num_rollouts=100, use_dqn=True):
        self.action_model = pickle.load(open('../dataset_generation/ActionModel.sav', 'rb'))
        self.num_rollouts = num_rollouts
        self.raise_dict = build_raise_dictionary()
        self.use_dqn = use_dqn

    def opponent_action_model(self, state: HoldemPoker):
        input_feature = [state.round_number, state.calling_amount, state.pot]
        prediction = self.action_model.predict_proba(np.array(input_feature, ndmin=2))
        prediction = prediction[0]
        choices = state.get_legal_actions()
        if len(choices) == 2:
            p = [prediction[0] + (prediction[1] / 2), prediction[2] + (prediction[1] / 2)]
        else:
            p = prediction
        return np.random.choice(choices, p=p)

    def opponent_hand_model(self, state: HoldemPoker):
        # assuming that we are player 1
        deck = HoldemPoker.DECK.copy()
        deck.remove(state.players[0]['hand'][0])
        deck.remove(state.players[0]['hand'][1])
        for card in state.community_cards:
            deck.remove(card)

        # count number of raises by opponent in round
        num_raises = 0
        for i in range(len(state.action_history) - 2, -1, -2):
            if state.action_history[i] == 'raise':
                num_raises += 1

        # sample hand strength based on the number of raises

        expected_hand_strength = random.choice(self.raise_dict[num_raises])
        epsilon = 0.05

        card1 = random.choice(deck)
        deck.remove(card1)
        card2 = random.choice(deck)
        deck.remove(card2)
        hand_strength = rank_hand([card1, card2], state.community_cards)
        while abs(hand_strength - expected_hand_strength) > epsilon:
            deck.append(card1)
            deck.append(card2)
            card1 = random.choice(deck)
            deck.remove(card1)
            card2 = random.choice(deck)
            deck.remove(card2)
            hand_strength = rank_hand([card1, card2], state.community_cards)
        return [card1, card2]

    def get_action(self, state: HoldemPoker):
        Q = {}
        N = {}
        T = {}
        agent = torch.load("../agents/holdem/logs/model.pth")
        for itr in range(self.num_rollouts):
            model_game = state.__copy__()
            initial_bankroll = model_game.players[0]["bankroll"]
            path = []
            while not model_game.is_game_over():
                # make move
                # initialize new Q values
                actions = model_game.get_legal_actions()
                S = model_game.serialize()
                s_test = model_game.get_state()
                DQN_values = get_dqn_values(state_to_DQN(s_test), agent)
                if S not in T:
                    T[S] = 0
                T[S] += 1
                for A in actions:
                    if (S, A) not in Q:
                        if not self.use_dqn:
                            Q[(S, A)] = 0
                        elif A == "call":
                            if DQN_values[0] != -math.inf:
                                Q[(S, A)] = DQN_values[0]
                            else:
                                Q[(S, A)] = DQN_values[3]
                        elif A == "raise":
                            Q[(S, A)] = DQN_values[1]
                        elif A == "fold":
                            Q[(S, A)] = DQN_values[2]
                    if (S, A) not in N:
                        N[(S, A)] = 0
                    N[(S, A)] += 1
                action_values = [Q[(S, A)] + self.c * np.sqrt(np.log(T[S]) / N[S, A]) for A in actions]
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
