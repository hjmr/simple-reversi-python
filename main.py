import argparse

from board import Stone, Board
from game import Game

from player import HumanPlayer, ComputerPlayer


def parse_args():
    parser = argparse.ArgumentParser(description="Simple Reversi")
    parser.add_argument("-t", "--thread_num", type=int, default=1, help="The number of threading.")
    parser.add_argument("-c", "--computer_first", action="store_true",
                        help="Computer is the first player (white stone).")
    parser.add_argument("-p", "--use_process", action="store_true",
                        help="Specify when to use ProcessPoolExecutor instead of ThreadPoolExecutor.")
    parser.add_argument("-l", "--level", type=int, default=5, help="Specify the level of computer player.")
    return parser.parse_args()


def run(players):
    _str_stone = {Stone.BLACK: "Black", Stone.WHITE: "White"}
    _curr_turn = Stone.BLACK

    _board = Board()

    _pass_num = 0
    while _pass_num < 2:
        print("---------------------------------------")
        print(_board)
        print("Turn: {} ({})".format(_str_stone[_curr_turn], players[_curr_turn]))

        if not Game.possible_to_put_stone(_board, _curr_turn):
            _pass_num += 1
            print("Pass.")
        else:
            _pass_num = 0
            _done = False
            while not _done:
                _pos = players[_curr_turn].next_move(_board)
                if Game.possible_to_put_stone_at(_board, _curr_turn, _pos):
                    Game.put_stone_at(_board, _curr_turn, _pos)
                    Game.reverse_stones_from(_board, _pos)
                    _done = True
        _curr_turn = Stone.reverse(_curr_turn)

    black_num = _board.count_stones(Stone.BLACK)
    white_num = _board.count_stones(Stone.WHITE)
    print("Black:{} White:{}".format(black_num, white_num))


if __name__ == "__main__":
    args = parse_args()
    players = {}
    if args.computer_first:
        players = {Stone.BLACK: ComputerPlayer(Stone.BLACK, args.level, args.thread_num, args.use_process),
                   Stone.WHITE: HumanPlayer(Stone.WHITE)}
    else:
        players = {Stone.BLACK: HumanPlayer(Stone.BLACK),
                   Stone.WHITE: ComputerPlayer(Stone.WHITE, args.level, args.thread_num, args.use_process)}
    run(players)
