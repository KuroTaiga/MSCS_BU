from game_helpers2 import *
import random
from itertools import product
class QGame(Game):
    def __init__(self,height = 4, width = 4,k = 4) -> None:
        self.k = k # k in a row
        self.squares = {(x, y) for x in range(width) for y in range(height)}
        self.names = ('A','B','C','D') 
        self.pieces = {'X': {'A':2, 'B':2, 'C':2, 'D':2}, 'O': {'A':2, 'B':2, 'C':2, 'D':2}}
        self.initial = QBoard(height=height, width=width, to_move='X', utility= 0) #empty QBoard

    def filterMove(self, moves, state):
        # Convert board state to a more efficient lookup structure
        
        legal_moves = []
        for move in moves:
            x, y, shape = move[0][0], move[0][1], move[1]

            # Determine the region for the current move
            region_x = x // 2 * 2  # This will round down x to the nearest even number
            region_y = y // 2 * 2  # This will round down y to the nearest even number

            # Check for overlap within the same region
            overlap = False
            for dx in range(2):
                for dy in range(2):
                    pos = (region_x + dx, region_y + dy)
                    if pos in state and state[pos][1] == shape and state[pos][0] != state.to_move:
                        overlap = True
                        break
                if overlap:
                    break
            for dx in range(4):
                pos = (dx,y)
                if pos in state and state[pos][1] == shape and state[pos][0] != state.to_move:
                        overlap = True
                        break
            for dy in range(4):
                pos = (x,dy)
                if pos in state and state[pos][1] == shape and state[pos][0] != state.to_move:
                        overlap = True
                        break
            if not overlap:
                legal_moves.append(move)

        return legal_moves

    def actions(self, state):
        """Return a collection of the allowable moves from this state."""
        emptyPlace = self.squares - set(state)
        player = state.to_move
        player_pieces = state.remaining_pieces(player)
        
        # moves are empty spots on board for now, combined with
        # avalible pieces for the player
        """now it takes care of pieces"""
        moves = [(square,piece) for square in emptyPlace
                for piece in self.names if player_pieces[piece]!=0]
        """professor's way of using product instead of nested loops"""
        #moves = [(square, piece) for square, piece in product(emptyPlace,self.names) 
        #         if player_pieces[piece] != 0]
        return self.filterMove(moves,state)

    def result(self, state, move):
        """Return the state that results from making a move from a state."""
        square, piece = move
        
        player = state.to_move
        """action function takes care of checking for remaining peices"""
        state = state.new({square: [player,piece]}, to_move=('O' if player == 'X' else 'X'))
        """Old implementation of how pieces"""
        # self.pieces[player][piece] -= 1
        # win is true either we got all pieces in or next player has no possible actions
        win = four_pieces(state, player, square, self.k) or len(self.actions(state))==0
        # print(win)
        state.utility = (0 if not win else +1 if player == 'X' else -1)
        
        return state
    
    def is_terminal(self, state):
        """Return True if this is a final state for the game."""
        """ won, no empty squares, or no legal moves """
        return state.utility != 0 or len(self.squares) == len(state) or len(self.actions(state))==0
    
    def utility(self, state, player):
        """Return the value of this final state to player."""
        return state.utility if player == 'X' else -state.utility
    
    def display(self, board):
        print(board)
    
class QBoard(defaultdict):
    # empty spot: player,shape
    empty = ('_','_')
    off = ('#','#')
    shapes = ['A','B','C','D']
    pieces = {'X': {'A':2, 'B':2, 'C':2, 'D':2}, 'O': {'A':2, 'B':2, 'C':2, 'D':2}}
    
    # the board should be tracking the number of ieces avaiable to each player
    # not the game class
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
        items_as_tuples = tuple((k, tuple(v) if isinstance(v, list) else v) for k, v in sorted(self.items()))
        return hash(items_as_tuples)+ hash(self.to_move)
    def __repr__(self):
        def row(y): return ' '.join(self[x, y][0]+','+self[x,y][1] for x in range(self.width))
        return '\n'.join(map(row, range(self.height))) +  '\n'
    def remaining_pieces(self, player):
        result = {'A':2, 'B':2, 'C':2, 'D':2}
        for x in range(self.width):
            for y in range(self.height):
                if self[x,y][0] == player:
                    result[self[x,y][1]] -= 1
        return result
def four_pieces(board, player, square, k):
    """True if player has k pieces in a line through square."""
    def in_row(x, y): 
        # check for the current row if it got all 4 pieces
        # return 1 if all 4 pieces are met, else 0
        x_pieces_list = []
        for x_iter in range(0,k):
            if (board[x_iter,y][1]!= '_'):
                x_pieces_list.append(board[x_iter,y][1])
        y_pieces_list = []
        for y_iter in range(0,k):
            if (board[x,y_iter][1]!= '_'):
                y_pieces_list.append(board[x,y_iter][1])
        return 1 if (len(set(x_pieces_list)) == 4 or len(set(y_pieces_list))==4) else 0
    def in_any_region(x,y):
        # Check for the current region
        # return 1 if it has all 4 pieces, else 0
        pieces_list = []
        xRange = [0,1] if x <= 2 else [2,3]
        yRange = [0,1] if y<=2 else [2,3]
        for x_iter in xRange:
            for y_iter in yRange:
                if board[x_iter,y_iter][1] != '_':
                    pieces_list.append(board[x_iter,y_iter][1])

        return True if (len(set(pieces_list)) == 4) else False

    return in_row(*square) or in_any_region(*square)



if __name__ == "__main__":
    qBoard = QBoard()
    # qGame = QGame()
    random.seed(7)
    # playing with 2 random players
    # print("2 Random players")
    # print(play_game(qGame, 
    #       dict(X=random_player, 
    #            O=random_player), 
    #       verbose=True).utility)
    
    #playing with random player + Minimax player
    
    print(play_game(QGame(), 
          dict(X=random_player, 
               O=random_player), 
          verbose=True).utility)
    
    print("Random vs Minimax")
    print(play_game(QGame(),
          {'X':random_player,
           'O':player(h_alphabeta_search)},verbose=True).utility)
    print("Done")