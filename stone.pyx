BLACK = 1
WHITE = 2


cpdef int reverse(int _stone):
    cdef int _rev_stone = BLACK if _stone == WHITE else WHITE
    return _rev_stone
