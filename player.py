import time

from board import Board
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
    def __init__(self, name, my_stone, middleEvaluator, finalEvaluator, max_search_level=5, num_thread=1):
        super().__init__(my_stone)
        self.name = name
        self.max_search_level = max_search_level
        self.num_thread = num_thread
        self.middleEvaluator = middleEvaluator
        self.finalEvaluator = finalEvaluator
        if 1 < self.num_thread:
            self.selector = Minimax_Threaded(self.middleEvaluator, self.my_stone, self.num_thread)
        else:
            self.selector = Minimax(self.middleEvaluator, self.my_stone)

    def next_move(self, a_board):
        if a_board.count_blank() < self.max_search_level + 8:
            if 1 < self.num_thread:
                self.selector = Minimax_Threaded(self.finalEvaluator, self.my_stone, num_thread=self.num_thread)
            else:
                self.selector = Minimax(self.finalEvaluator, self.my_stone)
            self.max_search_level = a_board.count_blank()

        _start_time = time.time()
        _pos, _eval, _eval_num = self.selector.search_next_move(a_board, self.max_search_level)
        _elapsed_time = time.time() - _start_time
        self._show_stat(_elapsed_time, _pos, _eval, _eval_num)
        return _pos

    def _show_stat(self, elapsed_time, pos, evaluation, evaluated_num):
        _time_per_eval_us = 1000 * 1000 * elapsed_time / evaluated_num
        print("Put: {} Eval: {} (level:{} num:{} time:{:.2f}s tpe:{:.2f}us)".format(
            self._pos2str(pos), evaluation, self.max_search_level, evaluated_num, elapsed_time, _time_per_eval_us))

    def _pos2str(self, pos):
        int2str_tbl = "-ABCDEFGH-"
        return int2str_tbl[pos[0]] + str(pos[1])

    def __str__(self):
        return "Computer ({})".format(self.name)
