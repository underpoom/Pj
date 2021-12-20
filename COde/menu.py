import pygame
import avl
import move
from tkinter import *
from functools import partial
pygame.init()

class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = - 100
        self.main_music = pygame.mixer.init()

    def draw_cursor(self):
        self.game.draw_text('*', 15, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()

class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.name = 'MainMenu'
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h + 30
        self.HowToPlayx, self.HowToPlayy = self.mid_w, self.mid_h + 60
        self.Exitx, self.Exity = self.mid_w, self.mid_h + 90
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty+20)
        
    def txthsname(self):
        scoredatatmp = ''
        with open("score.txt") as file_in: #เช็คว่าใน score.txt มีชื่อซ้ำไหมถ้ามีให้แก้เป็นของใหม่
            for line in file_in:
                
                scoreRead = line.split()
                
                scoredatatmp += str(scoreRead[0])+' '*(10-len(scoreRead[0]))+str(scoreRead[1])+'\n'
        
        return scoredatatmp

    def txthsname(self):
        scoredatatmp = ''
        ndata = 0
        with open("score.txt") as file_in: #เช็คว่าใน score.txt มีชื่อซ้ำไหมถ้ามีให้แก้เป็นของใหม่
            for line in file_in :
                scoreRead = line.split()
                scoredatatmp += str(scoreRead[0])+'\n'
                ndata+=1
                if ndata>=5:
                    break
        return scoredatatmp

    def txthsscore(self):
        scoredatatmp = ''
        ndata = 0
        with open("score.txt") as file_in: #เช็คว่าใน score.txt มีชื่อซ้ำไหมถ้ามีให้แก้เป็นของใหม่
            for line in file_in :
                scoreRead = line.split()
                scoredatatmp += str(scoreRead[1])+'\n'
                ndata+=1
                if ndata>=5:
                    break
        return scoredatatmp

    def blit_text(self,surface, text, pos, font, color=pygame.Color('orangered')):
        #color = self.game.RAINBOW1
        words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
        space = font.size(' ')[0]  # The width of a space.
        max_width, max_height = surface.get_size()
        x, y = pos
        for line in words:
            for word in line:
                word_surface = font.render(word, 0, color)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width:
                    x = pos[0]  # Reset the x.
                    y += word_height  # Start on new row.
                surface.blit(word_surface, (x, y))
                x += word_width + space
            x = pos[0]  # Reset the x.
            y += word_height  # Start on new row.

    def display_menu(self):
        k=50
        poshs_y = self.game.DISPLAY_H / 2 +100
        poshs_x_name = self.game.DISPLAY_W / 2+200+k
        poshs_x_score = self.game.DISPLAY_W / 2+300+k

        font = pygame.font.SysFont(pygame.font.get_default_font(), 30)
        self.run_display = True
        pygame.mixer.music.unload()
        pygame.mixer.music.load("Kings_tree.mp3")
        pygame.mixer.music.play(-1)

        
        bgtree = pygame.image.load("treebg.png")
        
        bgtree = pygame.transform.scale(bgtree, (self.game.DISPLAY_W,self.game.DISPLAY_H))
          
        recttt = pygame.Surface((300,180))
        recttt.set_alpha(128)
        recttt.fill((0,0,0))

        while self.run_display:
            
        
            self.game.check_events()
            self.check_input()
            

            self.game.display.blit(bgtree,(0,0))
            self.game.display.blit(recttt,(3/4*self.game.DISPLAY_W -50,self.game.DISPLAY_H * 3/4 - 50))
            self.game.draw_text("Top #5 high score", 30, poshs_x_name+120, poshs_y+40,1)
            self.blit_text(self.game.display,self.txthsname(),(poshs_x_name+40, poshs_y+60),font)
            self.blit_text(self.game.display,self.txthsscore(),(poshs_x_score+40, poshs_y+60),font)
            
            #pygame.draw.rect(self.game.display,GREEN, pygame.Rect(50,50,90,180) )
            self.game.draw_text("King's Tree", 60, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 50)
            self.game.draw_text("Start Game", 30, self.startx, self.starty+20)
            self.game.draw_text("HowToPlay", 30, self.HowToPlayx, self.HowToPlayy+40)
            self.game.draw_text("Exit", 30, self.Exitx, self.Exity+60)
            
            
            self.draw_cursor()
            self.blit_screen()
            pygame.display.update()
            


    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.HowToPlayx + self.offset, self.HowToPlayy+40)
                self.state = 'HowToPlay'
            elif self.state == 'HowToPlay':
                self.cursor_rect.midtop = (self.Exitx + self.offset, self.Exity+60)
                self.state = 'Exit'
            elif self.state == 'Exit':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty+20)
                self.state = 'Start'
        elif self.game.UP_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.Exitx + self.offset, self.Exity+60)
                self.state = 'Exit'
            elif self.state == 'HowToPlay':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty+20)
                self.state = 'Start'
            elif self.state == 'Exit':
                self.cursor_rect.midtop = (self.HowToPlayx + self.offset, self.HowToPlayy+40)
                self.state = 'HowToPlay'

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Start':
                self.game.playing = True
                self.game.gameTree = avl.GameTree()
            elif self.state == 'HowToPlay':
                self.game.curr_menu = self.game.HowToPlay
            elif self.state == 'Exit':
                self.game.curr_menu = self.game.Exit
            self.run_display = False

class HowToPlayMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.name = 'HowToPlay'
        #self.state = 'Volume'
        #self.volx, self.voly = self.mid_w, self.mid_h + 20
        #self.controlsx, self.controlsy = self.mid_w, self.mid_h + 40
        #self.cursor_rect.midtop = (self.volx + self.offset, self.voly)

    def display_menu(self):
        self.run_display = True
        bg1 = pygame.image.load("HTP.jpg")
        bg1 = pygame.transform.scale(bg1, (self.game.DISPLAY_W,self.game.DISPLAY_H))
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.blit(bg1,(0,0))
            #self.game.display.fill((0, 0, 0))
            #self.game.draw_text('HowToPlay', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 30)
            #self.game.draw_text("Volume", 15, self.volx, self.voly)
            #self.game.draw_text("Controls", 15, self.controlsx, self.controlsy)
            #self.draw_cursor()
            self.blit_screen()
    
    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        #elif self.game.UP_KEY or self.game.DOWN_KEY:
        #    if self.state == 'Volume':
        #        self.state = 'Controls'
        #        self.cursor_rect.midtop = (self.controlsx + self.offset, self.controlsy)
        #    elif self.state == 'Controls':
        #         self.state = 'Volume'
        #         self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
        elif self.game.START_KEY:
            # TO-DO: Create a Volume Menu and a Controls Menu
            pass

class Queue :
    def __init__(self) -> None:
        self.data = []
    def __str__(self) -> str:
        return str(self.data)
    def is_empty(self):
        return len(self.data) == 0
    def __len__(self):
        return len(self.data)
    def enqueue(self, new_data):
        return self.data.append(new_data)
    def dequeue(self):
        if self.is_empty():
            return 'empty'
        return self.data.pop(0)
    def size(self):
        return len(self.data)
    def top(self):
        if self.is_empty():
            return -1
        return self.data[0]
        
class ExitMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.name = 'Exit'

    def display_menu(self):
        pygame.quit()
        self.game.running = False
        #self.run_display = True
        #while self.run_display:
        #    self.game.check_events()
        #   if self.game.START_KEY or self.game.BACK_KEY:
        #       self.game.curr_menu = self.game.main_menu
        #        self.run_display = False
        #    self.game.display.fill(self.game.BLACK)
            #self.game.draw_text('Exit', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            #self.game.draw_text('Made by me', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 10)
            
        #   self.blit_screen()

class FinishedState(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.name = 'Finish'
        self.Exitx, self.Exity = self.mid_w, self.mid_h + 90
        self.cursor_rect.midtop = (self.Exitx + self.offset, self.Exity+60)
        self.user_text = ''
        self.base_font = pygame.font.Font(None,48)
        self.text_surface = self.base_font.render(self.user_text,True,(255,255,255))
        self.input_rect = pygame.Rect(self.game.DISPLAY_W/2-50,self.game.DISPLAY_H/2 - 70,140,48)
       

    def display_menu(self):
        self.run_display = True 
        pygame.mixer.music.unload()
        pygame.mixer.music.load("pogChamp.mp3")
        pygame.mixer.music.play(-1)
        while self.run_display:
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('You Win!', 80, self.game.DISPLAY_W/2, self.game.DISPLAY_H/4)
            self.game.draw_text(self.game.text[0], 30, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 10)
            self.game.draw_text(self.game.text[1], 30, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 50)
            self.game.draw_text(self.game.text[2], 30, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 90)
            self.game.draw_text("Enter", 30, self.Exitx, self.Exity+60)
            self.game.draw_text("Enter Your Name :",32,self.game.DISPLAY_W/2-200,self.game.DISPLAY_H/2-50)
            pygame.draw.rect(self.game.display,self.game.WHITE,self.input_rect,2)
            self.draw_cursor()
            self.text_surface = self.base_font.render(self.user_text,True,(255,255,255))
            self.game.display.blit(self.text_surface,(self.input_rect.x + 5,self.input_rect.y + 5))
            self.input_rect.w = max(100,self.text_surface.get_width() + 10)
            self.game.window.blit(self.game.display, (0, 0))
            pygame.display.update()
            self.game.reset_keys()

        #input username
        
    def bbsort(self,l):
        n = len(l)
        for i in range(n):
            for j in range(0,n-i-1):
                if float(l[j+1][1]) > float(l[j][1]):
                    l[j],l[j+1] = l[j+1],l[j]
        return l
    
    def check_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.game.curr_menu.run_display = False
                self.game.curr_menu = self.game.Exit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    print('test')
                    self.game.curr_menu = self.game.main_menu
                    self.game.gameTree = avl.GameTree()
                    #move.nmove = 0
                    self.run_display = False
                    scoredatatmp = Queue() #เอาไว้ดึงข้อมูลใน score.txt มาเก็บไว้ใน list
                    with open("score.txt") as file_in: #เช็คว่าใน score.txt มีชื่อซ้ำไหมถ้ามีให้แก้เป็นของใหม่
                        for line in file_in:
                            print(line)
                            scoreRead = line.split()
                            scoredatatmp.enqueue(scoreRead)
                    scoredatatmp.enqueue([self.user_text,str(self.game.score)])
                    scoredatatmp.data = self.bbsort(scoredatatmp.data)
                    with open('score.txt', 'w') as f: #เขียนข้อมูลใน list ที่เก็บ scoredatatmp ไว้ลง txt
                        for item in scoredatatmp.data:
                            f.write(item[0] + "  " + item[1]+"\n")
                    self.user_text = ''

                ###

                    
                if event.key == pygame.K_BACKSPACE:
                    self.user_text = self.user_text[:-1]
                elif len(self.user_text) < 8:
                    self.user_text += event.unicode
            

            
