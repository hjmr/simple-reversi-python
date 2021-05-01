from board import Board, Stone
from game import Game


class Evaluator:
    def __init__(self):
        pass

    def eval(self, _board, _my_stone, _max_level):
        self.my_stone = _my_stone
        self.max_level = _max_level
        _eval = self._minimax(_board, _my_stone, 0)

    def _minimax(self, _board, _stone, _level):
        _level += 1
        _pos_list = self._count_positions_to_put(_board, _stone)
        if 0 < len(_pos_list):
            _vals = {}
            for _p in _pos_list:
                b = _board.copy()
                Game.put_stone_at(b, _stone, _p)
                Game.reverse_stones_from(b, _p)
                if self.max_level <= _level:
                    _vals[_p] = self._eval_board(b)
                else:
                    _vals[_p] = self._minimax(b, Stone.reverse(_stone), _level)[1]
            if _stone == self.my_stone:
                _eval = max(_vals.items(), key=lambda x: x[1])
            else:
                _eval = min(_vals.items(), key=lambda x: x[1])
        else:
            _eval = (None, self._eval_board(_board))
        return _eval

    def _eval_board(self, _board):
        _eval = _board.count_stones(self.my_stone) - _board.count_stones(Stone.reverse(self.my_stone))
        return _eval

    def _count_positions_to_put(self, _board, _stone):
        _positions = []
        for x in range(1, 9):
            for y in range(1, 9):
                if Game.possible_to_put_stone_at(_board, _stone, (x, y)):
                    _positions.append((x, y))
        return _positions
