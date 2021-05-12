import stone
import game
from board import Board

SMALL_NUMBER = -1000
LARGE_NUMBER = 1000


class Minimax:
    def __init__(self, _evaluator, _my_stone):
        self.evaluator = _evaluator
        self.my_stone = _my_stone
        self.eval_count = 0

    def search_next_move(self, a_board, max_level):
        self.eval_count = 0
        _pos, _eval = self._minimax(a_board, self.my_stone, 0, max_level, SMALL_NUMBER, LARGE_NUMBER)
        return (_pos, _eval, self.eval_count)

    def _minimax(self, a_board, a_stone, level, max_level, alpha, beta):
        level += 1
        _pos_list = self._get_positions_to_put_stone(a_board, a_stone)
        if 0 < len(_pos_list):
            _eval_list = {}
            _alpha = SMALL_NUMBER
            _beta = LARGE_NUMBER
            for _p in _pos_list:
                b = a_board.copy()
                game.put_stone_at(b, a_stone, _p)
                game.reverse_stones_from(b, _p)
                if max_level <= level:
                    _eval_list[_p] = self._eval(b)
                else:
                    _eval_list[_p] = self._minimax(b, stone.reverse(a_stone), level, max_level, _alpha, _beta)[1]

                # alpha-beta branch cut
                if (a_stone == self.my_stone and beta < _eval_list[_p]) or \
                   (a_stone != self.my_stone and _eval_list[_p] < alpha):
                    break
                # update alpha-beta
                _alpha = _eval_list[_p] if _alpha < _eval_list[_p] else _alpha
                _beta = _eval_list[_p] if _eval_list[_p] < _beta else _beta

            if a_stone == self.my_stone:
                _eval_pos = max(_eval_list.items(), key=lambda x: x[1])
            else:
                _eval_pos = min(_eval_list.items(), key=lambda x: x[1])
        else:
            if max_level <= level:
                _eval_pos = (None, self._eval(a_board))
            else:
                _eval_pos = (None, self._minimax(a_board, stone.reverse(a_stone), level, max_level, alpha, beta)[1])
        return _eval_pos

    def _eval(self, a_board):
        self.eval_count += 1
        _eval = self.evaluator.eval(a_board, self.my_stone)
        return _eval

    def _get_positions_to_put_stone(self, a_board, a_stone):
        _positions = []
        for x in range(1, 9):
            for y in range(1, 9):
                if game.possible_to_put_stone_at(a_board, a_stone, (x, y)):
                    _positions.append((x, y))
        return _positions
