import stone


class Evaluator:
    def eval(self, a_board, a_stone):
        pass


class MiddleEvaluator(Evaluator):
    """evaluator for the first to middle periods."""

    def eval(self, a_board, my_stone):
        _my_putpos = self._count_putpos(a_board, my_stone)
        _opp_putpos = self._count_putpos(a_board, stone.reverse(my_stone))
        _eval = _my_putpos - _opp_putpos + self._eval_corners(a_board, my_stone)
        return _eval

    def _count_putpos(self, a_board, my_stone):
        _count = 0
        for x in range(1, 9):
            for y in range(1, 9):
                if a_board.possible_to_put_stone_at(my_stone, (x, y)):
                    _count += 1
        return _count

    def _eval_corners(self, a_board, my_stone):
        _opp_stone = stone.reverse(my_stone)
        _point = 0
        _corners = ((1, 1), (1, 8), (8, 1), (8, 8))
        _corner_point = 10
        for _c in _corners:
            _s = a_board.get_at(_c)
            if _s == my_stone:
                _point += _corner_point
            elif _s == _opp_stone:
                _point -= _corner_point
        return _point


class FinalEvaluator(Evaluator):
    """evaluator for the last period which evaluate the number of stones"""

    def eval(self, a_board, my_stone):
        _my_count = a_board.count_stones(my_stone)
        _opp_count = a_board.count_stones(stone.reverse(my_stone))
        _eval = _my_count - _opp_count
        return _eval
