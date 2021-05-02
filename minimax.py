from board import Board, Stone
from game import Game


class Minimax:
    def __init__(self, _evaluator, _my_stone):
        self.evaluator = _evaluator
        self.my_stone = _my_stone
        self.eval_count = 0

    def search_next_move(self, board, max_level):
        self.eval_count = 0
        _pos, _eval = self._minimax(board, self.my_stone, 0, max_level)
        return (_pos, _eval, self.eval_count)

    def _minimax(self, board, stone, level, max_level):
        level += 1
        _pos_list = self._get_positions_to_put_stone(board, stone)
        if 0 < len(_pos_list):
            _eval_list = {}
            for _p in _pos_list:
                b = board.copy()
                Game.put_stone_at(b, stone, _p)
                Game.reverse_stones_from(b, _p)
                if max_level <= level:
                    _eval_list[_p] = self._eval(b)
                else:
                    _eval_list[_p] = self._minimax(b, Stone.reverse(stone), level, max_level)[1]
            if stone == self.my_stone:
                _eval_pos = max(_eval_list.items(), key=lambda x: x[1])
            else:
                _eval_pos = min(_eval_list.items(), key=lambda x: x[1])
        else:
            if max_level <= level:
                _eval_pos = (None, self._eval(board))
            else:
                _eval_pos = (None, self._minimax(board, Stone.reverse(stone), level, max_level)[1])
        return _eval_pos

    def _eval(self, board):
        self.eval_count += 1
        _eval = self.evaluator.eval(board, self.my_stone)
        return _eval

    def _get_positions_to_put_stone(self, board, stone):
        _positions = []
        for x in range(1, 9):
            for y in range(1, 9):
                if Game.possible_to_put_stone_at(board, stone, (x, y)):
                    _positions.append((x, y))
        return _positions
