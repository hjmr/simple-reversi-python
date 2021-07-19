import stone


cdef class Evaluator:
    cpdef int eval(self, object a_board, int curr_stone, int my_stone):
        pass

cdef class PutPosEvaluator(Evaluator):
    """evaluator for the first to middle periods."""

    cpdef int eval(self, object a_board, int curr_stone, int my_stone):
        cdef int _my_putpos = self._count_putpos(a_board, my_stone)
        cdef int _opp_putpos = self._count_putpos(a_board, stone.reverse(my_stone))
        cdef int _eval = _my_putpos - _opp_putpos
        return _eval

    cdef int _count_putpos(self, object a_board, int my_stone):
        cdef int _count = 0
        cdef int x, y
        for x in range(1, 9):
            for y in range(1, 9):
                if a_board.possible_to_put_stone_at(my_stone, (x, y)):
                    _count += 1
        return _count

cdef class PutPosCornerEvaluator(Evaluator):
    """evaluator for the first to middle periods."""

    cpdef int eval(self, object a_board, int curr_stone, int my_stone):
        cdef int _my_putpos = self._count_putpos(a_board, my_stone)
        cdef int _opp_putpos = self._count_putpos(a_board, stone.reverse(my_stone))
        cdef int _eval = _my_putpos - _opp_putpos + self._eval_corners(a_board, my_stone)
        return _eval

    cdef int _count_putpos(self, object a_board, int my_stone):
        cdef int _count = 0
        cdef int x, y
        for x in range(1, 9):
            for y in range(1, 9):
                if a_board.possible_to_put_stone_at(my_stone, (x, y)):
                    _count += 1
        return _count

    cdef int _eval_corners(self, object a_board, int my_stone):
        cdef int _opp_stone = stone.reverse(my_stone)
        cdef int _point = 0
        cdef ((int, int), (int, int), (int, int), (int, int)) _corners = ((1, 1), (1, 8), (8, 1), (8, 8))
        cdef int _corner_point = 10
        cdef (int, int) _c
        cdef int _s
        for _c in _corners:
            _s = a_board.get_at(_c)
            if _s == my_stone:
                _point += _corner_point
            elif _s == _opp_stone:
                _point -= _corner_point
        return _point

cdef class AverageEvaluator(Evaluator):
    """take averaged evaluation."""

    cdef object evaluator

    def __init__(self):
        super().__init__()
        self.evaluator = PutPosCornerEvaluator()

    cpdef int eval(self, object a_board, int curr_stone, int my_stone):
        cdef int _oppo_stone = stone.reverse(curr_stone)
        cdef list _pos_list = self._get_positions_to_put_stone(a_board, _oppo_stone)
        cdef int _eval = 0
        cdef (int, int) _p

        if 0 < len(_pos_list):
            _eval = 0
            for _p in _pos_list:
                b = a_board.copy()
                b.put_stone_at(_oppo_stone, _p)
                b.reverse_stones_from(_p)
                _eval += self.evaluator.eval(a_board, curr_stone, my_stone) * 10
            _eval /= len(_pos_list)
        else:
            _eval = self.evaluator.eval(a_board, curr_stone, my_stone) * 10
        return _eval
        
    cdef list _get_positions_to_put_stone(self, object a_board, int curr_stone):
        cdef list _positions = []
        cdef int x, y
        for x in range(1, 9):
            for y in range(1, 9):
                if a_board.possible_to_put_stone_at(curr_stone, (x, y)):
                    _positions.append((x, y))
        return _positions


cdef class StoneNumEvaluator(Evaluator):
    """evaluator for the last period which evaluate the number of stones"""

    cpdef int eval(self, object a_board, int curr_stone, int my_stone):
        cdef int _my_count = a_board.count_stones(my_stone)
        cdef int _opp_count = a_board.count_stones(stone.reverse(my_stone))
        cdef int _eval = _my_count - _opp_count
        return _eval
