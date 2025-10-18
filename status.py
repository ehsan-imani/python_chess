from pieces import *
import os
message='hi:)\nthis game created by ehsan imani.\nproject link:\nhttps://github.com/ehsan-imani/chess-by-python'
def get_char_from_int(n):
    match(n):
        case 0:return 'a'
        case 1:return 'b'
        case 2:return 'c'
        case 3:return 'd'
        case 4:return 'e'
        case 5:return 'f'
        case 6:return 'g'
        case 7:return 'h'
def get_small_name(s):
    match(s):
        case 'pawn':return 'P'
        case 'queen':return 'Q'
        case 'king':return 'K'
        case 'knight':return 'N'
        case 'rook':return 'R'
        case 'bishop':return 'B'
        case _:return 'undefined'

#get a player status number and avalible moves
def getstatus(board,player,printly,arr_r,castling):
    status_n=0
    for row in range(8):
        for col in range(8):
            if(board[row][col] and board[row][col].color==player):
                # print(row,col)
                arr=board[row][col].av_mov(board,(row,col),castling)
                if(arr!=[]):
                    status_n+=len(arr)
                for i in arr:
                    if(printly):
                        x=board[i[0]][i[1]]
                        board[i[0]][i[1]]=board[row][col]
                        board[row][col]=x
                        s=getstatus(board,'white',False,arr,castling)-(getstatus(board,'black',False,arr,castling))
                        arr_r.append(([s,get_small_name(board[i[0]][i[1]].name)+' '+str(8-row)+get_char_from_int(col)+' -> '+str(8-i[0])+get_char_from_int(i[1])+'   atatus number after:']))
                        # print(get_small_name(board[i[0]][i[1]].name)+' '+str(8-row)+get_char_from_int(col)+' -> '+str(8-i[0])+get_char_from_int(i[1])+'   atatus number after:'+str(getstatus(board,'white',False)-(getstatus(board,'black',False))))
                        board[row][col]=board[i[0]][i[1]]
                        board[i[0]][i[1]]=x
    return status_n
#get and sort avalble moves and thaths status number
def get_status_n(current_player,chess_board,castling):
    black_status=0
    white_status=0
    if(current_player=='white'):
        arr=[]
        black_status=getstatus(chess_board.copy(),'black',True,arr,castling)
        os.system('cls')
        print(message,'\n')
        arr=[]
        white_status=getstatus(chess_board.copy(),'white',True,arr,castling)
    else:
        arr=[]
        white_status=getstatus(chess_board.copy(),'white',True,arr,castling)
        os.system('cls')
        print(message,'\n')
        arr=[]
        black_status=getstatus(chess_board.copy(),'black',True,arr,castling)
    if(current_player=='white'):
        arr=sorted(arr,key=lambda x:x[0], reverse=True)
    else:
        arr=sorted(arr,key=lambda x:x[0], reverse=False)
    for i in arr:
        print(i[1]+'\t after thath status number: '+str(i[0]))
    return white_status-black_status
    
                    
