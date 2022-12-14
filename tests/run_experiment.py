from games.holdem.holdem_game import HoldemPoker
from agents.holdem.holdem_random_agent import HoldemRandomAgent
from agents.holdem.holdem_mcts_agent import HoldemMCTSAgent
from agents.holdem.holdem_dqn_agent import HoldemDQNAgent
import numpy as np
import matplotlib.pyplot as plt


def run_experiment(num_hands, agents):
    game = HoldemPoker(bankrolls=(100, 100))
    for hand_number in range(num_hands):
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
    return game.players[0]['bankroll'], game.players[1]['bankroll']


def main():
    names = [
        "MCTS w/ DQN",
        "MCTS w/out DQN",
        "DQN",
        "Random"
    ]
    agents = [
        HoldemMCTSAgent(500, use_dqn=True),
        HoldemMCTSAgent(500, use_dqn=False),
        HoldemDQNAgent('../agents/holdem/plain_dqn_logs/model.pth'),
        HoldemRandomAgent(),
    ]
    results = np.array([[0.5 for _ in range(len(agents))] for _ in range(len(agents))])

    # run grid tournament
    for i in range(len(agents)):
        for j in range(i + 1, len(agents)):
            print(f"running {names[i]} vs {names[j]}")
            num_wins = 0
            games_to_play = 50
            for g in range(games_to_play):
                print(f"{g + 1}/{games_to_play}")
                i_br, j_br = run_experiment(25, [agents[i], agents[j]])
                if i_br > j_br:
                    num_wins += 1
            results[i][j] = num_wins / games_to_play
            results[j][i] = 1 - results[i][j]

    for row in results:
        for col in row:
            print(col, end=', ')
        print()

    fig, ax = plt.subplots()
    im = ax.imshow(results)

    # Show all ticks and label them with the respective list entries
    ax.set_xticks(np.arange(len(names)), labels=names)
    ax.set_yticks(np.arange(len(names)), labels=names)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    for i in range(len(names)):
        for j in range(len(names)):
            text = ax.text(j, i, round(results[i, j], 2),
                           ha="center", va="center", color="w")

    ax.set_title("Results of Tournament by Win Percentage")
    fig.tight_layout()
    plt.show()

    print("done")


if __name__ == '__main__':
    main()
