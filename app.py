import pygame
import math
from queue import PriorityQueue
from random import randint, randrange
import classes as cl
import constants as const

pygame.init()

#Window
PANTALLA =  pygame.display.set_mode((const.WIDTH,const.WIDTH))
pygame.display.set_caption("Sudoku_solver")

clock = pygame.time.Clock()

#Dibujar botones
def draw_buttons(win):
    
    #Sudoku
    digits_x = const.S_WIDTH+2*const.R_WIDTH
    digits_y = const.R_WIDTH
    pygame.draw.rect(win,const.BLACK,(digits_x,digits_y,2*const.R_WIDTH,const.R_WIDTH))
    font= pygame.font.SysFont('arial',52)
    digits = font.render("Sudoku",True,const.WHITE)
    win.blit(digits,(digits_x,digits_y))

    
    #Colores
    colors_x = const.R_WIDTH
    colors_y = const.S_WIDTH+2*const.R_WIDTH
    pygame.draw.rect(win,const.BLACK,(colors_x,colors_y,2*const.R_WIDTH,const.R_WIDTH))
    font= pygame.font.SysFont('arial',64)
    colors = font.render("Colors",True,const.WHITE)
    win.blit(colors,(colors_x,colors_y))
    k=0
    font= pygame.font.SysFont('arial',32)
    for i in range(7,12,2):
        for j in range (1,6,2):
            color_x= i*const.D_WIDTH-const.D_WIDTH/2
            color_y = const.S_WIDTH+j*const.D_WIDTH-const.D_WIDTH/2 +100
            pygame.draw.rect(win,const.colors_dict[k],(color_x,color_y,const.D_WIDTH,const.D_WIDTH))  
            k+=1


def draw(win):
    draw_buttons(win)
    pygame.display.update()

def get_clicked_pos(pos,grilla):
    gap = grilla.width // grilla.filas
    x,y = pos
    x -= grilla.x
    y -= grilla.y
    fila = x // gap
    col = y // gap
    return fila,col


def draw_background(win):
    pygame.draw.rect(win,const.GREY,(0,0,const.WIDTH,const.WIDTH))

def main(win,width):
    run = True

    grilla = cl.Grilla(width,75,75,9)
    grilla.make_grid()
    grilla.randomize_grid()
    celda = None

    main_diag_x = const.S_WIDTH+2*const.R_WIDTH
    main_diag_y= 3*const.R_WIDTH
    main_diag_width= 2*const.R_WIDTH
    main_diag_height= const.R_WIDTH
    main_diag_b = cl.On_off_button(main_diag_width,main_diag_height,main_diag_x,main_diag_y,"./Images/main_diag_on.jpg","./Images/main_diag_off.jpg")
    

    x_sums_x = const.S_WIDTH+2*const.R_WIDTH
    x_sums_y= 5*const.R_WIDTH
    x_sums_width= 2*const.R_WIDTH
    x_sums_height= const.R_WIDTH
    x_sums_b = cl.On_off_button(x_sums_width,x_sums_height,x_sums_x,x_sums_y,"./Images/x_sums_on.jpg","./Images/x_sums_off.jpg")

    arrows_x = const.S_WIDTH+2*const.R_WIDTH
    arrows_y= 7*const.R_WIDTH
    arrows_width= 2*const.R_WIDTH
    arrows_height= const.R_WIDTH
    arrows_b = cl.On_off_button(arrows_width,arrows_height,arrows_x,arrows_y,"./Images/arrows_on.jpg","./Images/arrows_off.jpg")

    thermo_x = const.S_WIDTH+2*const.R_WIDTH
    thermo_y= 9*const.R_WIDTH
    thermo_width= 2*const.R_WIDTH
    thermo_height= const.R_WIDTH
    thermo_b = cl.On_off_button(thermo_width,thermo_height,thermo_x,thermo_y,"./Images/thermos_on.jpg","./Images/thermos_off.jpg")

    pencil_x = const.S_WIDTH+2*const.R_WIDTH
    pencil_y = 5*const.D_WIDTH-const.D_WIDTH/2
    pencil_width = 38
    pencil_height= 38
    pencil_b = cl.On_off_button(pencil_width,pencil_height,pencil_x,pencil_y,"./Images/pencil.jpg","./Images/pen.jpg")

    reset_x = 0
    reset_y = const.WIDTH - 50
    reset_width = 50
    reset_height = 50
    reset_b = cl.Push_button(reset_x,reset_y,reset_width,reset_height,"./Images/reset.jpg","./Images/reset_click.jpg")

    colors_f= [0,0,0,0,0,0,0,0,0]


    draw_background(win)   
    while run: 
        clock.tick(60)
        draw(win)
        grilla.draw_grid(win)
        pencil_b.draw(win)
        reset_b.draw(win)
        main_diag_b.draw(win)
        x_sums_b.draw(win)
        arrows_b.draw(win)
        thermo_b.draw(win)
        pygame.display.update()
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                run = False
            
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                
                if grilla.x <pos[0]<grilla.x+const.S_WIDTH and grilla.y < pos[1]<grilla.y+const.S_WIDTH:
                    grilla.unhighlight_all()
                    fila,col = get_clicked_pos(pos,grilla)
                    fila = int(fila)
                    col = int(col)
                    celda = grilla.get_cell(fila,col)
                    celda.highlighted = True
                    for i in range(9):
                        if colors_f[i] == 1:
                            celda.color = const.colors_dict[i]
                    
                elif pencil_x < pos[0]  < pencil_x +pencil_width and pencil_y < pos[1] < pencil_y+pencil_height :
                    pencil_b.turn_opposite()
                
                elif reset_x < pos[0] < reset_x + reset_width and reset_y < pos[1] < reset_y + reset_height:                   
                    reset_b.click(win)
                    grilla.unhighlight_all()
                    grilla.reset_grid()
                    grilla.randomize_grid()
                    for i in range(9):
                        colors_f[i] = 0
                    pygame.draw.rect(win,const.GREY,(0,0,const.WIDTH,const.WIDTH))
                    if grilla.x_sums:
                        grilla.draw_x_sums(win)
                
                elif main_diag_x < pos[0] < main_diag_x + main_diag_width and main_diag_y < pos[1] < main_diag_y + main_diag_height:
                    main_diag_b.turn_opposite()       
                    if grilla.x_sums:
                        grilla.x_sums= False
                        x_sums_b.turn_off()
                    if grilla.arrows:
                        grilla.arrows = False
                        arrows_b.turn_off()
                    if grilla.thermo:
                        grilla.thermo = False
                        thermo_b.turn_off()
                    grilla.toogle_main_diag()
                
                elif arrows_x < pos[0] < arrows_x + arrows_width and arrows_y < pos[1] < arrows_y + arrows_height:
                    arrows_b.turn_opposite()       
                    if grilla.x_sums:
                        grilla.x_sums= False
                        x_sums_b.turn_off()
                    if grilla.main_diags:
                        grilla.main_diags = False
                        main_diag_b.turn_off()
                    if grilla.thermo:
                        grilla.thermo = False
                        thermo_b.turn_off()
                    grilla.toogle_arrows()

                elif x_sums_x < pos[0] < x_sums_x + x_sums_width and x_sums_y < pos[1] < x_sums_y + x_sums_height:
                    x_sums_b.turn_opposite()
                    if grilla.main_diags:
                        grilla.main_diags = False
                        main_diag_b.turn_off()
                    if grilla.arrows:
                        grilla.arrows = False
                        arrows_b.turn_off()
                    if grilla.thermo:
                        grilla.thermo = False
                        thermo_b.turn_off()
                    grilla.toogle_x_sums()
                
                elif thermo_x < pos[0] < thermo_x + thermo_width and thermo_y < pos[1] < thermo_y + thermo_height:
                    thermo_b.turn_opposite()
                    if grilla.main_diags:
                        grilla.main_diags = False
                        main_diag_b.turn_off()
                    if grilla.arrows:
                        grilla.arrows = False
                        arrows_b.turn_off()
                    if grilla.x_sums:
                        grilla.x_sums = False
                        x_sums_b.turn_off()
                    grilla.toogle_thermo()

                
                elif 7*const.D_WIDTH-const.D_WIDTH/2 <pos[0]< 7*const.D_WIDTH+const.D_WIDTH/2 and const.S_WIDTH+const.D_WIDTH-const.D_WIDTH/2 +100< pos[1] < const.S_WIDTH+const.D_WIDTH+const.D_WIDTH/2+100:
                    for i in range(9):
                        colors_f[i] = 0
                    colors_f[0] = 1
                elif 7*const.D_WIDTH-const.D_WIDTH/2 <pos[0]< 7*const.D_WIDTH+const.D_WIDTH/2 and const.S_WIDTH+3*const.D_WIDTH-const.D_WIDTH/2 +100< pos[1] < const.S_WIDTH+3*const.D_WIDTH+const.D_WIDTH/2+100:
                    for i in range(9):
                        colors_f[i] = 0
                    colors_f[1] = 1
                elif 7*const.D_WIDTH-const.D_WIDTH/2 <pos[0]< 7*const.D_WIDTH+const.D_WIDTH/2 and const.S_WIDTH+5*const.D_WIDTH-const.D_WIDTH/2 +100< pos[1] < const.S_WIDTH+5*const.D_WIDTH+const.D_WIDTH/2+100:
                    for i in range(9):
                        colors_f[i] = 0
                    colors_f[2] = 1
                elif 9*const.D_WIDTH-const.D_WIDTH/2 <pos[0]< 9*const.D_WIDTH+const.D_WIDTH/2 and const.S_WIDTH+const.D_WIDTH-const.D_WIDTH/2 +100< pos[1] < const.S_WIDTH+const.D_WIDTH+const.D_WIDTH/2+100:
                    for i in range(9):
                        colors_f[i] = 0
                    colors_f[3] = 1
                elif 9*const.D_WIDTH-const.D_WIDTH/2 <pos[0]< 9*const.D_WIDTH+const.D_WIDTH/2 and const.S_WIDTH+3*const.D_WIDTH-const.D_WIDTH/2 +100< pos[1] < const.S_WIDTH+3*const.D_WIDTH+const.D_WIDTH/2+100:
                    for i in range(9):
                        colors_f[i] = 0
                    colors_f[4] = 1
                elif 9*const.D_WIDTH-const.D_WIDTH/2 <pos[0]< 9*const.D_WIDTH+const.D_WIDTH/2 and const.S_WIDTH+5*const.D_WIDTH-const.D_WIDTH/2 +100< pos[1] < const.S_WIDTH+5*const.D_WIDTH+const.D_WIDTH/2+100:
                    for i in range(9):
                        colors_f[i] = 0
                    colors_f[5] = 1
                elif 11*const.D_WIDTH-const.D_WIDTH/2 <pos[0]< 11*const.D_WIDTH+const.D_WIDTH/2 and const.S_WIDTH+const.D_WIDTH-const.D_WIDTH/2 +100< pos[1] < const.S_WIDTH+const.D_WIDTH+const.D_WIDTH/2+100:
                    for i in range(9):
                        colors_f[i] = 0
                    colors_f[6] = 1
                elif 11*const.D_WIDTH-const.D_WIDTH/2 <pos[0]< 11*const.D_WIDTH+const.D_WIDTH/2 and const.S_WIDTH+3*const.D_WIDTH-const.D_WIDTH/2 +100< pos[1] < const.S_WIDTH+3*const.D_WIDTH+const.D_WIDTH/2+100:
                    for i in range(9):
                        colors_f[i] = 0
                    colors_f[7] = 1
                elif 11*const.D_WIDTH-const.D_WIDTH/2 <pos[0]< 11*const.D_WIDTH+const.D_WIDTH/2 and const.S_WIDTH+5*const.D_WIDTH-const.D_WIDTH/2 +100< pos[1] < const.S_WIDTH+5*const.D_WIDTH+const.D_WIDTH/2+100:
                    for i in range(9):
                        colors_f[i] = 0
                    colors_f[8] = 1
                else:
                    grilla.unhighlight_all()
                    celda = None
                    
                for i in range(9):
                    if colors_f[i] == 1:
                        pygame.draw.circle(win,const.colors_dict[i],(50,500), 70)

                
                
            if pygame.mouse.get_pressed()[2]:
                for i in range(9):
                    colors_f[i] = 0


            if event.type == pygame.KEYDOWN and not pencil_b.on:
                if celda and not celda.definite:
                    if event.key == pygame.K_1:
                        celda.change_cell_to(1)
                    if event.key == pygame.K_2:
                        celda.change_cell_to(2)
                    if event.key == pygame.K_3:
                        celda.change_cell_to(3)
                    if event.key == pygame.K_4:
                        celda.change_cell_to(4)
                    if event.key == pygame.K_5:
                        celda.change_cell_to(5)
                    if event.key == pygame.K_6:
                        celda.change_cell_to(6)
                    if event.key == pygame.K_7:
                        celda.change_cell_to(7)
                    if event.key == pygame.K_8:
                        celda.change_cell_to(8)
                    if event.key == pygame.K_0:
                        celda.change_cell_to(9)
            elif event.type == pygame.KEYDOWN and pencil_b.on:
                if celda and not celda.definite and not celda.locked:
                    if event.key == pygame.K_1:
                        if 1 in celda.pencil_marks:
                            celda.remove_pencil_mark(1)
                        else:
                            celda.add_pencil_mark(1)
                    if event.key == pygame.K_2:
                        if 2 in celda.pencil_marks:
                            celda.remove_pencil_mark(2)
                        else:
                            celda.add_pencil_mark(2)
                    if event.key == pygame.K_3:
                        if 3 in celda.pencil_marks:
                            celda.remove_pencil_mark(3)
                        else:
                            celda.add_pencil_mark(3)
                    if event.key == pygame.K_4:
                        if 4 in celda.pencil_marks:
                            celda.remove_pencil_mark(4)
                        else:
                            celda.add_pencil_mark(4)
                    if event.key == pygame.K_5:
                        if 5 in celda.pencil_marks:
                            celda.remove_pencil_mark(5)
                        else:
                            celda.add_pencil_mark(5)
                    if event.key == pygame.K_6:
                        if 6 in celda.pencil_marks:
                            celda.remove_pencil_mark(6)
                        else:
                            celda.add_pencil_mark(6)
                    if event.key == pygame.K_7:
                        if 7 in celda.pencil_marks:
                            celda.remove_pencil_mark(7)
                        else:
                            celda.add_pencil_mark(7)
                    if event.key == pygame.K_8:
                        if 8 in celda.pencil_marks:
                            celda.remove_pencil_mark(8)
                        else:
                            celda.add_pencil_mark(8)
                    if event.key == pygame.K_0:
                        if 9 in celda.pencil_marks:
                            celda.remove_pencil_mark(9)
                        else:
                            celda.add_pencil_mark(9)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if celda:
                        celda.reset()
                if event.key==pygame.K_v:
                    pencil_b.turn_opposite()
                if event.key == pygame.K_j:
                    grilla.solve()
                if event.key == pygame.K_o:
                    correct = grilla.try_solution()
                    if correct:
                        print("correct")
                    else:
                        print("no")
                if event.key == pygame.K_b:
                    celda.color = const.WHITE
                if event.key == pygame.K_r:
                    reset_b.click(win)
                    grilla.unhighlight_all()
                    grilla.reset_grid()
                    grilla.randomize_grid()
                    for i in range(9):
                        colors_f[i] = 0
                    pygame.draw.rect(win,const.GREY,(0,0,const.WIDTH,const.WIDTH))
                    if grilla.x_sums:
                        grilla.draw_x_sums(win)

    pygame.quit()

main(PANTALLA,const.S_WIDTH)