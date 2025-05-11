from model.move import Move
from model.player import Player
from model.board import Board

from random import uniform, choice
from time import sleep
from copy import deepcopy

class Minimax(Player):

    def _think(self, board) -> Move:
        # sleep(uniform(0.5, 1)) # Simulate thinking time
        # Dynamically adapt depth: deeper in early game, shallower in late game for speed
        total_pieces = self.count_total_pieces(board)
        if total_pieces < 20:
            depth = 3
        elif total_pieces < 50:
            depth = 4
        else:
            depth = 6  # Endgame: deeper search is possible (less moves)
            
        c = self.best_move(board, depth)
        if c is not None:
            return Move(c[1], c[0])
        else:
            valid_moves = board.get_valid_moves()
            return Move(valid_moves[0][1], valid_moves[0][0])

    def best_move(self, board, depth) -> Move:
        """Find the best move using minimax algorithm with alpha-beta pruning."""
        best_score = float('-inf')
        best_moves = []
        valid_moves = board.get_valid_moves()
        if not valid_moves:
            return None

        # print(f"\n[INFO] All move and score (depth={depth}):")
        for move in valid_moves:
            board_copy = deepcopy(board)
            board_copy.make_move(move[0], move[1])
            score = self.minimax(board_copy, depth - 1, float('-inf'), float('inf'), False)
            # print(f"  position: (x={move[1]}, y={move[0]})  score={score:.2f}")
            if score > best_score:
                best_score = score
                best_moves = [move]
            elif score == best_score:
                best_moves.append(move)

        # Randomize among best moves to avoid deterministic play
        return choice(best_moves)

    def minimax(self, board, depth: int, alpha: float, beta: float, maximizing_player: bool, indent=0):
        """Minimax algorithm with alpha-beta pruning."""
        valid_moves = board.get_valid_moves()
        if depth == 0 or not valid_moves:
            return self.evaluate_board2(board)

        if maximizing_player:
            value = float('-inf')
            for move in valid_moves:
                board_copy = deepcopy(board)
                board_copy.make_move(*move)
                value = max(value, self.minimax(board_copy, depth - 1, alpha, beta, False))
                alpha = max(alpha, value)
                if beta <= alpha:
                    # print(f"Prune at depth={depth}, alpha={alpha}, beta={beta}")
                    break  # Alpha-beta pruning
            return value
        else:
            value = float('inf')
            for move in valid_moves:
                board_copy = deepcopy(board)
                board_copy.make_move(*move)
                value = min(value, self.minimax(board_copy, depth - 1, alpha, beta, True))
                beta = min(beta, value)
                if beta <= alpha:
                    # print(f"Prune at depth={depth}, alpha={alpha}, beta={beta}")
                    break  # Alpha-beta pruning
            return value

    def evaluate_board2(self, board):
        """Evaluate the board based on various heuristics."""
        total_pieces = self.count_total_pieces(board)
        # Improved weights for each phase
        if total_pieces < 20:
            weights = {
                'piece_difference': 2,
                'mobility': 150,
                'corner_control': 250,
                'stability': 30,
                'adjacent_to_corners': -100
            }
        elif total_pieces < 50:
            weights = {
                'piece_difference': 25,
                'mobility': 70,
                'corner_control': 600,
                'stability': 120,
                'adjacent_to_corners': -50
            }
        else:
            weights = {
                'piece_difference': 300,
                'mobility': 5,
                'corner_control': 2000,
                'stability': 200,
                'adjacent_to_corners': -5
            }

        # pd = self.piece_difference(board)
        # mo = self.mobility(board)
        # cc = self.corner_control(board)
        # st = self.stability(board)
        # ac = self.adjacent_to_corners(board)
        # print(f"[DEBUG] piece_difference={pd}, mobility={mo}, corner_control={cc}, stability={st}, adjacent_to_corners={ac}")

        score = (
            weights['piece_difference'] * self.piece_difference(board) +
            weights['mobility'] * self.mobility(board) +
            weights['corner_control'] * self.corner_control(board) +
            weights['stability'] * self.stability(board) +
            weights['adjacent_to_corners'] * self.adjacent_to_corners(board)
        )
        return score

    def count_total_pieces(self, board) -> int:
        """Count the total number of pieces on the board."""
        player_count = sum(row.count(board._current_player) for row in board.board)
        opponent_count = sum(row.count(1 - board._current_player) for row in board.board)
        return player_count + opponent_count

    def piece_difference(self, board) -> float:
        """Evaluate the difference in pieces."""
        player_count = sum(row.count(board._current_player) for row in board.board)
        opponent_count = sum(row.count(1 - board._current_player) for row in board.board)
        total = player_count + opponent_count
        if total == 0:
            return 0
        return 100 * (player_count - opponent_count) / total

    def mobility(self, board) -> float:
        """Evaluate the mobility of the players."""
        ia_moves = len(board.get_valid_moves())
        orig_player = board._current_player
        board._current_player = 1 - orig_player
        adv_moves = len(board.get_valid_moves())
        board._current_player = orig_player
        if ia_moves + adv_moves == 0:
            return 0
        return 100 * (ia_moves - adv_moves) / (ia_moves + adv_moves)

    def corner_control(self, board) -> float:
        """Evaluate the corner control."""
        corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
        ia = 0
        adv = 0
        for x, y in corners:
            val = board.get_at(x, y)
            if val == board._current_player:
                ia += 1
            elif val == 1 - board._current_player:
                adv += 1
        return 25 * (ia - adv)

    def stability(self, board) -> float:
        """Evaluate the stability of pieces."""
        corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
        edges = [(i, j) for i in [0, 7] for j in range(1, 7)] + [(i, j) for i in range(1, 7) for j in [0, 7]]
        stable_ia = 0
        stable_adv = 0
        current = board._current_player
        opponent = 1 - current
        for x in range(8):
            for y in range(8):
                piece = board.get_at(x, y)
                if piece == current:
                    if (x, y) in corners:
                        stable_ia += 2
                    elif (x, y) in edges:
                        stable_ia += 1
                elif piece == opponent:
                    if (x, y) in corners:
                        stable_adv += 2
                    elif (x, y) in edges:
                        stable_adv += 1
        total = stable_ia + stable_adv
        if total == 0:
            return 0
        return 100 * (stable_ia - stable_adv) / total

    def adjacent_to_corners(self, board) -> float:
        """Evaluate the danger of being adjacent to corners."""
        danger_coords = {
            (0, 0): [(0, 1), (1, 0), (1, 1)],
            (0, 7): [(0, 6), (1, 7), (1, 6)],
            (7, 0): [(6, 0), (7, 1), (6, 1)],
            (7, 7): [(6, 7), (7, 6), (6, 6)],
        }
        score = 0
        for corner, adjacents in danger_coords.items():
            corner_val = board.get_at(*corner)
            for x, y in adjacents:
                if board.get_at(x, y) == board._current_player and corner_val == 0:
                    score -= 12.5
                elif board.get_at(x, y) == 1 - board._current_player and corner_val == 0:
                    score += 12.5
        return score / 1.5