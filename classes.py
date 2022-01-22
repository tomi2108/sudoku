from ast import Pass
import pygame
import math
from queue import PriorityQueue
from random import randint, randrange
import constants as const

#Window
PANTALLA =  pygame.display.set_mode((const.WIDTH,const.WIDTH))
pygame.display.set_caption("Sudoku_solver")

class Cell:
    def __init__(self,x,y,width):
        self.number = 0
        self.number_color = const.BLACK
        self.x = x
        self.y = y
        self.fila = self.y//width
        self.col = self.x//width
        self.color = const.WHITE
        self.width = width
        self.definite = False
        self.locked = False
        self.pencil_marks=[]
        self.highlighted = False
        self.arrow = 0
        self.thermo = 0
    
    def get_pos(self):
        return self.fila,self.col

    def draw_highlight(self,win):
        highlight = pygame.image.load("Python/Proyectos/Sudoku_solver/Images/highlight.png")
        win.blit(highlight,(self.x,self.y))

    def draw_arrow(self,win):
        if self.arrow==1:
            pygame.draw.circle(win,const.GREY,(self.x+const.D_WIDTH,self.y+const.D_WIDTH),const.D_WIDTH,2)
        if self.arrow==2:
            pygame.draw.circle(win,const.GREY,(self.x+const.D_WIDTH,self.y+const.D_WIDTH),const.D_WIDTH,2)
            pygame.draw.line(win,const.GREY,(self.x+const.R_WIDTH,self.y),(self.x+const.si*const.R_WIDTH,self.y-const.si*const.R_WIDTH+const.R_WIDTH),3)
        if self.arrow==3:
            pygame.draw.circle(win,const.GREY,(self.x+const.D_WIDTH,self.y+const.D_WIDTH),const.D_WIDTH,2)
            pygame.draw.line(win,const.GREY,(self.x+const.R_WIDTH,self.y+const.R_WIDTH),(self.x+const.si*const.R_WIDTH,self.y+const.si*const.R_WIDTH),3)
        if self.arrow==4:
            pygame.draw.circle(win,const.GREY,(self.x+const.D_WIDTH,self.y+const.D_WIDTH),const.D_WIDTH,2)
            pygame.draw.line(win,const.GREY,(self.x,self.y+const.R_WIDTH),(self.x-const.si*const.R_WIDTH+const.R_WIDTH,self.y+const.si*const.R_WIDTH),3)
        if self.arrow==5:
            pygame.draw.circle(win,const.GREY,(self.x+const.D_WIDTH,self.y+const.D_WIDTH),const.D_WIDTH,2)
            pygame.draw.line(win,const.GREY,(self.x,self.y),(self.x-const.si*const.R_WIDTH+const.R_WIDTH,self.y-const.si*const.R_WIDTH+const.R_WIDTH),3)
        if self.arrow==6:
            pygame.draw.line(win,const.GREY,(self.x+const.D_WIDTH,self.y),(self.x+const.D_WIDTH,self.y+const.R_WIDTH),3)
        if self.arrow==7:
            pygame.draw.line(win,const.GREY,(self.x,self.y+const.D_WIDTH),(self.x+const.R_WIDTH,self.y+const.D_WIDTH),3)
        if self.arrow==8:
            pygame.draw.line(win,const.GREY,(self.x,self.y),(self.x+const.R_WIDTH,self.y+const.R_WIDTH),3)
        if self.arrow==9:
            pygame.draw.line(win,const.GREY,(self.x,self.y+const.R_WIDTH),(self.x+const.R_WIDTH,self.y),3)
        if self.arrow==10:
            pygame.draw.line(win,const.GREY,(self.x+const.D_WIDTH,self.y),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),3)
            pygame.draw.line(win,const.GREY,(self.x+const.R_WIDTH,self.y+const.D_WIDTH),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),3)
        if self.arrow==11:
            pygame.draw.line(win,const.GREY,(self.x+const.D_WIDTH,self.y),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),3)
            pygame.draw.line(win,const.GREY,(self.x,self.y+const.D_WIDTH),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),3)
        if self.arrow==12:
            pygame.draw.line(win,const.GREY,(self.x+const.D_WIDTH,self.y+const.R_WIDTH),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),3)
            pygame.draw.line(win,const.GREY,(self.x,self.y+const.D_WIDTH),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),3)
        if self.arrow==13:
            pygame.draw.line(win,const.GREY,(self.x+const.D_WIDTH,self.y+const.R_WIDTH),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),3)
            pygame.draw.line(win,const.GREY,(self.x+const.R_WIDTH,self.y+const.D_WIDTH),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),3)
        if self.arrow==14:
            pygame.draw.line(win,const.GREY,(self.x+const.D_WIDTH,self.y),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),3)
            pygame.draw.line(win,const.GREY,(self.x,self.y),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),3)
        if self.arrow==15:
            pygame.draw.line(win,const.GREY,(self.x+const.D_WIDTH,self.y),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),3)
            pygame.draw.line(win,const.GREY,(self.x+const.D_WIDTH,self.y+const.D_WIDTH),(self.x+const.R_WIDTH,self.y),3)
        if self.arrow==16:
            pygame.draw.line(win,const.GREY,(self.x+const.D_WIDTH,self.y),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),3)
            pygame.draw.line(win,const.GREY,(self.x,self.y+const.R_WIDTH),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),3)
        if self.arrow==17:
            pygame.draw.line(win,const.GREY,(self.x+const.D_WIDTH,self.y),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),3)
            pygame.draw.line(win,const.GREY,(self.x+const.D_WIDTH,self.y+const.D_WIDTH),(self.x+const.R_WIDTH,self.y+const.R_WIDTH),3)
        if self.arrow==18:
            pygame.draw.line(win,const.GREY,(self.x+const.D_WIDTH,self.y+const.R_WIDTH),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),3)
            pygame.draw.line(win,const.GREY,(self.x,self.y),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),3)
        if self.arrow==19:
            pygame.draw.line(win,const.GREY,(self.x+const.D_WIDTH,self.y+const.R_WIDTH),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),3)
            pygame.draw.line(win,const.GREY,(self.x+const.D_WIDTH,self.y+const.D_WIDTH),(self.x+const.R_WIDTH,self.y),3)
        if self.arrow==20:
            pygame.draw.line(win,const.GREY,(self.x+const.D_WIDTH,self.y+const.R_WIDTH),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),3)
            pygame.draw.line(win,const.GREY,(self.x,self.y+const.R_WIDTH),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),3)
        if self.arrow==21:
            pygame.draw.line(win,const.GREY,(self.x+const.D_WIDTH,self.y+const.R_WIDTH),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),3)
            pygame.draw.line(win,const.GREY,(self.x+const.D_WIDTH,self.y+const.D_WIDTH),(self.x+const.R_WIDTH,self.y+const.R_WIDTH),3)
        if self.arrow == 22:
            pygame.draw.line(win,const.GREY,(self.x,self.y+const.D_WIDTH),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),3)
            pygame.draw.line(win,const.GREY,(self.x,self.y),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),3)
        if self.arrow == 23:
            pygame.draw.line(win,const.GREY,(self.x,self.y+const.D_WIDTH),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),3)
            pygame.draw.line(win,const.GREY,(self.x+const.D_WIDTH,self.y+const.D_WIDTH),(self.x+const.R_WIDTH,self.y),3)
        if self.arrow == 24:
            pygame.draw.line(win,const.GREY,(self.x,self.y+const.D_WIDTH),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),3)
            pygame.draw.line(win,const.GREY,(self.x,self.y+const.R_WIDTH),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),3)
        if self.arrow == 25:
            pygame.draw.line(win,const.GREY,(self.x,self.y+const.D_WIDTH),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),3)
            pygame.draw.line(win,const.GREY,(self.x+const.D_WIDTH,self.y+const.D_WIDTH),(self.x+const.R_WIDTH,self.y+const.R_WIDTH),3)
        if self.arrow == 26:
            pygame.draw.line(win,const.GREY,(self.x+const.R_WIDTH,self.y+const.D_WIDTH),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),3)
            pygame.draw.line(win,const.GREY,(self.x,self.y),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),3)
        if self.arrow == 27:
            pygame.draw.line(win,const.GREY,(self.x+const.R_WIDTH,self.y+const.D_WIDTH),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),3)
            pygame.draw.line(win,const.GREY,(self.x+const.D_WIDTH,self.y+const.D_WIDTH),(self.x+const.R_WIDTH,self.y),3)
        if self.arrow == 28:
            pygame.draw.line(win,const.GREY,(self.x+const.R_WIDTH,self.y+const.D_WIDTH),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),3)
            pygame.draw.line(win,const.GREY,(self.x,self.y+const.R_WIDTH),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),3)
        if self.arrow == 29:
            pygame.draw.line(win,const.GREY,(self.x+const.R_WIDTH,self.y+const.D_WIDTH),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),3)
            pygame.draw.line(win,const.GREY,(self.x+const.D_WIDTH,self.y+const.D_WIDTH),(self.x+const.R_WIDTH,self.y+const.R_WIDTH),3)
        if self.arrow==30:
            pygame.draw.line(win,const.GREY,(self.x+const.R_WIDTH/4,self.y+const.D_WIDTH),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),3)
            pygame.draw.line(win,const.GREY,(self.x,self.y+const.R_WIDTH),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),3)
            pygame.draw.line(win,const.GREY,(self.x+const.D_WIDTH,self.y+3*const.R_WIDTH/4),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),3)
        if self.arrow==31:
            pygame.draw.line(win,const.GREY,(self.x,self.y),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),3)
            pygame.draw.line(win,const.GREY,(self.x+const.D_WIDTH,self.y+const.R_WIDTH/4),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),3)
            pygame.draw.line(win,const.GREY,(self.x+const.R_WIDTH/4,self.y+const.D_WIDTH),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),3)
        if self.arrow==32:
            pygame.draw.line(win,const.GREY,(self.x+const.D_WIDTH,self.y+const.R_WIDTH/4),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),3)
            pygame.draw.line(win,const.GREY,(self.x+3*const.R_WIDTH/4,self.y+const.D_WIDTH),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),3)
            pygame.draw.line(win,const.GREY,(self.x+const.D_WIDTH,self.y+const.D_WIDTH),(self.x+const.R_WIDTH,self.y),3)
        if self.arrow==33:
            pygame.draw.line(win,const.GREY,(self.x+const.D_WIDTH,self.y+3*const.R_WIDTH/4),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),3)
            pygame.draw.line(win,const.GREY,(self.x+3*const.R_WIDTH/4,self.y+const.D_WIDTH),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),3)
            pygame.draw.line(win,const.GREY,(self.x+const.D_WIDTH,self.y+const.D_WIDTH),(self.x+const.R_WIDTH,self.y+const.R_WIDTH),3)
        if self.arrow==34:
            pygame.draw.line(win,const.GREY,(self.x,self.y+const.D_WIDTH),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),3)
            pygame.draw.line(win,const.GREY,(self.x+const.R_WIDTH/4,self.y+const.R_WIDTH/4),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),3)
            pygame.draw.line(win,const.GREY,(self.x+const.R_WIDTH/4,self.y+3*const.R_WIDTH/4),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),3)
        if self.arrow==35:
            pygame.draw.line(win,const.GREY,(self.x+const.D_WIDTH,self.y),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),3)
            pygame.draw.line(win,const.GREY,(self.x+const.R_WIDTH/4,self.y+const.R_WIDTH/4),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),3)
            pygame.draw.line(win,const.GREY,(self.x+const.D_WIDTH,self.y+const.D_WIDTH),(self.x+3*const.R_WIDTH/4,self.y+const.R_WIDTH/4),3)
        if self.arrow==36:
            pygame.draw.line(win,const.GREY,(self.x+const.R_WIDTH,self.y+const.D_WIDTH),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),3)
            pygame.draw.line(win,const.GREY,(self.x+const.D_WIDTH,self.y+const.D_WIDTH),(self.x+3*const.R_WIDTH/4,self.y+const.R_WIDTH/4),3)
            pygame.draw.line(win,const.GREY,(self.x+const.D_WIDTH,self.y+const.D_WIDTH),(self.x+3*const.R_WIDTH/4,self.y+3*const.R_WIDTH/4),3)
        if self.arrow==37:
            pygame.draw.line(win,const.GREY,(self.x+const.D_WIDTH,self.y+const.R_WIDTH),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),3)
            pygame.draw.line(win,const.GREY,(self.x+const.D_WIDTH,self.y+const.D_WIDTH),(self.x+3*const.R_WIDTH/4,self.y+3*const.R_WIDTH/4),3)
            pygame.draw.line(win,const.GREY,(self.x+const.R_WIDTH/4,self.y+3*const.R_WIDTH/4),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),3)
    
    def draw_thermo(self,win):

        if self.thermo==1:
            pygame.draw.circle(win,const.GREY,(self.x+const.D_WIDTH,self.y+const.D_WIDTH),const.D_WIDTH)
        if self.thermo==2:
            pygame.draw.circle(win,const.GREY,(self.x+const.D_WIDTH,self.y+const.D_WIDTH),const.D_WIDTH)
            pygame.draw.line(win,const.GREY,(self.x+const.R_WIDTH,self.y),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),15)
        if self.thermo==3:
            pygame.draw.circle(win,const.GREY,(self.x+const.D_WIDTH,self.y+const.D_WIDTH),const.D_WIDTH)
            pygame.draw.line(win,const.GREY,(self.x+const.R_WIDTH,self.y+const.R_WIDTH),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),15)
        if self.thermo==4:
            pygame.draw.circle(win,const.GREY,(self.x+const.D_WIDTH,self.y+const.D_WIDTH),const.D_WIDTH)
            pygame.draw.line(win,const.GREY,(self.x,self.y+const.R_WIDTH),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),15)
        if self.thermo==5:
            pygame.draw.circle(win,const.GREY,(self.x+const.D_WIDTH,self.y+const.D_WIDTH),const.D_WIDTH)
            pygame.draw.line(win,const.GREY,(self.x,self.y),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),15)
        if self.thermo==6:
            pygame.draw.line(win,const.GREY,(self.x+const.D_WIDTH,self.y),(self.x+const.D_WIDTH,self.y+const.R_WIDTH),15)
        if self.thermo==7:
            pygame.draw.line(win,const.GREY,(self.x,self.y+const.D_WIDTH),(self.x+const.R_WIDTH,self.y+const.D_WIDTH),15)
        if self.thermo==8:
            pygame.draw.line(win,const.GREY,(self.x,self.y),(self.x+const.R_WIDTH,self.y+const.R_WIDTH),15)
        if self.thermo==9:
            pygame.draw.line(win,const.GREY,(self.x,self.y+const.R_WIDTH),(self.x+const.R_WIDTH,self.y),15)
        if self.thermo==10:
            pygame.draw.line(win,const.GREY,(self.x+const.D_WIDTH,self.y),(self.x+const.D_WIDTH,self.y+const.D_WIDTH+7.5),15)
            pygame.draw.line(win,const.GREY,(self.x+const.R_WIDTH,self.y+const.D_WIDTH),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),15)
        if self.thermo==11:
            pygame.draw.line(win,const.GREY,(self.x+const.D_WIDTH,self.y),(self.x+const.D_WIDTH,self.y+const.D_WIDTH+7.5),15)
            pygame.draw.line(win,const.GREY,(self.x,self.y+const.D_WIDTH),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),15)
        if self.thermo==12:
            pygame.draw.line(win,const.GREY,(self.x+const.D_WIDTH,self.y+const.R_WIDTH),(self.x+const.D_WIDTH,self.y+const.D_WIDTH-7.5),15)
            pygame.draw.line(win,const.GREY,(self.x,self.y+const.D_WIDTH),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),15)
        if self.thermo==13:
            pygame.draw.line(win,const.GREY,(self.x+const.D_WIDTH,self.y+const.R_WIDTH),(self.x+const.D_WIDTH,self.y+const.D_WIDTH-7.5),15)
            pygame.draw.line(win,const.GREY,(self.x+const.R_WIDTH,self.y+const.D_WIDTH),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),15)
        if self.thermo==14:
            pygame.draw.line(win,const.GREY,(self.x+const.D_WIDTH,self.y),(self.x+const.D_WIDTH,self.y+const.D_WIDTH+7.5),15)
            pygame.draw.line(win,const.GREY,(self.x,self.y),(self.x+const.D_WIDTH+5.3,self.y+const.D_WIDTH+5.3),15)
        if self.thermo==15:
            pygame.draw.line(win,const.GREY,(self.x+const.D_WIDTH,self.y),(self.x+const.D_WIDTH,self.y+const.D_WIDTH+7.5),15)
            pygame.draw.line(win,const.GREY,(self.x+const.D_WIDTH,self.y+const.D_WIDTH),(self.x+const.R_WIDTH,self.y),15)
        if self.thermo==16:
            pygame.draw.line(win,const.GREY,(self.x+const.D_WIDTH,self.y),(self.x+const.D_WIDTH,self.y+const.D_WIDTH+7.5),15)
            pygame.draw.line(win,const.GREY,(self.x,self.y+const.R_WIDTH),(self.x+const.D_WIDTH+5.3,self.y+const.D_WIDTH-5.3),15)
        if self.thermo==17:
            pygame.draw.line(win,const.GREY,(self.x+const.D_WIDTH,self.y),(self.x+const.D_WIDTH,self.y+const.D_WIDTH+7.5),15)
            pygame.draw.line(win,const.GREY,(self.x+const.D_WIDTH-5.3,self.y+const.D_WIDTH-5.3),(self.x+const.R_WIDTH,self.y+const.R_WIDTH),15)
        if self.thermo==18:
            pygame.draw.line(win,const.GREY,(self.x+const.D_WIDTH,self.y+const.R_WIDTH),(self.x+const.D_WIDTH,self.y+const.D_WIDTH-7.5),15)
            pygame.draw.line(win,const.GREY,(self.x,self.y),(self.x+const.D_WIDTH+5.3,self.y+const.D_WIDTH+5.3),15)
        if self.thermo==19:
            pygame.draw.line(win,const.GREY,(self.x+const.D_WIDTH,self.y+const.R_WIDTH),(self.x+const.D_WIDTH,self.y+const.D_WIDTH-7.5),15)
            pygame.draw.line(win,const.GREY,(self.x+const.D_WIDTH,self.y+const.D_WIDTH),(self.x+const.R_WIDTH,self.y),15)
        if self.thermo==20:
            pygame.draw.line(win,const.GREY,(self.x+const.D_WIDTH,self.y+const.R_WIDTH),(self.x+const.D_WIDTH,self.y+const.D_WIDTH-7.5),15)
            pygame.draw.line(win,const.GREY,(self.x,self.y+const.R_WIDTH),(self.x+const.D_WIDTH+5.3,self.y+const.D_WIDTH-5.3),15)
        if self.thermo==21:
            pygame.draw.line(win,const.GREY,(self.x+const.D_WIDTH,self.y+const.R_WIDTH),(self.x+const.D_WIDTH,self.y+const.D_WIDTH-7.5),15)
            pygame.draw.line(win,const.GREY,(self.x+const.D_WIDTH-5.3,self.y+const.D_WIDTH-5.3),(self.x+const.R_WIDTH,self.y+const.R_WIDTH),15)
        if self.thermo == 22:
            pygame.draw.line(win,const.GREY,(self.x,self.y+const.D_WIDTH),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),15)
            pygame.draw.line(win,const.GREY,(self.x,self.y),(self.x+const.D_WIDTH+5.3,self.y+const.D_WIDTH+5.3),15)
        if self.thermo == 23:
            pygame.draw.line(win,const.GREY,(self.x,self.y+const.D_WIDTH),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),15)
            pygame.draw.line(win,const.GREY,(self.x+const.D_WIDTH,self.y+const.D_WIDTH),(self.x+const.R_WIDTH,self.y),15)
        if self.thermo == 24:
            pygame.draw.line(win,const.GREY,(self.x,self.y+const.D_WIDTH),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),15)
            pygame.draw.line(win,const.GREY,(self.x,self.y+const.R_WIDTH),(self.x+const.D_WIDTH+5.3,self.y+const.D_WIDTH-5.3),15)
        if self.thermo == 25:
            pygame.draw.line(win,const.GREY,(self.x,self.y+const.D_WIDTH),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),15)
            pygame.draw.line(win,const.GREY,(self.x+const.D_WIDTH-5.3,self.y+const.D_WIDTH-5.3),(self.x+const.R_WIDTH,self.y+const.R_WIDTH),15)
        if self.thermo == 26:
            pygame.draw.line(win,const.GREY,(self.x+const.R_WIDTH,self.y+const.D_WIDTH),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),15)
            pygame.draw.line(win,const.GREY,(self.x,self.y),(self.x+const.D_WIDTH+5.3,self.y+const.D_WIDTH+5.3),15)
        if self.thermo == 27:
            pygame.draw.line(win,const.GREY,(self.x+const.R_WIDTH,self.y+const.D_WIDTH),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),15)
            pygame.draw.line(win,const.GREY,(self.x+const.D_WIDTH,self.y+const.D_WIDTH),(self.x+const.R_WIDTH,self.y),15)
        if self.thermo == 28:
            pygame.draw.line(win,const.GREY,(self.x+const.R_WIDTH,self.y+const.D_WIDTH),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),15)
            pygame.draw.line(win,const.GREY,(self.x,self.y+const.R_WIDTH),(self.x+const.D_WIDTH+5.3,self.y+const.D_WIDTH-5.3),15)
        if self.thermo == 29:
            pygame.draw.line(win,const.GREY,(self.x+const.R_WIDTH,self.y+const.D_WIDTH),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),15)
            pygame.draw.line(win,const.GREY,(self.x+const.D_WIDTH-5.3,self.y+const.D_WIDTH-5.3),(self.x+const.R_WIDTH,self.y+const.R_WIDTH),15)
        if self.thermo==30:
            pygame.draw.line(win,const.GREY,(self.x,self.y+const.R_WIDTH),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),15)
            pygame.draw.circle(win,const.GREY,(self.x+const.D_WIDTH,self.y+const.D_WIDTH),7.5*const.si)
        if self.thermo==31:
            pygame.draw.line(win,const.GREY,(self.x,self.y),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),15)
            pygame.draw.circle(win,const.GREY,(self.x+const.D_WIDTH,self.y+const.D_WIDTH),7.5*const.si)
        if self.thermo==32:
            pygame.draw.line(win,const.GREY,(self.x+const.D_WIDTH,self.y+const.D_WIDTH),(self.x+const.R_WIDTH,self.y),15)
            pygame.draw.circle(win,const.GREY,(self.x+const.D_WIDTH,self.y+const.D_WIDTH),7.5*const.si)
        if self.thermo==33:
            pygame.draw.line(win,const.GREY,(self.x+const.D_WIDTH,self.y+const.D_WIDTH),(self.x+const.R_WIDTH,self.y+const.R_WIDTH),15)
            pygame.draw.circle(win,const.GREY,(self.x+const.D_WIDTH,self.y+const.D_WIDTH),7.5*const.si)
        if self.thermo==34:
            pygame.draw.line(win,const.GREY,(self.x,self.y+const.D_WIDTH),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),15)
            pygame.draw.circle(win,const.GREY,(self.x+const.D_WIDTH,self.y+const.D_WIDTH),7.5)
        if self.thermo==35:
            pygame.draw.line(win,const.GREY,(self.x+const.D_WIDTH,self.y),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),15)
            pygame.draw.circle(win,const.GREY,(self.x+const.D_WIDTH,self.y+const.D_WIDTH),7.5)
        if self.thermo==36:
            pygame.draw.line(win,const.GREY,(self.x+const.R_WIDTH,self.y+const.D_WIDTH),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),15)
            pygame.draw.circle(win,const.GREY,(self.x+const.D_WIDTH,self.y+const.D_WIDTH),7.5)    
        if self.thermo==37:
            pygame.draw.line(win,const.GREY,(self.x+const.D_WIDTH,self.y+const.R_WIDTH),(self.x+const.D_WIDTH,self.y+const.D_WIDTH),15)
            pygame.draw.circle(win,const.GREY,(self.x+const.D_WIDTH,self.y+const.D_WIDTH),7.5)


    def clear_arrow(self):
        self.arrow = 0
    def clear_thermo(self):
        self.thermo = 0

    def draw_pencil_marks(self,win):
        font= pygame.font.SysFont('arial',12)
        if 1 in self.pencil_marks:
            digit = font.render('1',True,const.BLACK)
            win.blit(digit,(3+self.x,3+self.y))
        if 2 in self.pencil_marks:
            digit = font.render('2',True,const.BLACK)
            win.blit(digit,(3+self.x+const.R_WIDTH/3,3+self.y))
        if 3 in self.pencil_marks:
            digit = font.render('3',True,const.BLACK)
            win.blit(digit,(3+self.x+2*const.R_WIDTH/3,3+self.y))
        if 4 in self.pencil_marks:
            digit = font.render('4',True,const.BLACK)
            win.blit(digit,(3+self.x,3+self.y+const.R_WIDTH/3))
        if 5 in self.pencil_marks:
            digit = font.render('5',True,const.BLACK)
            win.blit(digit,(3+self.x+const.R_WIDTH/3,3+self.y+const.R_WIDTH/3))
        if 6 in self.pencil_marks:
            digit = font.render('6',True,const.BLACK)
            win.blit(digit,(3+self.x+2*const.R_WIDTH/3,3+self.y+const.R_WIDTH/3))
        if 7 in self.pencil_marks:
            digit = font.render('7',True,const.BLACK)
            win.blit(digit,(3+self.x,3+self.y+2*const.R_WIDTH/3))
        if 8 in self.pencil_marks:
            digit = font.render('8',True,const.BLACK)
            win.blit(digit,(3+self.x+const.R_WIDTH/3,3+self.y+2*const.R_WIDTH/3))
        if 9 in self.pencil_marks:
            digit = font.render('9',True,const.BLACK)
            win.blit(digit,(3+self.x+2*const.R_WIDTH/3,3+self.y+2*const.R_WIDTH/3))
        
    def draw(self,win):
        pygame.draw.rect(win,self.color,(self.x,self.y,self.width,self.width))
        self.draw_arrow(win)
        self.draw_thermo(win)
        if self.number !=0:
            font= pygame.font.SysFont('arial',64)
            digit = font.render(str(self.number),True,self.number_color)
            win.blit(digit,(self.x+const.D_WIDTH/2,self.y))
        if not self.definite and not self.locked:
            self.draw_pencil_marks(win)
        if self.highlighted:
            self.draw_highlight(win)       
    
    def change_cell_to(self,numero):
        self.number = numero
        self.number_color = const.BLUE
        self.locked = True
    
    def remove_all_pencil_marks(self):
        self.pencil_marks.clear()

    def remove_pencil_mark(self,numero):
        self.pencil_marks.remove(numero)
    
    def add_pencil_mark(self,numero):
        if not self.locked and numero not in self.pencil_marks:
            self.pencil_marks.append(numero)
    
    def reset (self):
        self.number = 0
        self.locked = False
        self.definite = False

class On_off_button:
    def __init__(self,width,height,x,y,on_img,off_img):
        self.x=x
        self.y=y
        self.width=width
        self.height= height
        self.on = False
        self.on_img = on_img
        self.off_img = off_img
    def draw(self,win):
        if not self.on:
            pencil = pygame.image.load(self.off_img)
            win.blit(pencil,(self.x,self.y))
        elif self.on:
            pencil = pygame.image.load(self.on_img)
            win.blit(pencil,(self.x,self.y))
        pygame.display.update()
    def turn_on(self):
        self.on = True
    def turn_off(self):
        self.on = False
    def turn_opposite(self):    #if on, turns off / if off, turns on
        self.on = not self.on



class Grilla:
    def __init__(self,width,x,y,filas):
        self.grid = []
        self.x = x
        self.y = y
        self.width = width
        self.filas = filas
        self.main_diags = False
        self.x_sums = False
        self.arrows = False
        self.thermo = False
        self.code = ""
        self.k = 0
    
    def make_grid(self):
        gap = self.width//self.filas
        for i in range(self.filas):
            self.grid.append([])
            for j in range(self.filas) :
                celda = Cell(self.x+i*gap,self.y+j*gap,gap)
                self.grid[i].append(celda)
    
    def get_cell(self,fila,col):
        return self.grid[fila][col]
    
    def find_empty(self):
        for i in range(9):
            for j in range(9):
                if self.grid[i][j].number == 0:
                    return (i,j)
    
    def possible(self,y,x,n):
        for i in range(9):
            if self.grid[y][i].number == n:
                
                return False
        for i in range(9):
            if self.grid[i][x].number == n:
                
                return False
        x_0 = (x//3)*3
        y_0 = (y//3)*3
        for i in range (3):
            for j in range(3):
                if self.grid[y_0+i][x_0+j].number == n:
                    
                    return False
        if self.main_diags:
            if y == x:
                for i in range(9):
                    if self.grid[i][i].number == n:
                        return False
            if y == 8-x:
                    for i in range(9):
                        if self.grid[i][8-i].number == n:
                                return False
        return True

    def solve(self):
        find = self.find_empty()
        if not find:
            return True
        else:
            y , x = find
            for i in range(1,10):
                if self.possible(y,x,i):
                    celda = self.get_cell(y,x)
                    celda.change_cell_to(i)
                    if self.solve():
                        return True

                    celda.change_cell_to(0)
                            
            return False

    def try_solution(self):
        for x in range(9):
            for y in range(9):
                for i in range(9):
                    if (self.grid[y][i].number== self.grid[y][x].number and i != x) or self.grid[y][x].number == 0:
                        return False
                for i in range(9):
                    if (self.grid[i][x].number == self.grid[y][x].number and i != y) or self.grid[y][x].number == 0:
                        return False
                x_0 = (x//3)*3
                y_0 = (y//3)*3
                for i in range(3):
                    for j in range(3):
                        if (self.grid[y_0+i][x_0+j].number == self.grid[y][x].number and (y_0+i != y or x_0+j !=x)) or self.grid[y][x].number == 0:
                            return False
        if self.main_diags :
            for x in range(9):
                for i in range(9):
                    if (self.grid[x][x].number == self.grid[i][i].number and x != i) or self.grid[x][x].number == 0:
                        return False
            for x in range(9):
                for i in range(9):
                    if (self.grid[x][8-x].number == self.grid[i][8-i].number and x != i) or self.grid[x][x].number == 0:
                        return False
        return True



    def randomize_grid(self):
        for i in range(9):
            for j in range(9):
                celda = self.get_cell(i,j)
                celda.clear_arrow()
                celda.clear_thermo()
        self.k += 1
        if self.k > 3:
            self.k = (self.k%3)

        if not self.main_diags and not self.x_sums and not self.arrows and not self.thermo: 
            new_grid = const.grid_dict_aaaa[self.k]
            self.code = str(self.k) + "aaaa"
        
        if self. main_diags and not self.x_sums and not self.arrows and not self.thermo:
            new_grid = const.grid_dict_baaa[self.k]
            self.code = str(self.k) + "baaa"
        
        if self.x_sums and not self.main_diags and not self.arrows and not self.thermo:
            new_grid = const.grid_dict_abaa[self.k]
            self.code = str(self.k) + "abaa"
        if self.arrows and not self.main_diags and not self.x_sums and not self.thermo:
            new_grid = const.grid_dict_aaba[self.k]
            arrow_grid = const.arrow_dict[self.k]
            self.code = str(self.k) + "aaba"
            for i in range(self.filas):
                for j in range(self.filas):
                    self.grid[j][i].arrow = arrow_grid[i][j]
        if self.thermo and not self.main_diags and not self.x_sums and not self.arrows:
            new_grid = const.grid_dict_aaab[self.k]
            thermo_grid = const.thermo_dict[self.k]
            self.code = str(self.k) + "aaab"
            for i in range(self.filas):
                for j in range(self.filas):
                    self.grid[j][i].thermo = thermo_grid[i][j]

        for i in range(self.filas):
            for j in range(self.filas):
                self.grid[j][i].number = new_grid[i][j]
                if new_grid[i][j] != 0 :
                    self.grid[j][i].definite = True
    
    def draw_main_diags(self,win):
        pygame.draw.line(win,const.LIGHT_BLUE,(self.x,self.y),(self.x+self.width,self.y+self.width),3)
        pygame.draw.line(win,const.LIGHT_BLUE,(self.x,self.y+self.width),(self.x+self.width,self.y),3)

    def draw_x_sums(self,win):
        font = pygame.font.SysFont('arial',30)
        if self.code == "1abaa":
            pygame.draw.rect(win,const.GREY,(0,0,const.WIDTH,const.WIDTH))

            number = font.render("8",True,const.BLACK)
            win.blit(number,(const.R_WIDTH/2,2*const.R_WIDTH+const.R_WIDTH/4))
            win.blit(number,(10*const.R_WIDTH+const.R_WIDTH/4,2*const.R_WIDTH+const.R_WIDTH/4))

            number = font.render("17",True,const.BLACK)
            win.blit(number,(const.R_WIDTH/2,4*const.R_WIDTH+const.R_WIDTH/4))
            win.blit(number,(10*const.R_WIDTH+const.R_WIDTH/4,4*const.R_WIDTH+const.R_WIDTH/4))

            number = font.render("30",True,const.BLACK)
            win.blit(number,(const.R_WIDTH/2,6*const.R_WIDTH+const.R_WIDTH/4))
            win.blit(number,(10*const.R_WIDTH+const.R_WIDTH/4,6*const.R_WIDTH+const.R_WIDTH/4))

            number = font.render("28",True,const.BLACK)
            win.blit(number,(const.R_WIDTH/2,8*const.R_WIDTH+const.R_WIDTH/4))
            win.blit(number,(10*const.R_WIDTH+const.R_WIDTH/4,8*const.R_WIDTH+const.R_WIDTH/4))

            number = font.render("27",True,const.BLACK)
            win.blit(number,(2*const.R_WIDTH+const.R_WIDTH/4,10*const.R_WIDTH))
            win.blit(number,(2*const.R_WIDTH+const.R_WIDTH/4,const.R_WIDTH/2))

            number = font.render("11",True,const.BLACK)
            win.blit(number,(4*const.R_WIDTH+const.R_WIDTH/4,10*const.R_WIDTH))
            win.blit(number,(4*const.R_WIDTH+const.R_WIDTH/4,const.R_WIDTH/2))

            number = font.render("21",True,const.BLACK)
            win.blit(number,(6*const.R_WIDTH+const.R_WIDTH/4,const.R_WIDTH/2))

            number = font.render("16",True,const.BLACK)
            win.blit(number,(7*const.R_WIDTH+const.R_WIDTH/4,10*const.R_WIDTH))  
            win.blit(number,(7*const.R_WIDTH+const.R_WIDTH/4,const.R_WIDTH/2))
        if self.code == "2abaa":
            pygame.draw.rect(win,const.GREY,(0,0,const.WIDTH,const.WIDTH))
            number = font.render("18",True,const.BLACK)
            win.blit(number,(4*const.R_WIDTH+const.R_WIDTH/4,const.R_WIDTH/2))
            win.blit(number,(6*const.R_WIDTH+const.R_WIDTH/4,const.R_WIDTH/2))
            number = font.render("20",True,const.BLACK)
            win.blit(number,(1*const.R_WIDTH+const.R_WIDTH/4,const.R_WIDTH/2))
            number = font.render("33",True,const.BLACK)
            win.blit(number,(2*const.R_WIDTH+const.R_WIDTH/4,const.R_WIDTH/2))
            number = font.render("8",True,const.BLACK)
            win.blit(number,(8*const.R_WIDTH+const.R_WIDTH/4,const.R_WIDTH/2))
            number = font.render("39",True,const.BLACK)
            win.blit(number,(9*const.R_WIDTH+const.R_WIDTH/4,const.R_WIDTH/2))
            win.blit(number,(const.R_WIDTH/2,4*const.R_WIDTH+const.R_WIDTH/4))
            number = font.render("36",True,const.BLACK)
            win.blit(number,(const.R_WIDTH/2,6*const.R_WIDTH+const.R_WIDTH/4))
            number = font.render("31",True,const.BLACK)
            win.blit(number,(10*const.R_WIDTH+const.R_WIDTH/4,3*const.R_WIDTH+const.R_WIDTH/4))
            number = font.render("15",True,const.BLACK)
            win.blit(number,(10*const.R_WIDTH+const.R_WIDTH/4,7*const.R_WIDTH+const.R_WIDTH/4))
            number = font.render("25",True,const.BLACK)
            win.blit(number,(1*const.R_WIDTH+const.R_WIDTH/4,10*const.R_WIDTH))
            win.blit(number,(9*const.R_WIDTH+const.R_WIDTH/4,10*const.R_WIDTH))
            number = font.render("5",True,const.BLACK)
            win.blit(number,(2*const.R_WIDTH+const.R_WIDTH/4,10*const.R_WIDTH))
            number = font.render("19",True,const.BLACK)
            win.blit(number,(4*const.R_WIDTH+const.R_WIDTH/4,10*const.R_WIDTH))
            number = font.render("17",True,const.BLACK)
            win.blit(number,(6*const.R_WIDTH+const.R_WIDTH/4,10*const.R_WIDTH))
            number = font.render("37",True,const.BLACK)
            win.blit(number,(8*const.R_WIDTH+const.R_WIDTH/4,10*const.R_WIDTH))
        if self.code == "3abaa":
            pygame.draw.rect(win,const.GREY,(0,0,const.WIDTH,const.WIDTH))
            number = font.render("28",True,const.BLACK)
            #Izq
            win.blit(number,(const.R_WIDTH/2,const.R_WIDTH+const.R_WIDTH/4))
            win.blit(number,(const.R_WIDTH/2,3*const.R_WIDTH+const.R_WIDTH/4))
            win.blit(number,(const.R_WIDTH/2,4*const.R_WIDTH+const.R_WIDTH/4))
            win.blit(number,(const.R_WIDTH/2,7*const.R_WIDTH+const.R_WIDTH/4))
            #Abajo
            win.blit(number,(3*const.R_WIDTH+const.R_WIDTH/4,10*const.R_WIDTH))
            win.blit(number,(4*const.R_WIDTH+const.R_WIDTH/4,10*const.R_WIDTH))
            #Derecha
            win.blit(number,(10*const.R_WIDTH+const.R_WIDTH/4,const.R_WIDTH+const.R_WIDTH/4))
            win.blit(number,(10*const.R_WIDTH+const.R_WIDTH/4,4*const.R_WIDTH+const.R_WIDTH/4))
            win.blit(number,(10*const.R_WIDTH+const.R_WIDTH/4,5*const.R_WIDTH+const.R_WIDTH/4))
            win.blit(number,(10*const.R_WIDTH+const.R_WIDTH/4,8*const.R_WIDTH+const.R_WIDTH/4))
            #Arriba
            win.blit(number,(7*const.R_WIDTH+const.R_WIDTH/4,const.R_WIDTH/2))
        else:
            pass
        

    
    def draw_grid(self,win):
        for fila in self.grid:
            for node in fila:
                node.draw(win)
        gap  = self.width//self.filas
        for i in range(self.filas+1):
            if i%3 == 0:
                pygame.draw.line(win,const.BLACK,(self.x,self.y+i*gap),(self.x+self.width,self.y+i*gap),3)
            else:
                pygame.draw.line(win,const.BLACK,(self.x,self.y+i*gap),(self.x+self.width,self.y+i*gap))
        for j in range(self.filas+1):
            if j%3 == 0:
                pygame.draw.line(win,const.BLACK,(self.x+j*gap,self.y),(self.x+j*gap,self.y+self.width),3)
            else:
                pygame.draw.line(win,const.BLACK,(self.x+j*gap,self.y),(self.x+j*gap,self.y+self.width))
        
        if self.main_diags:
            self.draw_main_diags(win)

    def unhighlight_all(self):
        for i in range(self.filas):
            for j in range(self.filas):
                self.grid[i][j].highlighted = False
    def reset_grid(self):
        self.grid.clear()
        self.make_grid()
    def toogle_main_diag(self):
        self.main_diags = not self.main_diags
    def toogle_x_sums(self):
        self.x_sums = not self.x_sums
    def toogle_arrows(self):
        self.arrows = not self.arrows
    def toogle_thermo(self):
        self.thermo = not self.thermo

class Push_button:
    def __init__(self,x,y,width,height,unpush_img,push_img):
        self.x = x
        self.y = y
        self.width = width
        self.height= height
        self.clicked = False
        self.push_img= push_img
        self.unpush_img = unpush_img
    
    def draw(self,win):
        if self.clicked:
            img = pygame.image.load(self.push_img)
            win.blit(img,(self.x,self.y))
        else:
            img = pygame.image.load(self.unpush_img)
            win.blit(img,(self.x,self.y))
        pygame.display.update()
    def click(self,win):
        self.clicked = True
        self.draw(win)
        self.clicked = False
