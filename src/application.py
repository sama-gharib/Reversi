from model.board import Board
from model.player import Player
from model.human import Human
from model.stupidity import Stupidity
from view.ui import default_ui
from utils import ReactiveStr

import pygame

class Application:
    KNOWN_WHITE_PLAYERS = {
        "human": Human(),
        "stupidity": Stupidity()
    }
    
    KNOWN_BLACK_PLAYERS = {
        "human": Human(),
        "stupidity": Stupidity()
    }
    
    def __init__(self):
        self.reset()
        self._ui = default_ui(self)

    def reset(self):
        self._board = Board()
        self._white_key = ReactiveStr("human")
        self._black_key = ReactiveStr("human")

    def get_black_key(self):
        return self._black_key
    
    def get_white_key(self):
        return self._white_key

    def set_white_key(self, p: str):
        if p in self.KNOWN_WHITE_PLAYERS:
            self._white_key.value = p
            print(f"[DEBUG] Set white player to {p}.")
        else:
            print(f'[DEBUG] ERROR: Tried to set white player to unknown player type "{p}".')
    
    def set_black_key(self, p: str):
        if p in self.KNOWN_BLACK_PLAYERS:
            self._black_key.value = p
            print(f"[DEBUG] Set black player to {p}.")
        else:
            print(f'[DEBUG] ERROR: Tried to set black player to unknown player type "{p}".')

    @property
    def _black_player(self):
        return self.KNOWN_BLACK_PLAYERS[self._black_key.value]
    
    @property
    def _white_player(self):
        return self.KNOWN_WHITE_PLAYERS[self._white_key.value]
        
    def run(self):
        screen = pygame.display.set_mode((800, 600))
        clock = pygame.time.Clock()
        running = True
        
        while running and not self._ui.has_quit():
            if self._ui.get_tab_name() == "game_ui":
                # If a player have no valid moves 
                while not self._board.get_valid_moves():
                    print(f"[DEBUG] No valid moves for {'Black' if self._board.current_player == 0 else 'White'}. Switching turn.")
                    self._board._current_player = 1 - self._board._current_player
                    if not self._board.get_valid_moves():
                        break
                
                # Player turn rules
                if self._board.current_player == self._board.BLACK:
                    if self._black_player.is_done():
                        print("[DEBUG] Black's turn")
                        self._black_player.play_on(self._board)
                else:
                    if self._white_player.is_done():
                        print("[DEBUG] White's turn")
                        self._white_player.play_on(self._board)

            # Check if the game is over
            if self._board.is_game_over():
                winner = self._board.get_winner()
                if winner == self._board.BLACK:
                    print("[DEBUG] Game Over! Black wins!")
                elif winner == self._board.WHITE:
                    print("[DEBUG] Game Over! White wins!")
                else:
                    print("[DEBUG] Game Over! It's a tie!")
                running = False  # End the game

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    self._ui.event(event)

            screen.fill("white")
            self._ui.draw(screen)
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
