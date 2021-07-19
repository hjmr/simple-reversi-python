import argparse

import stone
from game import ConsoleGame
from player import HumanPlayer, ComputerPlayer
from gui import HumanGUIPlayer, GUIGame

from evaluator import PutPosEvaluator, PutPosCornerEvaluator, AverageEvaluator, StoneNumEvaluator


def parse_args():
    parser = argparse.ArgumentParser(description="Simple Reversi")
    parser.add_argument("-t", "--thread_num", type=int, default=4, help="The number of threading.")
    parser.add_argument("-c", "--computer_first", action="store_true",
                        help="Computer is the first player (white stone).")
    parser.add_argument("-l", "--level", type=int, default=6, help="Specify the level of computer player.")
    parser.add_argument("-g", "--use_gui", action="store_true", help="Use GUI.")
    return parser.parse_args()


def run(args):
    com_stone, man_stone = (stone.BLACK, stone.WHITE) if args.computer_first else (stone.WHITE, stone.BLACK)

    com_player = ComputerPlayer(com_stone, PutPosCornerEvaluator(), StoneNumEvaluator(), args.level, args.thread_num)
    man_player = HumanGUIPlayer(man_stone) if args.use_gui else HumanPlayer(man_stone)
    players = {com_stone: com_player, man_stone: man_player}

    game = GUIGame(players) if args.use_gui else ConsoleGame(players)
    game.play()


if __name__ == "__main__":
    run(parse_args())
