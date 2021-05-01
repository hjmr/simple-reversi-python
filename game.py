from board import Stone, Board

X = 0
Y = 1
directions = ((-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1))


class Game:
    @classmethod
    def possible_to_put_stone(cls, _board, _stone):
        _possible = False
        for x in range(1, 9):
            for y in range(1, 9):
                if cls.possible_to_put_stone_at(_board, _stone, (x, y)):
                    _possible = True
                    break
        return _possible

    @classmethod
    def possible_to_put_stone_at(cls, _board, _stone, _pos):
        _possible = False
        if _board.get_at(_pos) == Board.BLANK:
            for _dir in directions:
                if 0 < cls._count_reversible_stones_in_direction(_board, _stone, _pos, _dir):
                    _possible = True
                    break
        return _possible

    @classmethod
    def count_reversible_stones(cls, _board, _turn, _pos):
        _reverse_num = 0
        for _dir in directions:
            _reverse_num += cls._count_reversible_stones_in_direction(_board, _turn, _pos, _dir)
        return _reverse_num

    @classmethod
    def reverse_stones_from(cls, _board, _pos):
        _turn = _board.get_at(_pos)
        if _turn in (Stone.BLACK, Stone.WHITE):
            for _dir in directions:
                _last_pos = cls._find_last_pos_in_direction(_board, _turn, _pos, _dir)
                if _last_pos is not None:
                    cls._reverse_stones_in_direction(_board, _turn, _last_pos, (-_dir[X], -_dir[Y]))

    @classmethod
    def put_stone_at(cls, _board, _turn, _pos):
        _success = False
        if _board.get_at(_pos) == Board.BLANK:
            _board.set_stone_at(_turn, _pos)
            _success = True
        return _success

    @classmethod
    def _move(cls, _pos, _dir):
        return (_pos[X] + _dir[X], _pos[Y] + _dir[Y])

    @classmethod
    def _count_reversible_stones_in_direction(cls, _board, _turn, _pos, _dir):
        _opponent_turn = Stone.reverse(_turn)
        _reverse_num = 0
        _cur_pos = cls._move(_pos, _dir)
        while _board.get_at(_cur_pos) == _opponent_turn:
            _cur_pos = cls._move(_cur_pos, _dir)
            _reverse_num += 1
        if _board.get_at(_cur_pos) != _turn:
            _reverse_num = 0
        return _reverse_num

    @classmethod
    def _find_last_pos_in_direction(cls, _board, _turn, _pos, _dir):
        _opponent_turn = Stone.reverse(_turn)
        _cur_pos = cls._move(_pos, _dir)
        while _board.get_at(_cur_pos) == _opponent_turn:
            _cur_pos = cls._move(_cur_pos, _dir)
        if _board.get_at(_cur_pos) != _turn:
            _cur_pos = None
        return _cur_pos

    @classmethod
    def _reverse_stones_in_direction(cls, _board, _turn, _pos, _dir):
        _opponent_turn = Stone.reverse(_turn)
        _cur_pos = cls._move(_pos, _dir)
        while _board.get_at(_cur_pos) == _opponent_turn:
            _board.set_stone_at(_turn, _cur_pos)
            _cur_pos = cls._move(_cur_pos, _dir)


if __name__ == "__main__":
    b = Board()
    Game.put_stone_at(b, Stone.BLACK, (5, 3))
    Game.reverse_stones_from(b, (5, 3))
    print(b)
