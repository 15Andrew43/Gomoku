import numpy as np
from typing import Optional, List
from itertools import product


class EndGame(Exception):
    def __init__(self, winner, board):
        self.winner = winner
        self.board = board

def is_sub_arr(a1, a2):
    a1 = list(a1)
    a2 = list(a2)
    a1 = list(map(lambda x: str(x)[0], a1))
    a2 = list(map(lambda x: str(x)[0], a2))
    return ''.join(a2) in ''.join(a1)

class BoardState:
    def __init__(self, board: np.ndarray, current_player: int = 1):
        self.board: np.ndarray = board
        self.current_player: int = current_player

    def inverted(self) -> 'BoardState':
        return BoardState(board=self.board[::-1, ::-1] * -1, current_player=self.current_player * -1)

    def copy(self) -> 'BoardState':
        return BoardState(self.board.copy(), self.current_player)

    def do_move(self, to_x, to_y) -> Optional['BoardState']:
        """
        :return: new BoardState or None for invalid move
        """
        if (not (0 <= to_x < 15 and 0 <= to_y < 15)) or self.board[to_y, to_x] != 0:
               return None

        result = self.copy()
        result.board[to_y, to_x] = result.current_player
        # result.current_player *= (-1)

        # winner = result.get_winner
        winner = result.get_winner(to_y, to_x)
        result.current_player *= (-1)
        if winner == 1:
            print('black player won!!!')
        elif winner == -1:
            print('white player won!!!')
        else:
            # print('No one won!!!')
            pass
        if winner:
            raise EndGame(winner, result)

        return result

    def get_winner(self, to_y, to_x):
        a = (to_y - 4, to_x - 4)
        b = (to_y - 4, to_x + 4)
        c = (to_y + 4, to_x + 4)
        d = (to_y + 4, to_x - 4)
        for i in range(5):
            if (to_y - i == 0 or to_x - i == 0) and (to_y - i - 1 < 0 or to_x - i - 1 < 0):
                a = (to_y - i, to_x - i)
                break
        for i in range(5):
            if (to_y - i == 0 or to_x + i == 14) and (to_y - i - 1 < 0 or to_x + i + 1 > 14):
                b = (to_y - i, to_x + i)
                break
        for i in range(5):
            if (to_y + i == 14 or to_x + i == 14) and (to_y + i + 1 > 14 or to_x + i + 1 > 14):
                c = (to_y + i, to_x + i)
                break
        for i in range(5):
            if (to_y + i == 14 or to_x - i == 0) and (to_y + i + 1 > 14 or to_x - i - 1 < 0):
                d = (to_y + i, to_x - i)
                break
        # print("------------------------------------------------")
        # print(f'a = {a}, b = {b}, c = {c}, d = {d}')
        oy = []
        for y in range(min(a[0], b[0]), max(c[0], d[0]) + 1):
            oy.append(self.board[y, to_x])
        if is_sub_arr(oy, [self.current_player] * 5):
            # print('wow---------------------------------------')
            return self.current_player
        ox = []
        for x in range(min(a[1], d[1]), max(b[1], c[1]) + 1):
            ox.append(self.board[to_y, x])
        if is_sub_arr(ox, [self.current_player] * 5):
            return self.current_player
        ac = []
        for y, x in zip(range(a[0], c[0] + 1), range(a[1], c[1] + 1)):
            ac.append(self.board[y, x])
        if is_sub_arr(ac, [self.current_player] * 5):
            return self.current_player
        bd = []
        for y, x in zip(range(b[0], d[0] + 1), range(b[1], d[1] - 1, -1)):
            bd.append(self.board[y, x])
        if is_sub_arr(bd, [self.current_player] * 5):
            return self.current_player

        return None



    def get_possible_moves(self, y, x) -> List['BoardState']:
        """
        :param y:
        :param x:
        :return: ( должен бить?, массив возможных ходов из (у, х) )
        """
        moves = []
        for y, x in product(range(14), range(14)):
            if self.board[y, x] == 0:    
                moves.append((y, x))

    # @property
    # def get_winner(self):
    #     '''
    #     :return: winner or None
    #     '''
    #     for row in self.board:
    #         if is_sub_arr(row, [1] * 5):
    #             return 1
    #         if is_sub_arr(row, [-1] * 5):
    #             return -1
    #     for colomn in [self.board[:, i] for i in range(15)]:
    #         if is_sub_arr(colomn, [1] * 5):
    #             return 1
    #         if is_sub_arr(colomn, [-1] * 5):
    #             return -1
    #     for y, x in product(range(15), range(15)):
    #         current = self.board[y, x]
    #         if current == 0:
    #             continue
    #         for i in range(1, 5):
    #             if 0 <= y+i < 15 and 0 <= x+i < 15 and self.board[y + i, x + i] != current:
    #                 break
    #         else:
    #             return 1 if current == 1 else -1
    #         for i in range(1, 5):
    #             if 0 <= y+i < 15 and 0 <= x-i < 15 and self.board[y + i, x - i] != current:
    #                 break
    #         else:
    #             return 1 if current == 1 else -1
    #     return None


    @staticmethod
    def initial_state() -> 'BoardState':
        board = np.zeros(shape=(15, 15), dtype=np.int8)

        board[7, 7] = -1  # шашка первого игрока
        # board[4, 4] = -1
        # board[5, 5] = -1
        # board[6, 6] = -1
        # board[7, 7] = -1
        # board[7, 7] = -1
        return BoardState(board, 1)
