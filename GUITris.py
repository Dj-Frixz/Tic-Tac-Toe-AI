import numpy as np
from numpy.core.fromnumeric import size
from AITris import Tris
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
        # self.turn = False
        self.last_move = 0

    def _init_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000,1000))
        pygame.display.set_caption("Smart Noughts and Crosses")
        pygame.display.set_icon(load_sprite('Red_x.png'))

    def main_loop(self):
        self._draw_init()
        while 1:
            print(self.AI.turn)
            if self.AI.turn:
                self._pc_move(self.AI.Compute())
            else:
                self._handle_input()
            

    def _handle_input(self):
        #waiting for user input
        while 1:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    quit()
                if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
                    mouse_pos = pygame.mouse.get_pos()
                    for i in range(3):
                        for j in range(3):
                            if self.grid[i][j].collidepoint(mouse_pos) and self.AI.game[i][j]==0:
                                self.AI.game[i][j] = self.AI.pl
                                # draw the cross/nought on the board
                                self.screen.blit(self.pawn[self.AI.pl],self.grid[i][j].topleft)
                                pygame.display.flip()
                                self.AI.turn = self.AI.turn == False
                                return

    def _draw_init(self):
        self.screen.blit(self.background,(0,0))
        # USE FOR DEBUGGING
        #for row in self.grid:
        #    for rect in row:
        #        pygame.draw.rect(self.screen, (255,0,0), rect)

        pygame.display.flip()

    def _draw(self,surface,pos):
        pos = self._find_pos(pos)
        self.screen.blit(surface,(int(pos[0]*2.99/1000),int(pos[1]*2.99/1000)))
        pygame.display.flip()

    def _pc_move(self,move):
        self.screen.blit(self.pawn[self.AI.pc],self.grid[move[0]][move[1]].topleft)
        pygame.display.flip()

    def _reset(self):
        self.board = np.zeros((6,7),np.int8)
        self.empty_cells = np.full(7,6,np.int8)
        self.turn = 1