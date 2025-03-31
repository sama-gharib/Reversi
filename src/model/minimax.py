from model.move import Move
from model.player import Player
from model.board import Board

from random import uniform

from time import sleep

class Minimax (Player):

    def _think(self, board) -> Move:
        sleep(uniform(0.5, 1)) # Simulate thinking time
        # On utilise l'algorithme Minimax pour déterminer le meilleur coup
        c = self.best_move(board, 3)
        if c is not None:
            return Move(c[1], c[0])
        else:
            # Si aucun coup n'est trouvé, on retourne un coup par défaut
            valid_moves = board.get_valid_moves()
            return Move(valid_moves[0][1], valid_moves[0][0])
    
    def best_move(self, board, depth) -> Move:
        best_score = float('-inf')
        best_move = None
        valid_moves = board.get_valid_moves()
        print(f"[DEBUG] Valid moves: {valid_moves}")
        for move in valid_moves:
            board_copy = board.copy()
            board_copy.make_move(move[0], move[1])
            score = self.minimax(board_copy, depth - 1, False)
            print(f"[DEBUG] Move: {move}, Score: {score}")
            if score > best_score:
                best_score = score
                best_move = move
        print(f"[DEBUG] Best move: {best_move} with score: {best_score}")
        return best_move
    
    def minimax(self, board, depth, maximizing_player):
        if depth == 0 or board.is_game_over():
            return board.evaluate_board()

        if maximizing_player:
            max_eval = float('-inf')
            for move in board.get_valid_moves():
                new_board = board.copy()
                new_board.make_move(move[0], move[1])

                eval = self.minimax(new_board, depth - 1, False)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for move in board.get_valid_moves():
                new_board = board.copy()
                new_board.make_move(move[0], move[1])

                eval = self.minimax(new_board, depth - 1, True)
                min_eval = min(min_eval, eval)
            return min_eval