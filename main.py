from board import Stone, Board
from game import Game

conv_str2int = str.maketrans("abcdefgh", "12345678")
curr_turn = Stone.BLACK

board = Board()

while True:
    print("---------------------------------------")
    print(board)
    if curr_turn == Stone.BLACK:
        print("Turn: Black")
    else:
        print("Turn: White")

    if not Game.possible_to_put_stone(board, curr_turn):
        print("Pass.")
    else:
        done = False
        while not done:
            pos_str = input("Position? ").lower().translate(conv_str2int)
            pos = (int(pos_str[0]), int(pos_str[1]))
            if Game.possible_to_put_stone_at(board, curr_turn, pos):
                Game.put_stone_at(board, curr_turn, pos)
                Game.reverse_stones_from(board, pos)
                done = True

    curr_turn = Stone.reverse(curr_turn)
