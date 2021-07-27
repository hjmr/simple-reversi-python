import stone
from board import Board
from action_selector import ActionSelector

SMALL_NUMBER = -1000
LARGE_NUMBER = 1000


class Minimax(ActionSelector):
    def __init__(self, my_stone, evaluator, max_search_level = 5):
        super().__init__(my_stone)
        self.evaluator = evaluator
        self.max_search_level = max_search_level
        self.eval_count = 0

    def search_next_move(self, a_board):
        self.eval_count = 0
        _pos, _eval = self._minimax(a_board, self.my_stone, 0, SMALL_NUMBER, LARGE_NUMBER)
        return (_pos, _eval, self.eval_count)

    def _minimax(self, a_board, curr_stone, curr_level, alpha, beta):
        curr_level += 1
        _pos_list = self._get_positions_to_put_stone(a_board, curr_stone)
        if 0 < len(_pos_list):
            _eval_list = {}
            _alpha = SMALL_NUMBER
            _beta = LARGE_NUMBER
            for _p in _pos_list:
                b = a_board.copy()
                b.put_stone_at(curr_stone, _p)
                b.reverse_stones_from(_p)
                if self.max_search_level <= curr_level:
                    _eval_list[_p] = self._eval(b)
                else:
                    _eval_list[_p] = self._minimax(b, stone.reverse(curr_stone), curr_level, _alpha, _beta)[1]

                # alpha-beta branch cut
                if (curr_stone == self.my_stone and beta < _eval_list[_p]) or \
                   (curr_stone != self.my_stone and _eval_list[_p] < alpha):
                    break
                # update alpha-beta
                _alpha = _eval_list[_p] if _alpha < _eval_list[_p] else _alpha
                _beta = _eval_list[_p] if _eval_list[_p] < _beta else _beta

            if curr_stone == self.my_stone:
                _eval_pos = max(_eval_list.items(), key=lambda x: x[1])
            else:
                _eval_pos = min(_eval_list.items(), key=lambda x: x[1])
        else:
            if self.max_search_level <= curr_level:
                _eval_pos = (None, self._eval(a_board))
            else:
                _eval_pos = (None, self._minimax(a_board, stone.reverse(curr_stone), curr_level, alpha, beta)[1])
        return _eval_pos

    def _eval(self, a_board):
        self.eval_count += 1
        _eval = self.evaluator.eval(a_board, self.my_stone)
        return _eval

    def _get_positions_to_put_stone(self, a_board, stone):
        _positions = []
        for x in range(1, 9):
            for y in range(1, 9):
                if a_board.possible_to_put_stone_at(stone, (x, y)):
                    _positions.append((x, y))
        return _positions
