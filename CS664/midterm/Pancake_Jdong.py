from search_helpers import Problem, breadth_first_search, astar_search, greedy_bfs, uniform_cost_search
import random

class PancakeProblem(Problem):

    """
    only allowing flipping i and j
    """
    def __init__(self, initial): 
        self.initial, self.goal = tuple(initial), tuple(sorted(initial))

    def actions(self, state):
        result = []
        for i in range(1,len(state)+1):
            for j in range(1, len(state)+1):
                if i!=j:
                    # doesn't make sense to have i=j as a swap
                    result.append('Swap '+str(i)+' '+str(j))
        return result

    def result(self, state, action):
        # the indexing of the list start from 0 to len-1
        #i  = int(action[5]) -1
        #j = int(action[7]) -1
        # split by empty string
        splitString = action.split(' ')
        i,j = int(splitString[1]),int(splitString[2])


        state_ls = list(state)

        curr_i = state_ls[i]

        state_ls[i] = state_ls[j]
        state_ls[j] = curr_i
        return  tuple(state_ls)

    def h(self, node):
        "The gap heuristic."
        s = node.state
        return sum(abs(s[i] - s[i - 1]) > 1 for i in range(1, len(s)))
    def action_cost(self, s, action, s1):
        return abs(int(action[5])- int(action[7]))

BUID = 8916
random.seed(BUID)
N = 7
initial_state = list(range(1, N+1))
random.shuffle(initial_state)
verbose = 1
#should yield [4, 3, 5, 2, 6, 7, 1] as initial sequence
pancakeStack = PancakeProblem(initial_state)
# Modeify the problem for each function for each Question call in place
#Perform BFS, Uniform cost search, Gready BFS, A* 
# BFS
print("BFS: ")
breadth_first_search(problem=pancakeStack,verbose = verbose)
# Uniform cost search
print("Uniform cost search: ")
uniform_cost_search(problem=pancakeStack,verbose = verbose)
# Gready BFS
print("Greedy BFS")
greedy_bfs(problem=pancakeStack,verbose = verbose)
# A*
print("A*")
astar_search(problem=pancakeStack,verbose = verbose)
