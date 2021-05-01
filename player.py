import time

from board import Board
from evaluator import PutPosEvaluator, StoneNumEvaluator
from minimax import Minimax


class Player:
    def __init__(self):
        pass


conv_col2int = str.maketrans("ABCDEFGH", "12345678")


class HumanPlayer(Player):
    def __init__(self):
        super().__init__()

    def next_move(self, board):
        pos_str = input("Position? ").upper().translate(conv_col2int)
        return (int(pos_str[0]), int(pos_str[1]))

    def __str__(self):
        return "Human"


class ComputerPlayer(Player):
    def __init__(self, _my_stone, _max_search_level=5):
        super().__init__()
        self.max_search_level = _max_search_level
        self.my_stone = _my_stone
        self.selector = Minimax(PutPosEvaluator(), _my_stone)

    def next_move(self, _board):
        if _board.count_blank() < 15:
            self.selector = Minimax(StoneNumEvaluator(), self.my_stone)
            self.max_search_level = _board.count_blank()

        _start_time = time.time()
        _pos, _eval, _eval_num = self.selector.search_next_move(_board, self.max_search_level)
        _end_time = time.time()
        _elapsed_time = _end_time - _start_time
        print("Put: {} Eval: {} (level:{} num:{} time:{})".format(
            self._pos2str(_pos), _eval, self.max_search_level, _eval_num, _elapsed_time))
        return _pos

    def _pos2str(self, pos):
        int2str_tbl = "-ABCDEFGH-"
        return int2str_tbl[pos[0]] + str(pos[1])

    def __str__(self):
        return "Computer"
