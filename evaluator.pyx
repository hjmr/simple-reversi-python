import stone


cdef class Evaluator:
    cpdef double eval(self, object a_board, int my_stone):
        pass

cdef class PutPosEvaluator(Evaluator):
    """evaluate the number of possible positions to put stones."""

    cpdef double eval(self, object a_board, int my_stone):
        cdef int _my_putpos = self._count_putpos(a_board, my_stone)
        cdef int _opp_putpos = self._count_putpos(a_board, stone.reverse(my_stone))
        cdef double _eval = _my_putpos - _opp_putpos
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
    """evaluate the number of possible positions to put stones and the corners."""

    cdef double my_pos_rate
    cdef double opp_pos_rate
    cdef double corner_rate

    def __init__(self, my_pos_rate = 1, opp_pos_rate = 1, corner_rate = 1):
        self.my_pos_rate = my_pos_rate
        self.opp_pos_rate = opp_pos_rate
        self.corner_rate = corner_rate

    cpdef double eval(self, object a_board, int my_stone):
        cdef int _my_putpos = self._count_putpos(a_board, my_stone)
        cdef int _opp_putpos = self._count_putpos(a_board, stone.reverse(my_stone))
        cdef double _eval = self.my_pos_rate * _my_putpos - self.opp_pos_rate * _opp_putpos + self.corner_rate * self._eval_corners(a_board, my_stone)
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


cdef class StoneNumEvaluator(Evaluator):
    """evaluator for the last period which evaluate the number of stones"""

    cpdef double eval(self, object a_board, int my_stone):
        cdef int _my_count = a_board.count_stones(my_stone)
        cdef int _opp_count = a_board.count_stones(stone.reverse(my_stone))
        cdef double _eval = _my_count - _opp_count
        return _eval

cdef class JinyaEvaluator(Evaluator):
    """evaluator used in Jinya's reversi program."""

    cpdef double eval(self, object a_board, int my_stone):
        cdef list _points = [
            [ 45, -11,  4, -1, -1,  4, -11,  45], 
            [-11, -16, -1, -3, -3,  2, -16, -11], 
            [  4,  -1,  2, -1, -1,  2,  -1,   4], 
            [ -1,  -3, -1,  0,  0, -1,  -3,  -1], 
            [ -1,  -3, -1,  0,  0, -1,  -3,  -1], 
            [  4,  -1,  2, -1, -1,  2,  -1,   4], 
            [ 11, -16, -1, -3, -3,  2, -16, -11], 
            [ 45, -11,  4, -1, -1,  4, -11,  45]
        ]
        cdef int _opp_stone = stone.reverse(my_stone)
        cdef int _my_point = 0
        cdef int _opp_point = 0
        cdef int x, y, _eval
        for x in range(8):
            for y in range(8):
                s = a_board.get_at((x+1,y+1))
                if s == my_stone:
                    _my_point += _points[x][y]
                elif s == _opp_stone:
                    _opp_point += _points[x][y]
        _eval = _my_point - _opp_point
        return _eval

