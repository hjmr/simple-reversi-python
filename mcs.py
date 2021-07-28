import random

import stone
from board import Board
from action_selector import ActionSelector
from evaluator import StoneNumEvaluator

class MCS(ActionSelector):
    def __init__(self, my_stone, total_try = 1000):
        super().__init__(my_stone)
        self.eval_count = 0
        self.evaluator = StoneNumEvaluator()
        self.total_try = total_try

    def search_next_move(self, a_board):
        self.eval_count = 0
        _pos, _eval = self._mcs(a_board)
        return (_pos, _eval, self.eval_count)

    def _mcs(self, a_board):
        _pos_list = self._get_positions_to_put_stone(a_board, self.my_stone)
        _eval_list = {}
        _stage_rate = 40.0 / a_board.count_blank() # 最後までの手数に応じた比率（手数が長い（＝序盤）→ 読む数を少なく）
        _pos_num_rate = 1.0 / len(_pos_list)       # 打てる場所の数に応じた比率（読む数が一定になるように）
        _try_num = max(10, int(_stage_rate * _pos_num_rate * self.total_try))
        for _p in _pos_list:
            b = a_board.copy()
            b.put_stone_at(self.my_stone, _p)
            b.reverse_stones_from(_p)
            _ev = 0
            for _ in range(_try_num):
                _ev += self._eval(b.copy(), stone.reverse(self.my_stone))
            _eval_list[_p] = _ev / _try_num
        _eval_pos = max(_eval_list.items(), key=lambda x: x[1])        
        return _eval_pos
    
    def _eval(self, a_board, curr_stone):
        _pos_list = self._get_positions_to_put_stone(a_board, curr_stone)
        if 0 < len(_pos_list):
            _p = _pos_list[random.randint(0, len(_pos_list)-1)]
            a_board.put_stone_at(curr_stone, _p)
            a_board.reverse_stones_from(_p)
            _eval = self._eval(a_board, stone.reverse(curr_stone))
        elif self._can_put_stone(a_board, stone.reverse(curr_stone)):
             _eval = self._eval(a_board, stone.reverse(curr_stone))
        else:
            self.eval_count += 1
            _eval = 1 if 0 < self.evaluator.eval(a_board, self.my_stone) else -1
        return _eval

    def _can_put_stone(self, a_board, stone):
        for x in range(1, 9):
            for y in range(1, 9):
                if a_board.possible_to_put_stone_at(stone, (x, y)):
                    return True
        return False

    def _get_positions_to_put_stone(self, a_board, stone):
        _positions = []
        for x in range(1, 9):
            for y in range(1, 9):
                if a_board.possible_to_put_stone_at(stone, (x, y)):
                    _positions.append((x, y))
        return _positions
