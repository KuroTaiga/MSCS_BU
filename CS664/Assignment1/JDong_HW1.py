import search_helpers as sh
import random

BUID = 8916

# Pancake problem
class PancakeProblem(sh.Problem):
    """A PancakeProblem the goal is always `tuple(range(1, n+1))`, where the
    initial state is a permutation of `range(1, n+1)`. An act is the index `i` 
    of the top `i` pancakes that will be flipped."""
    
    def __init__(self, initial): 
        self.initial, self.goal = tuple(initial), tuple(sorted(initial))
    
    # in the form of flip<i> to flip the top i pancakes
    """
    OLD action function used for Q1 and Q2
    def actions(self, state): 
        return range(2, len(state) + 1)
    OLD result function used for Q1 and Q2
    def result(self, state, i): 
        return state[:i][::-1] + state[i:]
    """
    def actions(self, state):
        return ['Flip ' + str(i) for i in range(2, len(state) + 1)]

    def result(self, state, action):
        i  = int(action[5:])
        print(action)
        print(action[5])
        return state[:i][::-1] + state[i:]

    def h(self, node):
        "The gap heuristic."
        s = node.state
        return sum(abs(s[i] - s[i - 1]) > 1 for i in range(1, len(s)))

class PancakeProblemWithFlipCost(PancakeProblem):
    """
     The action_cost should be the number of pancakes to be flipped
    """
    def action_cost(self, s, action, s1):
        return int(action[5:])
    
class PancakeProblemOutOfOrder(PancakeProblem):
    """
    The heuristic h should be the sum of the gap of the consecutive pancakes in the node’s state.
    """
    def h(self, node):
        s = node.state
        return sum((abs(s[i] - s[i - 1])-1) for i in range(1,len(s)))

# initialize the starting state of the pancake problem based on the last 4 digits of the BUID
# it returns a shuffled list containing elements 1,2...n
def initPancake(BUID,n):
    random.seed(BUID)
    currList = list(range(1,n+1))
    random.shuffle(currList)
    return tuple(currList)

if __name__ == "__main__":
    N = 5
    verbose = 1
    startingState = initPancake(BUID,N) 
    #should yield [4, 3, 5, 2, 6, 7, 1] as initial sequence
    pancakeStack = PancakeProblem(startingState)
    pancakeStackWithCost = PancakeProblemWithFlipCost(startingState)
    pancakeStackOutOfOrder = PancakeProblemOutOfOrder(startingState)
    # Modeify the problem for each function for each Question call in place
    #Perform BFS, Uniform cost search, Gready BFS, A* and weighted A* (1.1)
    # use verbose=1 for those algorithms
    weightAStar = 1.1
    # BFS
    print("BFS: ")
    sh.breadth_first_search(problem=pancakeStackOutOfOrder,verbose = verbose)
    # Uniform cost search
    print("Uniform cost search: ")
    sh.uniform_cost_search(problem=pancakeStackOutOfOrder,verbose = verbose)
    # Gready BFS
    print("Greedy BFS")
    sh.greedy_bfs(problem=pancakeStackOutOfOrder,verbose = verbose)
    # A*
    print("A*")
    sh.astar_search(problem=pancakeStackOutOfOrder,verbose = verbose)
    # weighted A*
    print("Weighted A*")
    sh.weighted_astar_search(problem=pancakeStackOutOfOrder,weight=weightAStar,verbose = verbose)
    