import rlcard
from agents.leduc.leduc_random_agent import RandomAgent
from agents.leduc.leduc_logic_agent import LogicAgent
import rlcard.envs.leducholdem


# Make environment
env = rlcard.make('leduc-holdem')

print(env)
exit()

random_agent = RandomAgent()
logic_agent = LogicAgent()
env.set_agents([
    random_agent,
    logic_agent,
])

# run 1000 simulations
player_1_avg = 0
player_2_avg = 0
num_games = 10000

for i in range(num_games):
    _, payoffs = env.run(is_training=False)
    player_1_avg += payoffs[0]
    player_2_avg += payoffs[1]
player_1_avg /= num_games
player_2_avg /= num_games
print(f"after {num_games} games: \nplayer 1 (random) averaged {player_1_avg} points \nplayer 2 (logic) averaged {player_2_avg} points")
