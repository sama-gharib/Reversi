from model.move import Move
from model.player import Player
from typing import Optional, Tuple
import math

class AlphaBeta(Player):
    def __init__(self, max_depth: int = 8):
        super().__init__()
        self.max_depth = max_depth
    
    def _think(self, board) -> Move:

        best_move = self._get_best_move(board)
        if best_move is None:
            raise Exception("[DEBUG] No valid moves available but game didn't end")
            
        return Move(best_move[1], best_move[0])
    
    def _get_best_move(self, board) -> Optional[Tuple[int, int]]:
        """ Gets the best move using alpha-beta pruning """
        valid_moves = board.get_valid_moves()
        if not valid_moves:
            return None
            
        _, best_move = self._alphabeta(board, self.max_depth)
        return best_move
    
    def _alphabeta(
        self, 
        board, 
        depth: int, 
        alpha: float = -math.inf, 
        beta: float = math.inf, 
        maximizing_player: bool = True
    ) -> Tuple[float, Optional[Tuple[int, int]]]:
        """ Alpha-Beta Pruning implementation """
        if depth == 0 or board.is_game_over():
            return self._evaluate_board(board), None

        valid_moves = board.get_valid_moves()
        if not valid_moves:
            # Pass turn
            new_board = board.copy()
            new_board._current_player = 1 - new_board.current_player
            return self._alphabeta(new_board, depth - 1, alpha, beta, not maximizing_player)

        best_move = None
        
        if maximizing_player:
            max_eval = -math.inf
            for move in valid_moves:
                new_board = board.copy()
                new_board.make_move(*move)
                
                eval, _ = self._alphabeta(new_board, depth - 1, alpha, beta, False)
                
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
                        
            return max_eval, best_move
        else:
            min_eval = math.inf
            for move in valid_moves:
                new_board = board.copy()
                new_board.make_move(*move)
                
                eval, _ = self._alphabeta(new_board, depth - 1, alpha, beta, True)
                
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
                        
            return min_eval, best_move
    
    def _evaluate_board(self, board) -> float:
        """ Evaluates the board state for the current player """
        # Evaluation weights
        weights = {
            'coin_parity': 1.0,
            'mobility': 2.0,
            'corner': 5.0,
            'stability': 3.0,
            'edge': 2.5
        }
        
        # Coin parity (normalized)
        player_count = sum(row.count(board.current_player) for row in board.board)
        opponent_count = sum(row.count(1 - board.current_player) for row in board.board)
        total = player_count + opponent_count + 1  # +1 to avoid division by zero
        coin_parity = (player_count - opponent_count) / total
        
        # Mobility
        current_moves = len(board.get_valid_moves())
        board._current_player = 1 - board.current_player
        opponent_moves = len(board.get_valid_moves())
        board._current_player = 1 - board.current_player  # Switch back
        mobility = (current_moves - opponent_moves) / (current_moves + opponent_moves + 1)
        
        # Corner control
        corners = [(0,0), (0,7), (7,0), (7,7)]
        player_corners = sum(1 for (x,y) in corners if board.get_at(x,y) == board.current_player)
        opponent_corners = sum(1 for (x,y) in corners if board.get_at(x,y) == 1 - board.current_player)
        corner_total = player_corners + opponent_corners + 1
        corner_control = (player_corners - opponent_corners) / corner_total
        
        # Edge control
        edges = [(i,j) for i in [0,7] for j in range(1,7)] + [(i,j) for i in range(1,7) for j in [0,7]]
        player_edges = sum(1 for (x,y) in edges if board.get_at(x,y) == board.current_player)
        opponent_edges = sum(1 for (x,y) in edges if board.get_at(x,y) == 1 - board.current_player)
        edge_total = player_edges + opponent_edges + 1
        edge_control = (player_edges - opponent_edges) / edge_total
        
        # Stability (simplified)
        stability = self._calculate_stability(board)
        
        # Weighted sum
        evaluation = (
            weights['coin_parity'] * coin_parity +
            weights['mobility'] * mobility +
            weights['corner'] * corner_control +
            weights['edge'] * edge_control +
            weights['stability'] * stability
        )
        
        return evaluation
    
    def _calculate_stability(self, board) -> float:
        """ Simplified stability calculation """
        corners = [(0,0), (0,7), (7,0), (7,7)]
        edges = [(i,j) for i in [0,7] for j in range(1,7)] + [(i,j) for i in range(1,7) for j in [0,7]]
        
        stable = 0
        for x in range(8):
            for y in range(8):
                if board.get_at(x,y) == board.current_player:
                    if (x,y) in corners:
                        stable += 2  # Corners are very stable
                    elif (x,y) in edges:
                        stable += 1  # Edges are somewhat stable
        
        return stable / 64  # Normalized