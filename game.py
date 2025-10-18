class ChessGame:
    def __init__(self,board):
        self.message='hi:)\nthis game created by ehsan imani.\nproject link:\nhttps://github.com/ehsan-imani/chess-by-python'
        self.board = board
        self.current_player = 'white'
        self.selected=None
        self.av_mov=[]
        self.check_home=None
        self.white_status=0
        self.black_status=0
        self.castling={'white_short_castling':True,
                      'white_long_castling':True,
                      'black_short_castling':True,
                      'black_long_castling':True}
    def selecte(self,loc):
        self.selected=loc
    def switch_player(self):
        self.current_player = 'black' if self.current_player == 'white' else 'white'