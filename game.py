import stone
from board import Board

X = 0
Y = 1
directions = ((-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1))


def possible_to_put_stone(a_board, a_stone):
    _possible = False
    for x in range(1, 9):
        for y in range(1, 9):
            if possible_to_put_stone_at(a_board, a_stone, (x, y)):
                _possible = True
                break
    return _possible


def possible_to_put_stone_at(a_board, a_stone, pos):
    _possible = False
    if a_board.is_blank_at(pos):
        for _dir in directions:
            if 0 < _count_reversible_stones_in_direction(a_board, a_stone, pos, _dir):
                _possible = True
                break
    return _possible


def count_reversible_stones(a_board, a_stone, pos):
    _reverse_num = 0
    for _dir in directions:
        _reverse_num += _count_reversible_stones_in_direction(a_board, a_stone, pos, _dir)
    return _reverse_num


def reverse_stones_from(a_board, pos):
    _stone = a_board.get_at(pos)
    if _stone in (stone.BLACK, stone.WHITE):
        for _dir in directions:
            _last_pos = _find_last_pos_in_direction(a_board, _stone, pos, _dir)
            if _last_pos is not None:
                _reverse_stones_in_direction(a_board, _stone, _last_pos, (-_dir[X], -_dir[Y]))


def put_stone_at(a_board, a_stone, pos):
    _success = False
    if a_board.is_blank_at(pos):
        a_board.set_stone_at(a_stone, pos)
        _success = True
    return _success


def _move(pos, dire):
    return (pos[X] + dire[X], pos[Y] + dire[Y])


def _count_reversible_stones_in_direction(a_board, a_stone, pos, dire):
    _opponent_turn = stone.reverse(a_stone)
    _reverse_num = 0
    _cur_pos = _move(pos, dire)
    while a_board.get_at(_cur_pos) == _opponent_turn:
        _cur_pos = _move(_cur_pos, dire)
        _reverse_num += 1
    if a_board.get_at(_cur_pos) != a_stone:
        _reverse_num = 0
    return _reverse_num


def _find_last_pos_in_direction(a_board, a_stone, pos, dire):
    _opponent_turn = stone.reverse(a_stone)
    _cur_pos = _move(pos, dire)
    while a_board.get_at(_cur_pos) == _opponent_turn:
        _cur_pos = _move(_cur_pos, dire)
    if a_board.get_at(_cur_pos) != a_stone:
        _cur_pos = None
    return _cur_pos


def _reverse_stones_in_direction(a_board, a_stone, pos, dire):
    _opponent_turn = stone.reverse(a_stone)
    _cur_pos = _move(pos, dire)
    while a_board.get_at(_cur_pos) == _opponent_turn:
        a_board.set_stone_at(a_stone, _cur_pos)
        _cur_pos = _move(_cur_pos, dire)


if __name__ == "__main__":
    b = Board()
    put_stone_at(b, stone.BLACK, (5, 3))
    reverse_stones_from(b, (5, 3))
    print(b)
