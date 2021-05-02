from board import Stone, Board

X = 0
Y = 1
directions = ((-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1))


class Game:
    @classmethod
    def possible_to_put_stone(cls, board, stone):
        _possible = False
        for x in range(1, 9):
            for y in range(1, 9):
                if cls.possible_to_put_stone_at(board, stone, (x, y)):
                    _possible = True
                    break
        return _possible

    @classmethod
    def possible_to_put_stone_at(cls, board, stone, pos):
        _possible = False
        if board.get_at(pos) == Board.BLANK:
            for _dir in directions:
                if 0 < cls._count_reversible_stones_in_direction(board, stone, pos, _dir):
                    _possible = True
                    break
        return _possible

    @classmethod
    def count_reversible_stones(cls, board, turn, pos):
        _reverse_num = 0
        for _dir in directions:
            _reverse_num += cls._count_reversible_stones_in_direction(board, turn, pos, _dir)
        return _reverse_num

    @classmethod
    def reverse_stones_from(cls, board, pos):
        _stone = board.get_at(pos)
        if _stone in (Stone.BLACK, Stone.WHITE):
            for _dir in directions:
                _last_pos = cls._find_last_pos_in_direction(board, _stone, pos, _dir)
                if _last_pos is not None:
                    cls._reverse_stones_in_direction(board, _stone, _last_pos, (-_dir[X], -_dir[Y]))

    @classmethod
    def put_stone_at(cls, board, stone, pos):
        _success = False
        if board.get_at(pos) == Board.BLANK:
            board.set_stone_at(stone, pos)
            _success = True
        return _success

    @classmethod
    def _move(cls, pos, dire):
        return (pos[X] + dire[X], pos[Y] + dire[Y])

    @classmethod
    def _count_reversible_stones_in_direction(cls, board, stone, pos, dire):
        _opponent_turn = Stone.reverse(stone)
        _reverse_num = 0
        _cur_pos = cls._move(pos, dire)
        while board.get_at(_cur_pos) == _opponent_turn:
            _cur_pos = cls._move(_cur_pos, dire)
            _reverse_num += 1
        if board.get_at(_cur_pos) != stone:
            _reverse_num = 0
        return _reverse_num

    @classmethod
    def _find_last_pos_in_direction(cls, board, stone, pos, dire):
        _opponent_turn = Stone.reverse(stone)
        _cur_pos = cls._move(pos, dire)
        while board.get_at(_cur_pos) == _opponent_turn:
            _cur_pos = cls._move(_cur_pos, dire)
        if board.get_at(_cur_pos) != stone:
            _cur_pos = None
        return _cur_pos

    @classmethod
    def _reverse_stones_in_direction(cls, board, stone, pos, dire):
        _opponent_turn = Stone.reverse(stone)
        _cur_pos = cls._move(pos, dire)
        while board.get_at(_cur_pos) == _opponent_turn:
            board.set_stone_at(stone, _cur_pos)
            _cur_pos = cls._move(_cur_pos, dire)


if __name__ == "__main__":
    b = Board()
    Game.put_stone_at(b, Stone.BLACK, (5, 3))
    Game.reverse_stones_from(b, (5, 3))
    print(b)
