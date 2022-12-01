import copy

# raw_obs': {'hand': ['CK', 'SA'], 'public_cards': [], 'all_chips': [1, 2], 'my_chips': 1,
# 'legal_actions': ['raise', 'fold', 'check'], 'raise_nums': [0, 0, 0, 0]},
# 'raw_legal_actions': ['raise', 'fold', 'check'], 'action_record': [(0, 'fold')]}

# state = {'agent_hand': self.players[self.current_player]['hand'],
#                  'community_cards': self.community_cards,
#                  'pot': self.pot,
#                  'legal_actions': self.get_legal_actions(),
#                  'calling_amount': self.calling_amount,
#                  'round_raises': self.round_raises,
#                  }


def flip_card_representation(cards):
    new_cards = cards.copy()
    for i in range(len(cards)):
        new_cards[i] = new_cards[i][1].upper() + new_cards[i][0]
    return new_cards


def state_to_DQN(state):
    """
    Translates our env state to the RLCard DQN state

    :param state: Our env state
    :return: The DQN raw state
    """

    raw_state = dict()
    raw_state['hand'] = flip_card_representation(state['agent_hand'])
    raw_state['public_cards'] = flip_card_representation(state['community_cards'])
    curr_stake = (state['pot'] - state['calling_amount']) // 2
    raw_state['all_chips'] = [curr_stake, curr_stake + state['calling_amount']]
    raw_state['my_chips'] = curr_stake
    raw_state['legal_actions'] = state['legal_actions']
    if state['calling_amount'] == 0:
        raw_state['legal_actions'].pop(0)
        raw_state['legal_actions'].append('check')
    raw_state['raise_nums'] = state['round_raises']
    raw_state['raw_legal_actions'] = copy.deepcopy(raw_state['legal_actions'])
    raw_state['action_record'] = []
    print(raw_state)
    return raw_state

