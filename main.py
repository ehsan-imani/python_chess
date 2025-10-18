import pygame
from pieces import *
import math
from game import *
from status import *
import os
import tkinter as tk

#create board background
chess_board = [[None for _ in range(8)]  for _ in range(8)] 
def initialize_board():
    board = [[None for _ in range(8)] for _ in range(8)]
    for row in range(8):
        for col in range(8):
            if (row + col) % 2 == 0:
                board[row][col] = 'white'
            else:
                board[row][col] = 'black'
    return board

#get monior screen small side
root =tk.Tk()
min_screen_size=root.winfo_screenwidth() if root.winfo_screenwidth()<root.winfo_screenheight() else root.winfo_screenheight()
root.destroy()

#create pygame window
pygame.init()
screen = pygame.display.set_mode((min_screen_size/10*8.5, min_screen_size/10*8.5))
pygame.display.set_caption("Chess Game")

home_size= min_screen_size/10

#draw chess main board
def draw_board(screen, board,chess,selected,av_homes):
    for row in range(8):
        for col in range(8):
            color = (250, 228, 178) if board[row][col] == 'white' else (93, 53, 43)
            selected_color=(255, 126, 54)
            pygame.draw.rect(screen, color, (col * home_size+home_size/4, row * home_size+home_size/4, home_size, home_size))
            if(selected==(row,col)):
                pygame.draw.circle(screen, selected_color, (col*home_size+home_size/4+(home_size/2),row*home_size+home_size/4+(home_size/2)),home_size/2-1,5)
            elif((row,col) in av_homes):
                pygame.draw.circle(screen, selected_color, (col*home_size+home_size/4+(home_size/2),row*home_size+home_size/4+(home_size/2)),home_size/8)
            if(chess[row][col]==None):continue
            if((row,col)==game.check_home):
                pygame.draw.rect(screen, (225,100,100), (col * home_size+home_size/4, row * home_size+home_size/4, home_size,home_size))
            img=chess[row][col].img
            #draw pieces
            screen.blit(img, (col*home_size+home_size/4+(home_size-50)/2, row*home_size+home_size/4+(home_size-50)/2))
    Font_size=13
    my_font = pygame.font.SysFont('Comic Sans MS', Font_size)
    #draw left side numbers
    for i in range(8):
        color = (250, 228, 178) if board[0][i] == 'white' else (93, 53, 43)
        pygame.draw.rect(screen,color,(0,i*home_size+home_size/4,home_size/4,home_size))
        text_surface = my_font.render(str(8-i), False, (255,255,255) if i%2==1 else (0,0,0))
        screen.blit(text_surface,(home_size/16,i*home_size+home_size/2+Font_size))
    #draw right side numbers
    for i in range(8):
        color = (250, 228, 178) if board[7][i] == 'white' else (93, 53, 43)
        pygame.draw.rect(screen,color,(home_size*8+home_size/4,i*home_size+home_size/4,home_size/4,home_size))
        text_surface = my_font.render(str(8-i), False, (255,255,255) if i%2==0 else (0,0,0))
        screen.blit(text_surface,(home_size*8+home_size/3,i*home_size+home_size/2+Font_size))
    #draw top side chars
    for i in range(8):
        color = (250, 228, 178) if board[i][0] == 'white' else (93, 53, 43)
        pygame.draw.rect(screen,color,(i*home_size+home_size/4,0,home_size,home_size/4))
        text_surface = my_font.render(get_char_from_int(i), False, (255,255,255) if i%2==1 else (0,0,0))
        screen.blit(text_surface,(i*home_size+home_size/2+home_size/4,home_size/8-10))
    #draw bottom side chars
    for i in range(8):
        color = (250, 228, 178) if board[i][7] == 'white' else (93, 53, 43)
        pygame.draw.rect(screen,color,(i*home_size+home_size/4,home_size*8+home_size/4,home_size,home_size/4))
        text_surface = my_font.render(get_char_from_int(i), False, (255,255,255) if i%2==0 else (0,0,0))
        screen.blit(text_surface,(i*home_size+home_size/2+home_size/4,home_size*8.5-Font_size-home_size/8))
    pygame.draw.rect(screen,(40,40,40),(home_size/4,home_size/4,home_size*8,home_size*8),1)


#convert soldier to another pieces
def soldier_to(player,loc,board):
    os.system('cls')
    print(game.message,'\n')
    match(input('player '+player+'User 1 Enter one of the pieces below to place with your pawn.\nR for rook\nB for bishop\nN for knight\nQ for queen\n')):
        case 'B' | 'b':board[loc[0]][loc[1]]=Bishop(player,'bishop','./images/'+player+' bishop.png')
        case 'Q' | 'q':board[loc[0]][loc[1]]=Queen(player,'queen','./images/'+player+' queen.png')
        case 'R' | 'r':board[loc[0]][loc[1]]=Rook(player,'rook','./images/'+player+' rook.png')
        case 'N' | 'n':board[loc[0]][loc[1]]=Knight(player,'knight','./images/'+player+' knight.png')
        case _:soldier_to(player,loc,board)

                
            

# create pieces and put in chess board array
for row in range(8):
    chess_board[1][row]=Pawn("black",'pawn','./images/black pawn.png')
    chess_board[6][row]=Pawn("white",'pawn','./images/white pawn.png')
chess_board[0][4]=King("black",'king','./images/black king.png')
chess_board[7][4]=King("white",'king','./images/white king.png')
chess_board[0][3]=Queen("black",'queen','./images/black queen.png')
chess_board[7][3]=Queen("white",'queen','./images/white queen.png')
chess_board[0][0]=Rook("black",'rook','./images/black rook.png')
chess_board[0][7]=Rook("black",'rook','./images/black rook.png')
chess_board[7][0]=Rook("white",'rook','./images/white rook.png')
chess_board[7][7]=Rook("white",'rook','./images/white rook.png')
chess_board[0][2]=Bishop("black",'bishop','./images/black bishop.png')
chess_board[0][5]=Bishop("black",'bishop','./images/black bishop.png')
chess_board[7][2]=Bishop("white",'bishop','./images/white bishop.png')
chess_board[7][5]=Bishop("white",'bishop','./images/white bishop.png')
chess_board[0][1]=Knight("black",'knight','./images/black knight.png')
chess_board[0][6]=Knight("black",'knight','./images/black knight.png')
chess_board[7][6]=Knight("white",'knight','./images/white knight.png')
chess_board[7][1]=Knight("white",'knight','./images/white knight.png')


#set False to don't show status number
print_status_number=True
running = True
chess = initialize_board()
game=ChessGame(chess_board)
screen.fill((0, 0, 0))
draw_board(screen, chess , chess_board,game.selected,[])
pygame.display.flip()
ev=True
print(game.message)
if(print_status_number):
    print('status number is: '+str(get_status_n(game.current_player,chess_board,game.castling)))
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if(event.type==pygame.MOUSEBUTTONUP and event.button==1 and ev):
            #click on pygame window
            y=math.floor((event.pos[1]-home_size/4)/(min_screen_size/10))
            x=math.floor((event.pos[0]-home_size/4)/(min_screen_size/10))
            if(x<0 or y<0 or y>7 or x>7):
                continue
            if(chess_board[y][x] and chess_board[y][x].color==game.current_player):
                if((y,x)!=game.selected):
                    game.selecte((y,x))
                    game.av_mov=chess_board[y][x].av_mov(chess_board,game.selected,game.castling)
            elif(((not chess_board[y][x]) or chess_board[y][x].color!=game.current_player) and ((y,x) in game.av_mov)):
                chess_board[y][x]=chess_board[game.selected[0]][game.selected[1]]
                chess_board[game.selected[0]][game.selected[1]]=None
                
                #Checking the soldier's arrival at the end
                if(chess_board[y][x] and chess_board[y][x].name=='pawn' and (y==7 or y==0)):
                    soldier_to(game.current_player,(y,x),chess_board)
                    os.system('cls')
                    print(game.message,'\n')

                #checking the move is castling move or not
                if(game.castling['white_long_castling'] and chess_board[y][x].name=='king' and game.current_player=='white' and x == 2):
                    chess_board[7][3]=chess_board[7][0]
                    chess_board[7][7]=None
                    game.castling['white_long_castling']=False
                    game.castling['white_short_castling']=False
                elif(game.castling['white_short_castling'] and chess_board[y][x].name=='king' and game.current_player=='white' and x == 6):
                    chess_board[7][5]=chess_board[7][7]
                    chess_board[7][7]=None
                    game.castling['white_short_castling']=False
                    game.castling['white_long_castling']=False
                elif(game.castling['black_long_castling'] and chess_board[y][x].name=='king' and game.current_player=='black' and x == 2):
                    chess_board[0][3]=chess_board[0][0]
                    chess_board[0][0]=None
                    game.castling['black_long_castling']=False
                    game.castling['black_short_castling']=False
                elif(game.castling['black_short_castling'] and chess_board[y][x].name=='king' and game.current_player=='black' and y == 6):
                    chess_board[0][5]=chess_board[0][7]
                    chess_board[0][7]=None
                    game.castling['black_short_castling']=False
                    game.castling['black_long_castling']=False

                #checking the king move
                elif(game.castling['white_long_castling'] and game.castling['white_short_castling'] and chess_board[y][x].name=='king' and game.current_player=='white'):
                    game.castling['white_long_castling']=False
                    game.castling['white_short_castling']=False
                elif(game.castling['black_long_castling'] and game.castling['black_short_castling'] and chess_board[y][x].name=='king' and game.current_player=='black'):
                    game.castling['black_long_castling']=False
                    game.castling['black_short_castling']=False

                #checking the rooks moves
                elif(game.castling['white_short_castling'] and y==7 and x==7):
                    game.castling['white_short_castling']=False
                elif(game.castling['white_long_castling'] and y==0 and x==7):
                    game.castling['white_long_castling']=False
                elif(game.castling['black_short_castling'] and y==0 and x==0):
                    game.castling['black_short_castling']=False
                elif(game.castling['black_long_castling'] and y==7 and x==0):
                    game.castling['black_long_castling']=False
                
                
                game.selected=[]
                game.av_mov=[]
                game.switch_player()
                if(print_status_number):
                    print('status number is: '+str(get_status_n(game.current_player,chess_board,game.castling)))
                
                #check player is in check or not
                if(is_in_check(game.current_player,chess_board)):
                    arr_x=[]
                    if(getstatus(chess_board,game.current_player,False,arr_x,game.castling)==0):
                        game.selecte(None)
                        game.av_mov=[]
                        draw_board(screen, chess , chess_board,game.selected,game.av_mov)
                        print('checkmated...!\nplayer '+game.current_player+' loss game')
                        ev=False
                    else:
                        print('check')
                        game.check_home=get_king_home(game.current_player,chess_board)
                else:
                    game.check_home=None
            else:
                game.selecte(None)
                game.av_mov=[]
            draw_board(screen, chess , chess_board,game.selected,game.av_mov)
            pygame.display.flip()

pygame.quit()