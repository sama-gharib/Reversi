from model.move import Move
from model.player import Player
from model.board import Board

from random import uniform

from time import sleep

from copy import deepcopy

class Minimax (Player):

    def _think(self, board) -> Move:
        #sleep(uniform(0.5, 1)) # Simulate thinking time
        c = self.best_move(board, 6)
        if c is not None:
            return Move(c[1], c[0])
        else:
            # Si aucun coup n'est trouvé, on retourne un coup par défaut
            valid_moves = board.get_valid_moves()
            return Move(valid_moves[0][1], valid_moves[0][0])
    
    def best_move(self, board, depth) -> Move:
        """ Find the best move using minimax algorithm """
        best_score = float('-inf')
        best_move = None
        valid_moves = board.get_valid_moves()
        if not valid_moves:
            return None
        for move in valid_moves:
            board_copy = deepcopy(board)
            board_copy.make_move(move[0], move[1])
            score = self.minimax(board_copy, depth-1, float('-inf'), float('inf'), False, indent=1)
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

    def minimax(self, board, depth: int, alpha: float, beta: float, maximizing_player: bool, indent=0):
        """ Minimax algorithm with alpha-beta pruning and tree visualization """
        valid_moves = board.get_valid_moves()

        if depth == 0 or not valid_moves:
            eval_score = self.evaluate_board2(board)
            return eval_score

        if maximizing_player:
            best_score = float('-inf')
            for move in valid_moves:
                board_copy = deepcopy(board)
                board_copy.make_move(*move)
                score = self.minimax(board_copy, depth - 1, alpha, beta, False, indent+1)
                if score > best_score:
                    best_score = score
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
            return best_score
        else:
            best_score = float('inf')
            for move in valid_moves:
                board_copy = deepcopy(board)
                board_copy.make_move(*move)
                score = self.minimax(board_copy, depth - 1, alpha, beta, True, indent+1)
                if score < best_score:
                    best_score = score
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
            return best_score

    def evaluate_board2(self, board):
        """ Evaluate the board based on various heuristics """
        total_pieces = self.count_total_pieces(board)

        # Beginning of game
        if total_pieces < 20:
            weights = {
                'piece_difference': 10,
                'mobility': 100,
                'corner_control': 500,
                'stability': 30,
                'adjacent_to_corners': -50
            }
        # Mid game
        elif total_pieces < 50:
            weights = {
                'piece_difference': 20,
                'mobility': 50,
                'corner_control': 700,
                'stability': 50,
                'adjacent_to_corners': -30
            }
        # End of game
        else:
            weights = {
                'piece_difference': 100,
                'mobility': 20,
                'corner_control': 1000,
                'stability': 100,
                'adjacent_to_corners': -10
            }

        # Calcul final score
        score = (
            weights['piece_difference'] * self.piece_difference(board) +
            weights['mobility'] * self.mobility(board) +
            weights['corner_control'] * self.corner_control(board) +
            weights['stability'] * self.stability(board) +
            weights['adjacent_to_corners'] * self.adjacent_to_corners(board)
        )

        return score
    
    def count_total_pieces(self, board) -> int:
        """ Count the total number of pieces on the board """
        player_count = sum(row.count(board._current_player) for row in board.board)
        opponent_count = sum(row.count(1 - board._current_player) for row in board.board)
        return player_count + opponent_count

    
    def piece_difference(self, board) -> float:
        """ Evaluate the difference in pieces """
        player_count = sum(row.count(board._current_player) for row in board.board)
        opponent_count = sum(row.count(1 - board._current_player) for row in board.board)
        total = player_count + opponent_count
        if total == 0:
            return 0
        return 100 * (player_count - opponent_count) / total
    
    def mobility(self, board) -> float:
        """ Evaluate the mobility of the players """
        ia_moves = len(board.get_valid_moves())
        # Save current player to avoid side effects
        orig_player = board._current_player
        board._current_player = 1 - orig_player
        adv_moves = len(board.get_valid_moves())
        board._current_player = orig_player
        if ia_moves + adv_moves == 0:
            return 0
        return 100 * (ia_moves - adv_moves) / (ia_moves + adv_moves)
    
    def corner_control(self, board) -> float:
        """ Evaluate the corner control """
        corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
        ia = 0
        adv = 0
        for x, y in corners:
            if board.get_at(x, y) == board._current_player:
                ia += 1
            elif board.get_at(x, y) == 1 - board._current_player:
                adv += 1
        return 25 * (ia - adv)
    
    def stability(self, board) -> float:
        """ Evaluate the stability of pieces """
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
        """ Evaluate the danger of being adjacent to corners """
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
        return score/ 1.5