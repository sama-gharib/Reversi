from typing import List, Tuple
# from collections import OrderedDict

from model.move import Move

class Board:
    """ Reversi (Othello) board class """

    BOARD_SIZE = 8

    EMPTY = -1
    BLACK = 0
    WHITE = 1

    DIRECTIONS = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),          (0, 1),
        (1, -1), (1, 0),  (1, 1)
    ]

    def __init__(self):
        """
        Initialize the board
        
        Parameters
        ----------
        board_size: int
            Size of the board (default is 8x8)
        """
        self._board_size = Board.BOARD_SIZE
        self._board = [[self.EMPTY for _ in range(self._board_size)] for _ in range(self._board_size)]
        self._current_player = self.BLACK
        self._init_board()

    def _init_board(self):
        """ Initialize the starting position of the board """
        mid = self._board_size // 2
        self._board[mid - 1][mid - 1] = self.WHITE
        self._board[mid][mid] = self.WHITE
        self._board[mid - 1][mid] = self.BLACK
        self._board[mid][mid - 1] = self.BLACK
        self.history = []
        
    def get_at(self, line: int, column: int) -> int:
        return self._board[line][column]

    def clear_board(self):
        """ Clear the board """
        self._board = [[self.EMPTY for _ in range(self._board_size)] for _ in range(self._board_size)]
        self._init_board()
        self._current_player = self.BLACK

    def in_bounds(self, x: int, y: int) -> bool:
        """ Check if the coordinates are within the board limits """
        return 0 <= x < self._board_size and 0 <= y < self._board_size

    def is_valid_move(self, x: int, y: int) -> bool:
        """ Check if a move is valid """
        if not self.in_bounds(x, y) or self._board[x][y] != self.EMPTY:
            return False

        for dx, dy in self.DIRECTIONS:
            nx, ny = x + dx, y + dy
            has_opponent_between = False

            while self.in_bounds(nx, ny) and self._board[nx][ny] == 1 - self._current_player:
                nx += dx
                ny += dy
                has_opponent_between = True

            if has_opponent_between and self.in_bounds(nx, ny) and self._board[nx][ny] == self._current_player:
                return True

        return False

    def get_valid_moves(self) -> List[Tuple[int, int]]:
        """ Get all valid moves for the current player """
        return [(x, y) for x in range(self._board_size) for y in range(self._board_size) if self.is_valid_move(x, y)]

    def make_move(self, x: int, y: int) -> bool:
        """ Play a move and flip the pieces. Returns True if successful, otherwise False """
        if not self.is_valid_move(x, y):
            raise ValueError(f'Move on line {x} and column {y} is illegal.')

        self.history.append(Move (
            team = "black" if self._current_player == Board.BLACK else "white",
            line = x,
            column = y
        ))

        self._board[x][y] = self._current_player

        for dx, dy in self.DIRECTIONS:
            flips = []
            nx, ny = x + dx, y + dy

            while self.in_bounds(nx, ny) and self._board[nx][ny] == 1 - self._current_player:
                flips.append((nx, ny))
                nx += dx
                ny += dy

            if flips and self.in_bounds(nx, ny) and self._board[nx][ny] == self._current_player:
                for fx, fy in flips:
                    self._board[fx][fy] = self._current_player

        self._current_player = 1 - self._current_player
        return True
    
    def flipped_pieces(self, x: int, y: int) -> int:
        """ Count the number of pieces flipped for a move """
        if not self.is_valid_move(x, y):
            raise ValueError(f'Move on line {x} and column {y} is illegal.')

        count_flips = 0
        for dx, dy in self.DIRECTIONS:
            flips = []
            nx, ny = x + dx, y + dy
            has_opponent_between = False

            while self.in_bounds(nx, ny) and self._board[nx][ny] == 1 - self._current_player:
                flips.append((nx, ny))
                nx += dx
                ny += dy
                has_opponent_between = True

            if has_opponent_between and self.in_bounds(nx, ny) and self._board[nx][ny] == self._current_player:
                count_flips += len(flips)
        
        return count_flips

    def get_score(self, team) -> int:
        return sum(row.count(team) for row in self.board)    

    def is_game_over(self) -> bool:
        """ Check if the game is over (no valid moves for both players) """
        if self.get_valid_moves():
            return False

        self._current_player = 1 - self._current_player
        if self.get_valid_moves():
            self._current_player = 1 - self._current_player  # Switch back to the original player
            return False

        return True

    def get_winner(self) -> int:
        """ Determine the winner (BLACK/WHITE), returns -1 in case of a tie """
        black_count = sum(row.count(self.BLACK) for row in self._board)
        white_count = sum(row.count(self.WHITE) for row in self._board)

        if black_count > white_count:
            return self.BLACK
        elif white_count > black_count:
            return self.WHITE
        else:
            return self.EMPTY

    def display_board(self):
        """ Display the current state of the board """
        symbols = {self.EMPTY: '.', self.BLACK: 'B', self.WHITE: 'W'}
        print("  " + " ".join(str(i) for i in range(self._board_size)))
        for i in range(self._board_size):
            row = " ".join(symbols[self._board[i][j]] for j in range(self._board_size))
            print(f"{i} {row}")

    @property
    def board_size(self) -> int:
        """ Getter for the board size """
        return self._board_size

    @property
    def current_player(self) -> int:
        """ Getter for the current player """
        return self._current_player

    @property
    def board(self) -> List[List[int]]:
        """ Getter for the board """
        return self._board

    
