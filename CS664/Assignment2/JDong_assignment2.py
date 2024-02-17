import game_helpers as gh

class QGame(gh.Game):
    def __init__(self,height = 4, width = 4,k = 4) -> None:
        self.k = k # k in a row
        self.squares = {(x, y) for x in range(width) for y in range(height)}
        self.names = ('A','B','C','D') 
        self.pieces = {'X': {'A':2, 'B':2, 'C':2, 'D':2}, 'O': {'A':2, 'B':2, 'C':2, 'D':2}}
        self.inital = QBoard #empty QBoard

    def filterMove(self,moves,state):
        #TODO write function to check for 
        player = state.to_move
        for move in moves:
            currX = move[0][0]
            currY = move[0][1]

        return moves
    

    def actions(self, state):
        """Return a collection of the allowable moves from this state."""
        emptyPlace = self.squares - set(state)
        player = state.to_move
        pieces = self.pieces[player]

        moves = [(square,piece) for square in emptyPlace
                for piece in self.names if pieces[piece]!=0]
        
        return self.filterMove(moves)
    
    

    def result(self, state, move):
        """Return the state that results from making a move from a state."""
        square, piece = move
        player = board.to_move
        board = board.new({square: [player,piece]}, to_move=('O' if player == 'X' else 'X'))
        win = k_in_row(board, player, square, self.k)
        board.utility = (0 if not win else +1 if player == 'X' else -1)
        return board
    

    def is_terminal(self, state):
        """Return True if this is a final state for the game."""
        return state.utility != 0 or len(self.squares) == len(state)
    
    def utility(self, state, player):
        """Return the value of this final state to player."""
        return state.utility if player == 'X' else -state.utility
    
    def display(self, board):
        print(board)
    
class QBoard(gh.defaultdict):
    # empty spot: player,shape
    empty = ('_','_')
    off = ('#','#')
    shapes = ['A','B','C','D']

    def __init__(self, width = 4, height = 4,to_move = None, **kwds):
        self.__dict__.update(width=width, height=height, to_move=to_move, **kwds)
    def new(self, changes: dict, **kwds) -> 'QBoard':
        "Given a dict of {(x, y): contents} changes, return a new Board with the changes."
        board = QBoard(width=self.width, height=self.height, **kwds)
        board.update(self)
        board.update(changes)
        return board
    def __missing__(self, loc):
        x, y = loc
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.empty
        else:
            return self.off    
    def __hash__(self): 
        return hash(tuple(sorted(self.items()))) + hash(self.to_move)
    def __repr__(self):
        def row(y): return ' '.join(self[x, y][0]+','+self[x,y][1] for x in range(self.width))
        return '\n'.join(map(row, range(self.height))) +  '\n'

def checkRow(board, player, square, xRange,yRange,k):
    """True if player has k pieces in a line through square."""

    def in_row(x, y, dx, dy): 
        return 0 if board[x, y][0] != player else 1 + in_row(x + dx, y + dy, dx, dy)
    
    return any(in_row(*square, dx, dy) + in_row(*square, -dx, -dy) - 1 >= k 
               for (dx, dy) in ((0, 1), (1, 0), (1, 1), (1, -1)))



if __name__ == "__main__":
    qBoard = QBoard()