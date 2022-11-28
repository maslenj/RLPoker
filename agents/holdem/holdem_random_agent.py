from games.holdem.holdem_game import HoldemPoker
import random


class HoldemRandomAgent:
    def get_action(self, state: HoldemPoker):
        action = random.choice(state.get_legal_actions())
        return action
