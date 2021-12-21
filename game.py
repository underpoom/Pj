import pygame
from menu import *
import avl
import move
import tkinter.messagebox
from tkinter import *

class Game():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("KING's Tree")
        self.running, self.playing = True, False
        self.ESC_KEY,self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.LEFT_KEY, self.RIGHT_KEY = False, False, False, False,False,False,False
        self.DISPLAY_W, self.DISPLAY_H = 1280/1.2, 720/1.2
        self.display = pygame.Surface((self.DISPLAY_W,self.DISPLAY_H))        
        self.window = pygame.display.set_mode(((self.DISPLAY_W,self.DISPLAY_H)))        
        self.font_name = pygame.font.get_default_font()
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        self.RAINBOW1 = (255,215,0)
        self.finished_state = FinishedState(self)
        self.main_menu = MainMenu(self)
        self.HowToPlay = HowToPlayMenu(self)
        self.Exit = ExitMenu(self)
        self.curr_menu = self.main_menu
        self.win = False
        self.gameTree = avl.GameTree()
        self.text = ''
        self.score = ''

    def game_loop(self):
        self.lChild,self.now,self.rChid = 30,50,90
        bg = pygame.image.load("bg.jpg")
        bg = pygame.transform.scale(bg, (self.DISPLAY_W,self.DISPLAY_H))
        while self.playing:
            self.check_events()
            if self.ESC_KEY or self.win:
                self.playing= False
            #self.display.fill(self.BLACK) #อันนี้commmentอยู่นะ อิอิ
            self.display.blit(bg,(0,0))
            #self.draw_text('Thanks for Playing', 20, self.DISPLAY_W/2, self.DISPLAY_H/2)
            self.draw_text(str(self.gameTree.current), 120, self.DISPLAY_W/2, self.DISPLAY_H/4)
            self.draw_text('Destination : '+str(self.gameTree.drand), 30, self.DISPLAY_W*3/4+80, self.DISPLAY_H-50)
            self.draw_text('Move : '+str(move.nmove), 30,self.DISPLAY_W/8,self.DISPLAY_H/16)
            self.window.blit(self.display, (0,0))
            pygame.display.update()
            self.reset_keys()
            if self.gameTree.current.val == self.gameTree.drand:
                self.win = True
        if self.win:
            self.text = move.accurage(move.nmove,self.gameTree.ansmove)
            self.score = move.score(move.nmove,self.gameTree.ansmove)
            #print(self.text)
            self.win = False
            self.curr_menu = self.finished_state
            self.reset_keys()
            move.nmove = 0
        else:
            move.nmove = 0
            self.reset_keys()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    if self.playing:
                        self.gameTree.current = move.moveBack(self.gameTree.current)
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
                if event.key == pygame.K_LEFT:
                    if self.playing:
                        self.gameTree.current = move.moveLeft(self.gameTree.current)
                    self.LEFT_KEY = True
                if event.key == pygame.K_RIGHT:
                    if self.playing:
                        self.gameTree.current = move.moveRight(self.gameTree.current)
                    self.RIGHT_KEY = True
                if event.key == pygame.K_ESCAPE:
                    self.ESC_KEY = True

    def reset_keys(self):
        self.ESC_KEY,self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.LEFT_KEY, self.RIGHT_KEY = False, False, False, False,False,False,False

    def draw_text(self, text, size, x, y ,deff = 0):
        font = pygame.font.Font("arial.ttf",size)
        if deff == 0:
            text_surface = font.render(text, True, self.WHITE)
        else:
            text_surface = font.render(text, True, pygame.Color("orangered"))
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface,text_rect)

    def getWin(self):
        return self.win