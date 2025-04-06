from model.move import Move
from model.player import Player
from model.board import Board

from random import uniform

from time import sleep

class Minimax (Player):

    def _think(self, board) -> Move:
        sleep(uniform(0.5, 1)) # Simulate thinking time
        # On utilise l'algorithme Minimax pour déterminer le meilleur coup
        c = self.best_move(board, 4)
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
        corners = [(0,0), (0,7), (7,0), (7,7)]
        for move in valid_moves:
            if move in corners:
                # Si on joue un coin, on ne cherche pas plus loin
                return move
            
            # Une copie = on simule un coup valide
            print(f"[DEBUG] Move1: {move}")
            board_copy = board.copy()
            board_copy.make_move(move[0], move[1])
            score = self.minimax(board_copy, depth - 1, float('-inf'), float('inf'), False)

            if score > best_score:
                best_score = score
                best_move = move

        return best_move
          
    def minimax(self, board, depth, alpha, beta, maximizing_player):
        new_board = board.copy()
        valid_moves = new_board.get_valid_moves()

        if depth == 0 or len(valid_moves) == 0:
            return self.evaluate_board2(new_board)
        
        if maximizing_player:
            best_score = float('-inf')

            for move in valid_moves:
                new_board = board.copy()
                new_board.make_move(*move)

                score = self.minimax(new_board, depth - 1, alpha, beta, False)

                if score > best_score:
                    best_score = score
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
            
            return best_score
        
        else:
            best_score = float('inf')

            for move in valid_moves:
                new_board = board.copy()
                new_board.make_move(*move)

                score = self.minimax(new_board, depth - 1, alpha, beta, True)

                if score < best_score:
                    best_score = score
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
            
            return best_score

        
    def evaluate_board(self, board) -> float:
        """ Évalue le plateau de jeu en fonction des poids définis."""
        WEIGHTS = [
        [150, -50, 20,  10,  10, 20, -50, 150],
        [-50, -50, -2, -2, -2, -2, -50, -50],
        [20,  -2,  1,  1,  1,  1,  -2,  20],
        [10,   -2,  1,  0,  0,  1,  -2,   10],
        [10,   -2,  1,  0,  0,  1,  -2,   10],
        [20,  -2,  1,  1,  1,  1,  -2,  20],
        [-50, -50, -2, -2, -2, -2, -50, -50],
        [150, -50, 20,  10,  10, 20, -50, 150]
        ]

        score = 0
        for x in range(8):
            for y in range(8):
                if board.get_at(x, y) == board.current_player:  # L'IA
                    score += WEIGHTS[x][y]
                elif board.get_at(x, y) == 1 - board.current_player:  # Adversaire
                    score -= WEIGHTS[x][y]
        return score
    
    def evaluate_board2(self, board) -> float:
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