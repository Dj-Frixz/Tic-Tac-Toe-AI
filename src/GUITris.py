import sys
sys.path.append('lib')
import numpy as np
from src.AITris import Tris
#import lib.pygame as pygame
import pygame
from data.utils import load_sprite

class Game:

    def __init__(self):
        self.screen = None
        self._init_pygame()
        self.background = load_sprite('board-1000.png',False)
        self.AI = Tris()
        self.pawn = (None,load_sprite('cross-200.png'),load_sprite('nought-200.png'))
        self.grid = (
            (pygame.Rect(190,150,200,200),pygame.Rect(415,150,200,200),pygame.Rect(650,150,200,200)),
            (pygame.Rect(190,390,200,200),pygame.Rect(415,390,200,200),pygame.Rect(650,390,200,200)),
            (pygame.Rect(190,640,200,200),pygame.Rect(415,640,200,200),pygame.Rect(650,640,200,200))
        )
        self.clock = pygame.time.Clock()
        self.empty_cells = np.full(7,6,np.int8)
        self.last_move = 0
        self.font = pygame.font.Font(None, 50)

    def _init_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000,1000))
        pygame.display.set_caption("Smart Noughts and Crosses")
        pygame.display.set_icon(load_sprite('Red_x.png'))

    def main_loop(self):
        self._draw_init()
        while 1:
            if self.AI.turn:
                a,b = self.AI.Compute()
                self._pc_move(a,b)
                check = self.AI.CheckWin(self.AI.game,a,b,True)
                if check == 1:
                    self._game_over_screen("I'm sorry, you lost. L ez win lol.")
                elif check == 0:
                    self._game_over_screen("It's a tie. Dang.")
            else:
                if self._handle_input():
                    self._game_over_screen("It's a tie. Dang.")

    def _handle_input(self,restart=None):
        #waiting for user input
        while 1:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    quit()
                if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
                    if restart:
                        self.AI.Reset()
                        self._draw_init()
                        return
                    mouse_pos = pygame.mouse.get_pos()
                    for i in range(3):
                        for j in range(3):
                            if self.grid[i][j].collidepoint(mouse_pos) and self.AI.game[i,j]==0:
                                tie = self.AI.Move(i,j) +1
                                # draw the cross/nought on the board
                                self.screen.blit(self.pawn[self.AI.pl],self.grid[i][j].topleft)
                                pygame.display.flip()
                                self.AI.turn = not(self.AI.turn)
                                return tie

    def _draw_init(self):
        self.screen.blit(self.background,(0,0))

        # USE FOR DEBUGGING
        #for row in self.grid:
        #    for rect in row:
        #        pygame.draw.rect(self.screen, (255,0,0), rect)

        pygame.display.flip()

    def _pc_move(self,a,b):
        self.screen.blit(self.pawn[self.AI.pc],self.grid[a][b].topleft)
        pygame.display.flip()

    def _game_over_screen(self,message:str):
        game_over = self.font.render(message, False, (0,0,0), (255,255,255))
        rect = game_over.get_rect()
        rect.center = (500,500)
        self.screen.blit(game_over,rect.topleft)
        pygame.display.flip()
        self._handle_input(restart=1)

    def _reset(self):
        self.board = np.zeros((6,7),np.int8)
        self.empty_cells = np.full(7,6,np.int8)
        self.turn = 1