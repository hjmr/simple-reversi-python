from board import Stone, Board
from game import Game
from evaluator import Evaluator
from minimax import Minimax

conv_str2int = str.maketrans("ABCDEFGH", "12345678")


def pos2str(pos):
    int2str_tbl = "-ABCDEFGH-"
    return int2str_tbl[pos[0]] + str(pos[1])


str_stone = {Stone.BLACK: "Black", Stone.WHITE: "White"}
str_player = {Stone.BLACK: "Human", Stone.WHITE: "Computer"}
curr_turn = Stone.BLACK

board = Board()
evaluator = Evaluator()
chooser = Minimax(evaluator, Stone.WHITE)

pass_num = 0
while pass_num < 2:
    print("---------------------------------------")
    print(board)
    print("evaluation: {}".format(evaluator.eval(board, Stone.BLACK)))
    print("Turn: {} ({})".format(str_stone[curr_turn], str_player[curr_turn]))

    if not Game.possible_to_put_stone(board, curr_turn):
        print("Pass.")
        pass_num += 1
    else:
        pass_num = 0
        if str_player[curr_turn] == "Computer":
            pos, val, eval_num = chooser.find_next_move(board, 5)
            print("Put: {} Eval: {} ({})".format(pos2str(pos), val, eval_num))
            Game.put_stone_at(board, curr_turn, pos)
            Game.reverse_stones_from(board, pos)
        else:
            done = False
            while not done:
                pos_str = input("Position? ").upper().translate(conv_str2int)
                pos = (int(pos_str[0]), int(pos_str[1]))
                if Game.possible_to_put_stone_at(board, curr_turn, pos):
                    Game.put_stone_at(board, curr_turn, pos)
                    Game.reverse_stones_from(board, pos)
                    done = True

    curr_turn = Stone.reverse(curr_turn)

black_num = board.count_stones(Stone.BLACK)
white_num = board.count_stones(Stone.WHITE)
print("Black:{} White:{}".format(black_num, white_num))
