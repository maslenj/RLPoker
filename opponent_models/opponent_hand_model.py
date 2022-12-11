from episode import generate_episodes


class OpponentHandModel:
    def __init__(self, episodes=None):
        # train models
        # import data set
        pass


def main():
    episodes = generate_episodes("../hands_valid.json")
    OpponentHandModel(episodes=episodes)


if __name__ == '__main__':
    main()
