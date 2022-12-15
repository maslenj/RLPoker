import numpy as np
import matplotlib.pyplot as plt

from tests.run_experiment import run_experiment
from agents.holdem.holdem_dqn_agent import HoldemDQNAgent


def main():
    dqn_names = [
        "DQN with initialization",
        "Plain DQN"
    ]

    dqn_agents = [
        HoldemDQNAgent('../agents/holdem/logs/model.pth'),
        HoldemDQNAgent('../agents/holdem/plain_dqn_logs/model.pth')
    ]

    results = np.array([[0.5 for _ in range(len(dqn_agents))] for _ in range(len(dqn_agents))])

    print(f"running DQN with initialization vs Plain DQN")
    num_wins = 0
    games_to_play = 50
    num_hands_per_game = 25

    for g in range(games_to_play):
        print(f"{g + 1}/{games_to_play}")
        i_br, j_br = run_experiment(num_hands_per_game, [dqn_agents[0], dqn_agents[1]])
        if i_br > j_br:
            num_wins += 1
    results[0][1] = num_wins / games_to_play
    results[1][0] = 1 - results[0][1]

    for row in results:
        for col in row:
            print(col, end=', ')
        print()

    fig, ax = plt.subplots()
    im = ax.imshow(results)

    # Show all ticks and label them with the respective list entries
    ax.set_xticks(np.arange(len(dqn_names)), labels=dqn_names)
    ax.set_yticks(np.arange(len(dqn_names)), labels=dqn_names)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    for i in range(len(dqn_names)):
        for j in range(len(dqn_names)):
            text = ax.text(j, i, round(results[i, j], 2),
                           ha="center", va="center", color="w")

    ax.set_title("Results of Head to Head DQN Match by Win Percentage")
    fig.tight_layout()
    plt.show()

    print("done")


if __name__ == '__main__':
    main()
