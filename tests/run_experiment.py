from games.holdem.holdem_game import HoldemPoker
from agents.holdem.holdem_random_agent import HoldemRandomAgent
from agents.holdem.holdem_mcts_agent import HoldemMCTSAgent
from agents.holdem.holdem_dqn_agent import HoldemDQNAgent


def run_experiment(num_games, agents):
    game = HoldemPoker(bankrolls=(100, 100))
    for game_number in range(num_games):
        print(game_number)
        player_bankrupt = False
        for p in game.players:
            if p["bankroll"] < game.raise_amount:
                player_bankrupt = True
        if player_bankrupt:
            print("game ended by player bankruptcy")
            break
        game.new_game()
        while not game.is_game_over():
            action = agents[game.current_player].get_action(game)
            game.make_move(action)
    print(f"player 0 result: {game.players[0]['bankroll']}")
    print(f"player 1 result: {game.players[1]['bankroll']}")


def main():
    agents1 = [HoldemMCTSAgent(1000), HoldemDQNAgent()]
    agents2 = [HoldemMCTSAgent(1000), HoldemRandomAgent()]
    run_experiment(50, agents1)
    run_experiment(50, agents2)


if __name__ == '__main__':
    main()
