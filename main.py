import rlcard
from rlcard.agents import LeducholdemHumanAgent as HumanAgent
from leduc_random_agent import RandomAgent
from leduc_logic_agent import LogicAgent


# Make environment
env = rlcard.make('leduc-holdem')
random_agent = RandomAgent()
logic_agent = LogicAgent()
env.set_agents([
    random_agent,
    logic_agent,
])

# run 1000 simulations
player_1_avg = 0
player_2_avg = 0
num_games = 1000

env.run(is_training=False)
exit()

for i in range(num_games):
    _, payoffs = env.run(is_training=False)
    player_1_avg += payoffs[0]
    player_2_avg += payoffs[1]
player_1_avg /= num_games
player_2_avg /= num_games
print(f"after {num_games} games: \nplayer 1 averaged {player_1_avg} points \nplayer 2 averaged {player_2_avg} points")
