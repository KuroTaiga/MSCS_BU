from collections import namedtuple, Counter, defaultdict
import random
import math
import functools 
from itertools import product

cache = functools.lru_cache(10**8)

##########################################

class Game:
    """A game is similar to a problem, but it has a terminal test instead of 
    a goal test, and a utility for each terminal state. To create a game, 
    subclass this class and implement `actions`, `result`, `is_terminal`, 
    and `utility`. You will also need to set the .initial attribute to the 
    initial state; this can be done in the constructor."""

    def actions(self, state):
        """Return a collection of the allowable moves from this state."""
        raise NotImplementedError

    def result(self, state, move):
        """Return the state that results from making a move from a state."""
        raise NotImplementedError

    def is_terminal(self, state):
        """Return True if this is a final state for the game."""
        return not self.actions(state)
    
    def utility(self, state, player):
        """Return the value of this final state to player."""
        raise NotImplementedError

##########################################

def play_game(game, strategies: dict, verbose=False):
    """Play a turn-taking game. `strategies` is a {player_name: function} dict,
    where function(state, game) is used to get the player's move."""
    
    state = game.initial
    count = 0
    while not game.is_terminal(state):
        player = state.to_move
        move = strategies[player](game, state)
        state = game.result(state, move)
        count += 1
        if verbose: 
            print('Step', count, 'After Player', player, 'move:', move)
            print(state)

    if not verbose:
        print('Step', count, 'After Player', player, 'move:', move)
        #print(state)
    return state

##########################################

infinity = math.inf
node_count = 0

def minimax_search(game, state):
    """Search game tree to determine best move; return (value, move) pair."""

    global node_count
    node_count = 0

    player = state.to_move

    def max_value(state, depth=0):
        global node_count
        node_count += 1
        if node_count % 1000000 == 0:
            print(node_count, depth)
        if game.is_terminal(state):
            return game.utility(state, player), None
            
        v, move = -infinity, None
        for a in game.actions(state):
            v2, _ = min_value(game.result(state, a), depth+1)
            if v2 > v:
                v, move = v2, a
        return v, move

    def min_value(state, depth=1):
        global node_count
        node_count += 1
        if node_count % 1000000 == 0:
            print(node_count, depth)
        if game.is_terminal(state):
            return game.utility(state, player), None
            
        v, move = +infinity, None
        for a in game.actions(state):
            v2, _ = max_value(game.result(state, a), depth+1)
            if v2 < v:
                v, move = v2, a
        return v, move

    return max_value(state)


##########################################

def alphabeta_search(game, state):
    """Search game to determine best action; use alpha-beta pruning.
    This version searches all the way to the leaves."""

    global node_count
    node_count = 0

    player = state.to_move

    def max_value(state, alpha, beta, depth=0):
        global node_count
        node_count += 1
        if node_count % 100000 == 0:
            print(node_count, depth)

        if game.is_terminal(state):
            return game.utility(state, player), None
            
        v, move = -infinity, None
        for a in game.actions(state):
            v2, _ = min_value(game.result(state, a), alpha, beta, depth+1)
            if v2 > v:
                v, move = v2, a
                alpha = max(alpha, v)
            if v >= beta:
                return v, move
        return v, move

    def min_value(state, alpha, beta, depth=1):
        global node_count
        node_count += 1
        if node_count % 100000 == 0:
            print(node_count, depth)

        if game.is_terminal(state):
            return game.utility(state, player), None
            
        v, move = +infinity, None
        for a in game.actions(state):
            v2, _ = max_value(game.result(state, a), alpha, beta, depth+1)
            if v2 < v:
                v, move = v2, a
                beta = min(beta, v)
            if v <= alpha:
                return v, move
        return v, move

    return max_value(state, -infinity, +infinity)

##########################################
def minimax_search_tt(game, state):
    """Search game to determine best move; return (value, move) pair."""

    player = state.to_move

    @cache
    def max_value(state):
        if game.is_terminal(state):
            return game.utility(state, player), None
        v, move = -infinity, None
        for a in game.actions(state):
            v2, _ = min_value(game.result(state, a))
            if v2 > v:
                v, move = v2, a
        return v, move

    @cache
    def min_value(state):
        if game.is_terminal(state):
            return game.utility(state, player), None
        v, move = +infinity, None
        for a in game.actions(state):
            v2, _ = max_value(game.result(state, a))
            if v2 < v:
                v, move = v2, a
        return v, move

    return max_value(state)
########################################

def cache1(function):
    "Like lru_cache(None), but only considers the first argument of function."
    cache = {}
    def wrapped(x, *args):
        if x not in cache:
            cache[x] = function(x, *args)
        return cache[x]
    return wrapped

def alphabeta_search_tt(game, state):
    """Search game to determine best action; use alpha-beta pruning.
    This version searches all the way to the leaves."""

    global node_count
    node_count = 0

    player = state.to_move

    @cache1
    def max_value(state, alpha, beta, depth=0):
        global node_count
        node_count += 1
        if node_count % 1000000 == 0:
            print(node_count, depth)


        if game.is_terminal(state):
            return game.utility(state, player), None
        v, move = -infinity, None
        for a in game.actions(state):
            v2, _ = min_value(game.result(state, a), alpha, beta, depth+1)
            if v2 > v:
                v, move = v2, a
                alpha = max(alpha, v)
            if v >= beta:
                return v, move
        return v, move

    @cache1
    def min_value(state, alpha, beta, depth=1):
        global node_count
        node_count += 1
        if node_count % 1000000 == 0:
            print(node_count, depth)

        if game.is_terminal(state):
            return game.utility(state, player), None
        v, move = +infinity, None
        for a in game.actions(state):
            v2, _ = max_value(game.result(state, a), alpha, beta, depth+1)
            if v2 < v:
                v, move = v2, a
                beta = min(beta, v)
            if v <= alpha:
                return v, move
        return v, move

    return max_value(state, -infinity, +infinity)

    ########################


def cutoff_depth(d):
    """A cutoff function that searches to depth d."""
    return lambda game, state, depth: depth > d

def h_alphabeta_search(game, state, cutoff=cutoff_depth(4), h=lambda s, p: 0):
    """Search game to determine best action; use alpha-beta pruning.
    As in [Figure 5.7], this version searches all the way to the leaves."""

    player = state.to_move

    @cache1
    def max_value(state, alpha, beta, depth):
        if game.is_terminal(state):
            return game.utility(state, player), None
        if cutoff(game, state, depth):
            return h(state, player), None
        v, move = -infinity, None
        for a in game.actions(state):
            v2, _ = min_value(game.result(state, a), alpha, beta, depth+1)
            if v2 > v:
                v, move = v2, a
                alpha = max(alpha, v)
            if v >= beta:
                return v, move
        return v, move

    @cache1
    def min_value(state, alpha, beta, depth):
        if game.is_terminal(state):
            return game.utility(state, player), None
        if cutoff(game, state, depth):
            return h(state, player), None
        v, move = +infinity, None
        for a in game.actions(state):
            v2, _ = max_value(game.result(state, a), alpha, beta, depth + 1)
            if v2 < v:
                v, move = v2, a
                beta = min(beta, v)
            if v <= alpha:
                return v, move
        return v, move

    return max_value(state, -infinity, +infinity, 0)

    ##############



def random_player(game, state): 
    return random.choice(list(game.actions(state)))


def player(search_algorithm):
    """A game player who uses the specified search algorithm"""
    return lambda game, state: search_algorithm(game, state)[1]

##########################################

