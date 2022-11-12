from games.leduc.leduc_game import LeducPoker

game = LeducPoker(100, 100)

while not game.is_game_over:
    print(f"it's player {game.to_play}'s turn")
    print(f"pot: {game.pot}")
    print(f"hand card: {game.players[game.to_play]['hand']}")
    if game.round == 1:
        print(f"community card: {game.community_card}")
    print(f"amount to call: {game.to_call}")
    print(f"available actions: {game.get_legal_actions()}")
    action = input("what is your action?\n")
    game.step(action)

print("player bankrolls")
print(f"player 0 bankroll: {game.players[0]['bankroll']}")
print(f"player 1 bankroll: {game.players[1]['bankroll']}")
