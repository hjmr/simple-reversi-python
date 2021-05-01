from board import Board, Stone
from game import Game


class Minimax:
    def __init__(self, _evaluator, _my_stone):
        self.evaluator = _evaluator
        self.my_stone = _my_stone
        self.max_level = 1
        self.eval_count = 0

    def find_next_move(self, _board, _max_level):
        self.eval_count = 0
        self.max_level = _max_level
        _pos, _eval = self._minimax(_board, self.my_stone, 0)
        return (_pos, _eval, self.eval_count)

    def _minimax(self, _board, _stone, _level):
        _level += 1
        _pos_list = self._get_positions_to_put_stone(_board, _stone)
        if 0 < len(_pos_list):
            _eval_list = {}
            for _p in _pos_list:
                b = _board.copy()
                Game.put_stone_at(b, _stone, _p)
                Game.reverse_stones_from(b, _p)
                if self.max_level <= _level:
                    _eval_list[_p] = self._eval(b)
                else:
                    _eval_list[_p] = self._minimax(b, Stone.reverse(_stone), _level)[1]
            if _stone == self.my_stone:
                _eval_pos = max(_eval_list.items(), key=lambda x: x[1])
            else:
                _eval_pos = min(_eval_list.items(), key=lambda x: x[1])
        else:
            _eval_pos = (None, self._eval(_board))
        return _eval_pos

    def _eval(self, _board):
        self.eval_count += 1
        _eval = self.evaluator.eval(_board, self.my_stone)
        return _eval

    def _get_positions_to_put_stone(self, _board, _stone):
        _positions = []
        for x in range(1, 9):
            for y in range(1, 9):
                if Game.possible_to_put_stone_at(_board, _stone, (x, y)):
                    _positions.append((x, y))
        return _positions
