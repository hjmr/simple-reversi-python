from board import Stone
from game import Game

conv_str2int = str.maketrans("abcdefgh", "12345678")
curr_turn = Stone.BLACK

game = Game()

while True:
    print("---------------------------------------")
    print(game)
    if curr_turn == Stone.BLACK:
        print("Turn: Black")
    else:
        print("Turn: White")

    if not game.possible_to_put_stone(curr_turn):
        print("Pass.")
    else:
        done = False
        while not done:
            pos_str = input("Position? ").lower().translate(conv_str2int)
            pos = (int(pos_str[0]), int(pos_str[1]))
            if game.possible_to_put_stone_at(curr_turn, pos):
                game.put_stone_at(curr_turn, pos)
                game.reverse_stones_from(pos)
                done = True

    curr_turn = Stone.reverse(curr_turn)
