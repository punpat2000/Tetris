# Prog-11: Tetris
# Fill in your ID & Name
# ...
# Declare that you do this by yourself

import pygame
import copy
import random

def make_shape(): 
    shape = [[[1,1,1],[1,0,0]], [[2,2,2],[0,0,2]], [[3,3,3],[0,3,0]], [[4,4,4,4]], [[5,5,0],[0,5,5]], [[6,0],[6,6],[0,6]], [[7,7],[7,7]]]
    return shape[random.randrange(len(shape))]

def show_text(x,y,size,text,screen):
    text_surface = pygame.font.Font(pygame.font.match_font('arial'), size).render(text, True, (255,255,255))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)

def top(board):
    row = min([i for i in range(len(board)) if board[i]!=[0]*len(board[0])],default=0)-1
    return 60*(2+(row-1)//6) if row>6 else 120

def scoring(board):
    count = len([i for i in board if 0 not in i])
    return 50*count*(count-1)*max(1,(count-2)) if count>1 else 40*count

def pgame():
    width,height,FPS = 480,720,60
    all_color = [(255,128,0),(0,0,255),(255,0,255),(0,255,255),(255,0,0),(0,255,0),(255,255,0)]
    board = [[0]*10 for i in range(23)]
    shape = make_shape()
    score,time,end,column = 0,0,0,0
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((width,height))
    pygame.display.set_caption("ComProg-10: Tetris")

    while end == 0:
        screen.fill((0,0,0))
        time_cap = top(board)
        clock.tick(FPS)
        frame = [board]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    frame = animate_drop(shape,board,column) #multiple frames
                    if len(frame)!=0:
                        score += scoring(frame[-1])
                        frame = frame + animate_clear(frame[-1])
                        board = frame[-1]
                        shape = make_shape()
                        column,time = 0,0
                    else:
                        end = 1
                elif event.key == pygame.K_LEFT:
                    column = column-1 if column>0 else column
                elif event.key == pygame.K_RIGHT:
                    column = column+1 if column<len(board[0])-len(shape[0]) else column
                elif event.key == pygame.K_z:
                    shape = rotateL(shape)
                    column = min(column,len(board[0])-len(shape[0]))
                elif event.key == pygame.K_x:
                    shape = rotateR(shape)
                    column = min(column,len(board[0])-len(shape[0]))
        time+=1
        if time >= time_cap:
            frame = animate_drop(shape,board,column)
            if len(frame)!=0:
                score += scoring(frame[-1])
                frame = frame + animate_clear(frame[-1])
                board = frame[-1]
                shape = make_shape()
                column,time = 0,0
            else:
                end = 1
        for i in frame:
            screen.fill((0,0,0))
            clock.tick(FPS)
            board_row, board_column = len(i), len(i[0])
            shape_row, shape_column = len(shape), len(shape[0])
            for j in range(shape_row):
                for k in range(shape_column):
                    if shape[j][k]!=0:
                        pygame.draw.rect(screen,all_color[shape[j][k]-1],[30+column*24+k*24,20+j*24,20,20],0)
            for j in range(board_row):
                for k in range(board_column):
                    if i[j][k]!=0:
                        pygame.draw.rect(screen,all_color[i[j][k]-1],[30+k*24,124+j*24,20,20],0)
            for i in range(board_column+1):
                if i >= column and i <= column + shape_column:
                    pygame.draw.line(screen,(255,255,255),[28+i*24,672],[28+i*24,116],3)
                else:
                    pygame.draw.line(screen,(128,128,128),[28+i*24,672],[28+i*24,116])
            show_text(380,120,50,"TIME",screen)
            show_text(380,500,50,"SCORE",screen)
            show_text(240,685,15,"Z/X for rotating      Right/Left Arrow Key for moving      Spacebar for dropping",screen)
            pygame.display.flip()
        show_text(380,180,150,str(time//60)+"."+str((time//6)%10),screen)
        show_text(380,550,75,str(score),screen)
        pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.quit()
                    return 
        screen.fill((0,0,0))
        show_text(240,150,50,"TOTAL SCORE",screen)
        show_text(240,250,250,str(score),screen)  
        show_text(240,550,25,"press enter to exit the game",screen) 
        pygame.display.flip()

#-------------------------------------------------------

def rotateR(shape):
    new_shape = []
    for i in range(len(shape[0])):
        new_row = []
        for j in range(len(shape)-1,-1,-1):
            new_row.append(shape[j][i])
        new_shape.append(new_row)
    return  new_shape

def rotateL(shape):
    new_shape = []
    for i in range(len(shape[0])-1,-1,-1):
        new_row = []
        for j in range(len(shape)):
            new_row.append(shape[j][i])
        new_shape.append(new_row)
    return  new_shape

def animate_drop(shape, board, c):
    frames: list = []
    if c not in range(len(board)):
        return frames
    done: bool = False
    for i in range(1, len(board)):
        for j in range(len(shape)):
            if i-j < 0:
                    break
            for k in range(len(shape[j])):  
                if shape[len(shape)-1-j][k]!=0 and board[i-j][k+c]!=0:
                    done = True
                    break
            if done:
                break
        if done:
            break
        frame = copy.deepcopy(board) #a copy of unmodified board
        for j in range(len(shape) - 1, -1, -1):
            token_row = shape[j]
            row_num = i - (len(shape) - 1 - j)
            if row_num < 0:
                break
            start_i = end_i = 0
            for k in range(len(token_row)):
                if token_row[k] != 0:
                    start_i = k
                    break
            for k in range(len(token_row)):
                if token_row[-k-1] != 0:
                    end_i = k
                    break
            frame[row_num][c+start_i:c+len(token_row)-end_i] = token_row[start_i:len(token_row)-end_i]
        frames.append(frame)
    return frames

def animate_clear(board):
    frames: list = list()
    temp = copy.deepcopy(board)
    ALL_ZEROS, OCCUPIED = True, False
    status: list[bool] = [OCCUPIED]*len(board) #keep track of all zeros rows, so that there is no need to recheck again. (perfomance wise)
    detected: bool = False
    for i in range(len(board)):
        filled = all(v != 0 for v in temp[i])
        if filled:
            temp[i] = [0]*len(temp[i]) #return [0, 0, 0, 0, 0,...]
            status[i] = detected = ALL_ZEROS
            continue
        status[i] = all(v == 0 for v in temp[i])
    if not detected:
        return frames
    frames.append(temp)
    final = status[:]
    final.sort()
    final.reverse()
    while final != status:
        end_row = status.index(OCCUPIED)
        start_row = len(status) - 1 - status[::-1].index(ALL_ZEROS) - 1
        frame = copy.deepcopy(frames[-1])
        for i in range(start_row, end_row - 1, -1): #start from bottom to top
            if status[i+1] and not status[i]:
                frame[i], frame[i+1] = frame[i+1], frame[i]
                status[i], status[i+1] = ALL_ZEROS, OCCUPIED
                i -= 1
        frames.append(frame)
    return frames
    

    

#----------------------------------------------        

pgame()