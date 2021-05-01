from board import Stone, Board
from game import Game

from player import HumanPlayer, ComputerPlayer

human_player = HumanPlayer()
computer_player = ComputerPlayer(Stone.WHITE)

str_stone = {Stone.BLACK: "Black", Stone.WHITE: "White"}
players = {Stone.BLACK: human_player, Stone.WHITE: computer_player}
curr_turn = Stone.BLACK

board = Board()

pass_num = 0
while pass_num < 2:
    print("---------------------------------------")
    print(board)
    print("Turn: {} ({})".format(str_stone[curr_turn], players[curr_turn]))

    if not Game.possible_to_put_stone(board, curr_turn):
        pass_num += 1
        print("Pass.")
    else:
        pass_num = 0
        done = False
        while not done:
            pos = players[curr_turn].next_move(board)
            if Game.possible_to_put_stone_at(board, curr_turn, pos):
                Game.put_stone_at(board, curr_turn, pos)
                Game.reverse_stones_from(board, pos)
                done = True
    curr_turn = Stone.reverse(curr_turn)

black_num = board.count_stones(Stone.BLACK)
white_num = board.count_stones(Stone.WHITE)
print("Black:{} White:{}".format(black_num, white_num))
