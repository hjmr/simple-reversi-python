from board import Stone
from game import Game


class Evaluator:
    def eval(self, _board, _stone):
        pass


class PutPosEvaluator(Evaluator):
    def eval(self, _board, _stone):
        _my_putpos = self._count_putpos(_board, _stone)
        _opp_putpos = self._count_putpos(_board, Stone.reverse(_stone))
        _eval = _my_putpos - _opp_putpos
        return _eval

    def _count_putpos(self, _board, _stone):
        _count = 0
        for x in range(1, 9):
            for y in range(1, 9):
                if Game.possible_to_put_stone_at(_board, _stone, (x, y)):
                    _count += 1
        return _count


class StoneNumEvaluator(Evaluator):
    def eval(self, _board, _stone):
        _my_count = _board.count_stones(_stone)
        _opp_count = _board.count_stones(Stone.reverse(_stone))
        _eval = _my_count - _opp_count
        return _eval
