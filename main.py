import argparse

import stone
from game import ConsoleGame
from player import HumanPlayer, MinimaxThreadPlayer, McsPlayer
from gui import HumanGUIPlayer, GUIGame

from evaluator import PutPosEvaluator, PutPosCornerEvaluator, StoneNumEvaluator


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

    com1_player = McsPlayer("MCS", com_stone, try_num = args.level)
    # com2_player = MinimaxThreadPlayer("PPC-211", man_stone, PutPosCornerEvaluator(2, 1, 1), StoneNumEvaluator(), args.level, args.thread_num)
    # players = {com_stone: com1_player, man_stone: com2_player}
    man_player = HumanGUIPlayer(man_stone) if args.use_gui else HumanPlayer(man_stone)
    players = {com_stone: com1_player, man_stone: man_player}

    game = GUIGame(players) if args.use_gui else ConsoleGame(players)
    game.play()


if __name__ == "__main__":
    run(parse_args())
