import time

from board import Board
from evaluator import MiddleEvaluator, FinalEvaluator
from minimax import Minimax
from minimax_thread import Minimax_Threaded


class Player:
    def __init__(self, my_stone):
        self.my_stone = my_stone

    def get_my_stone(self):
        return self.my_stone


conv_col2int = str.maketrans("ABCDEFGH", "12345678")


class HumanPlayer(Player):
    def __init__(self, my_stone):
        super().__init__(my_stone)

    def next_move(self, board):
        _pos_str = input("Position? ").upper().translate(conv_col2int)
        return (int(_pos_str[0]), int(_pos_str[1]))

    def __str__(self):
        return "Human"


class ComputerPlayer(Player):
    def __init__(self, my_stone, max_search_level=5, num_thread=1):
        super().__init__(my_stone)
        self.max_search_level = max_search_level
        self.num_thread = num_thread
        if 1 < self.num_thread:
            self.selector = Minimax_Threaded(MiddleEvaluator(), self.my_stone, self.num_thread)
        else:
            self.selector = Minimax(MiddleEvaluator(), self.my_stone)

    def next_move(self, board):
        if board.count_blank() <= self.max_search_level + 7:
            if 1 < self.num_thread:
                self.selector = Minimax_Threaded(FinalEvaluator(), self.my_stone, num_thread=self.num_thread)
            else:
                self.selector = Minimax(FinalEvaluator(), self.my_stone)
            self.max_search_level = board.count_blank()

        _start_time = time.time()
        _pos, _eval, _eval_num = self.selector.search_next_move(board, self.max_search_level)
        _end_time = time.time()
        _elapsed_time = _end_time - _start_time
        _time_per_eval = 1000 * _elapsed_time / _eval_num
        print("Put: {} Eval: {} (level:{} num:{} time:{:.2f}s tpe:{:.2f}ms)".format(
            self._pos2str(_pos), _eval, self.max_search_level, _eval_num, _elapsed_time, _time_per_eval))
        return _pos

    def _pos2str(self, pos):
        int2str_tbl = "-ABCDEFGH-"
        return int2str_tbl[pos[0]] + str(pos[1])

    def __str__(self):
        return "Computer"
