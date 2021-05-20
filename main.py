import argparse

import stone
from game import ConsoleGame
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


def run(args):
    com_stone, man_stone = (stone.BLACK, stone.WHITE) if args.computer_first else (stone.WHITE, stone.BLACK)
    players = {com_stone: ComputerPlayer(com_stone, args.level, args.thread_num, args.use_process),
               man_stone: HumanPlayer(man_stone)}
    game = ConsoleGame(players)
    game.play()


if __name__ == "__main__":
    run(parse_args())
