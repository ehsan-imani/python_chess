import pygame
#To calculate av_mov on rook, queen, bishop pieces
def go(board,selected,x_m,y_m,av_mov):
    y=selected[0]
    x=selected[1]
    color='black'
    n_color='white'
    if(board[y][x].color=='white'):
        color='white'
        n_color='black'
    for i in range(8):
        if(y+y_m>7 or y+y_m<0 or x+x_m>7 or x+x_m<0):
            break
        if(board[y+y_m][x+x_m]!=None):
            if(board[y+y_m][x+x_m].color==n_color):
                av_mov.append((y+y_m,x+x_m))
            break
        else:
            av_mov.append((y+y_m,x+x_m))
            y+=y_m
            x+=x_m
    return av_mov
#check check
def is_in_check(player,board):
    n_color='white'
    if(player=='white'):
        n_color='black'
    (king_y ,king_x) =get_king_home(player,board)
    
    for row in range(8):
        for col in range(8):
            if(board[row][col] and board[row][col].color==n_color):
                av_mov=board[row][col].av_mov(board,(row,col),None,False)
                if(av_mov and ((king_y,king_x) in av_mov)):
                    return True
    return False
#get a player kig home location
def get_king_home(player,board):
    king_x=None
    king_y=None
    for row in range(8):
        for col in range(8):
            if(board[row][col] and board[row][col].name=='king' and board[row][col].color==player):
                king_x=row
                king_y=col
                break
        if(king_x):break
    return (king_x,king_y)
#Removing the movements that we make after performing the ritual
def edit_av_mov(av_mov,board,color,x,y):
    if(not av_mov):
        return
    deleted_arr=[]
    for i in av_mov:
        last_p=board[i[0]][i[1]]
        board[i[0]][i[1]]=board[y][x]
        board[y][x]=None
        if(is_in_check(color,board)):
            deleted_arr.append(i)
        board[y][x]=board[i[0]][i[1]]
        board[i[0]][i[1]]=last_p
    for i in deleted_arr:
        av_mov.remove(i)

#check part of castling
def check_in_range(board,player,min,max,y):
    king_loc=get_king_home(player,board)
    for i in range(min,max):
        if(board[y][i] and (y,i)!=king_loc and (i!=0 and i!=7)):
            return False
        last_p=board[y][i]
        board[y][i]=board[king_loc[0]][king_loc[1]]
        board[king_loc[0]][king_loc[1]]=None
        if(is_in_check(player,board)):
            board[king_loc[0]][king_loc[1]]=board[y][i]
            board[y][i]=last_p
            return False
        board[king_loc[0]][king_loc[1]]=board[y][i]
        board[y][i]=last_p
    return True
class Piece:
    def __init__(self, color,name,url):
        self.name=name
        self.color = color
        if(url):
            self.img=pygame.transform.scale(pygame.image.load(url).convert_alpha(),(50,50))

    def av_mov(board,selected):
        raise NotImplementedError("improve this method")

class Pawn(Piece):
    def av_mov(self,board,selected,castling,edit_m=True):
        av_mov=[]
        y=selected[0]
        x=selected[1]
        if(board[y][x].color=='white'):
            if(y!=0 and board[y-1][x]==None):
                av_mov.append((y-1,x))
                if(y==6 and board[y-2][x]==None):
                    av_mov.append((y-2,x))
            if(x!=7 and y!=0 and board[y-1][x+1]!=None and board[y-1][x+1].color=='black'):
                av_mov.append((y-1,x+1))
            if(x!=0 and y!=0 and board[y-1][x-1]!=None and board[y-1][x-1].color=='black'):
                av_mov.append((y-1,x-1))
        else:
            if(y!=7 and board[y+1][x]==None):
                av_mov.append((y+1,x))
                if(y==1 and board[y+2][x]==None):
                    av_mov.append((y+2,x))
            if(x!=7 and y!=7 and board[y+1][x+1]!=None and board[y+1][x+1].color=='white'):
                av_mov.append((y+1,x+1))
            if(x!=0 and y!=7 and board[y+1][x-1]!=None and board[y+1][x-1].color=='white'):
                av_mov.append((y+1,x-1))
        if(edit_m):
            edit_av_mov(av_mov,board,self.color,x,y)
        return av_mov

class Rook(Piece):
    def av_mov(self,board,selected,castling,edit_m=True):
        av_mov=[]
        go(board,selected,1,0,av_mov)
        go(board,selected,0,1,av_mov)
        go(board,selected,0,-1,av_mov)
        go(board,selected,-1,0,av_mov)
        if(edit_m):
            edit_av_mov(av_mov,board,self.color,selected[1],selected[0])
        return av_mov

class Knight(Piece):
    def av_mov(self,board,selected,castling,edit_m=True):
        av_mov=[]
        y=selected[0]
        x=selected[1]
        n_color='white'
        if(board[y][x].color=='white'):
            n_color='black'
        if(y>=2 and x>=1 and (board[y-2][x-1]==None or board[y-2][x-1].color==n_color)):
            av_mov.append((y-2,x-1))
        if(y>=2 and x<=6 and (board[y-2][x+1]==None or board[y-2][x+1].color==n_color)):
            av_mov.append((y-2,x+1))
        if(y<=5 and x>=1 and (board[y+2][x-1]==None or board[y+2][x-1].color==n_color)):
            av_mov.append((y+2,x-1))
        if(y<=5 and x<=6 and (board[y+2][x+1]==None or board[y+2][x+1].color==n_color)):
            av_mov.append((y+2,x+1))
        if(y>=1 and x>=2 and (board[y-1][x-2]==None or board[y-1][x-2].color==n_color)):
            av_mov.append((y-1,x-2))
        if(y>=1 and x<=5 and (board[y-1][x+2]==None or board[y-1][x+2].color==n_color)):
            av_mov.append((y-1,x+2))
        if(y<=6 and x>=2 and (board[y+1][x-2]==None or board[y+1][x-2].color==n_color)):
            av_mov.append((y+1,x-2))
        if(y<=6 and x<=5 and (board[y+1][x+2]==None or board[y+1][x+2].color==n_color)):
            av_mov.append((y+1,x+2))
        if(edit_m):
            edit_av_mov(av_mov,board,self.color,selected[1],selected[0])
        return av_mov
class Bishop(Piece):
    def av_mov(self,board,selected,castling,edit_m=True):
        av_mov=[]
        go(board,selected,-1,-1,av_mov)
        go(board,selected,1,1,av_mov)
        go(board,selected,-1,1,av_mov)
        go(board,selected,1,-1,av_mov)
        if(edit_m):
            edit_av_mov(av_mov,board,self.color,selected[1],selected[0])
        return av_mov

class Queen(Piece):
    def av_mov(self,board,selected,castling,edit_m=True):
        av_mov=[]
        go(board,selected,1,0,av_mov)
        go(board,selected,0,1,av_mov)
        go(board,selected,0,-1,av_mov)
        go(board,selected,-1,0,av_mov)
        go(board,selected,-1,-1,av_mov)
        go(board,selected,1,1,av_mov)
        go(board,selected,-1,1,av_mov)
        go(board,selected,1,-1,av_mov)
        if(edit_m):
            edit_av_mov(av_mov,board,self.color,selected[1],selected[0])
        return av_mov
class King(Piece):
    def av_mov(self,board,selected,castling,edit_m=True):
        av_mov=[]
        y=selected[0]
        x=selected[1]
        n_color='white'
        if(board[y][x].color=='white'):
            n_color='black'
        if(x<7):
            if(board[y][x+1]==None or board[y][x+1].color==n_color):
                av_mov.append((y,x+1))
            if(y<7 and (board[y+1][x+1]==None or board[y+1][x+1].color==n_color)):
                av_mov.append((y+1,x+1))
            if(y>0 and (board[y-1][x+1]==None or board[y-1][x+1].color==n_color)):
                av_mov.append((y-1,x+1))
        if(x>0):
            if(board[y][x-1]==None or board[y][x-1].color==n_color):
                av_mov.append((y,x-1))
            if(y<7 and (board[y+1][x-1]==None or board[y+1][x-1].color==n_color)):
                av_mov.append((y+1,x-1))
            if(y>0 and (board[y-1][x-1]==None or board[y-1][x-1].color==n_color)):
                av_mov.append((y-1,x-1))
        if(y<7 and (board[y+1][x]==None or board[y+1][x].color==n_color)):
                av_mov.append((y+1,x))
        if(y>0 and (board[y-1][x]==None or board[y-1][x].color==n_color)):
                av_mov.append((y-1,x))
        if(edit_m):
            edit_av_mov(av_mov,board,self.color,selected[1],selected[0])
            if(self.color=='white'):
                if(castling['white_short_castling'] and check_in_range(board,self.color,4,8,7)):
                    av_mov.append((7,6))
                if(castling['white_long_castling'] and check_in_range(board,self.color,0,5,7)):
                    av_mov.append((7,2))
            else:
                if(castling['black_short_castling'] and check_in_range(board,self.color,4,8,0)):
                    av_mov.append((0,6))
                if(castling['black_long_castling'] and check_in_range(board,self.color,0,5,0)):
                    av_mov.append((0,2))
        return av_mov