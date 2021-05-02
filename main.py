import argparse

from board import Stone, Board
from game import Game

from player import HumanPlayer, ComputerPlayer


def parse_args():
    parser = argparse.ArgumentParser(description="Simple Reversi")
    parser.add_argument("-t", "--thread_num", type=int, default=1, help="The number of threading.")
    parser.add_argument("-c", "--computer_first", action="store_true",
                        help="Computer is the first player (white stone).")
    return parser.parse_args()


def run(players):
    str_stone = {Stone.BLACK: "Black", Stone.WHITE: "White"}
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


if __name__ == "__main__":
    args = parse_args()
    players = {}
    if args.computer_first:
        players = {Stone.BLACK: ComputerPlayer(Stone.BLACK, num_thread=args.thread_num),
                   Stone.WHITE: HumanPlayer(Stone.WHITE)}
    else:
        players = {Stone.BLACK: HumanPlayer(Stone.BLACK),
                   Stone.WHITE: ComputerPlayer(Stone.WHITE, num_thread=args.thread_num)}
    run(players)
