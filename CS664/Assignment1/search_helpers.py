import heapq, math
from collections import deque

class Problem:
    """The abstract class for a formal problem. A new domain subclasses this,
    overriding `actions` and `results`, and perhaps other methods.
    The default heuristic is 0 and the default action cost is 1 for all states.
    When you create an instance of a subclass, specify `initial`, and `goal` states 
    (or give an `is_goal` method) and perhaps other keyword args for the subclass."""

    def __init__(self, initial=None, goal=None, **kwds): 
        self.__dict__.update(initial=initial, goal=goal, **kwds) 
        
    def actions(self, state):        raise NotImplementedError
    def result(self, state, action): raise NotImplementedError
    def is_goal(self, state):        return state == self.goal
    def action_cost(self, s, a, s1): return 1
    def h(self, node):               return 0
    
    def __str__(self):
        return '{}({!r}, {!r})'.format(
            type(self).__name__, self.initial, self.goal)
    
#############################################################################

class Node:
    "A Node in a search tree."
    
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.__dict__.update(state=state, parent=parent, action=action, path_cost=path_cost)

    def __len__(self): 
        return 0 if self.parent is None else (1 + len(self.parent))
        
    def __lt__(self, other): 
        return self.path_cost < other.path_cost

    def __repr__(self): 
        return '<Node {}>'.format(self.state) if self.parent is None else \
            ' <Node {}, action {}, cost {}, \n parent {}>'.format(
                self.state, self.action, self.path_cost, repr(self.parent))
    
#############################################################################

failure = Node('failure', path_cost=math.inf) # Indicates an algorithm couldn't find a solution.
cutoff  = Node('cutoff',  path_cost=math.inf) # Indicates iterative deepening search was cut off.

#############################################################################

def expand(problem, node):
    "Expand a node, generating the children nodes."
    s = node.state
    for action in problem.actions(s):
        s1 = problem.result(s, action)
        cost = node.path_cost + problem.action_cost(s, action, s1)
        yield Node(s1, node, action, cost)
        

def path_actions(node):
    "The sequence of actions to get to this node."
    if node.parent is None:
        return []  
    return path_actions(node.parent) + [node.action]


def path_states(node):
    "The sequence of states to get to this node."
    if node in (cutoff, failure, None): 
        return []
    return path_states(node.parent) + [node.state]

#############################################################################

FIFOQueue = deque

LIFOQueue = list

class PriorityQueue:
    """A queue in which the item with minimum f(item) is always popped first."""

    def __init__(self, items=(), key=lambda x: x): 
        self.key = key
        self.items = [] # a heap of (score, item) pairs
        for item in items:
            self.add(item)
         
    def add(self, item):
        """Add item to the queue."""
        pair = (self.key(item), item)
        heapq.heappush(self.items, pair)

    def pop(self):
        """Pop and return the item with min f(item) value."""
        return heapq.heappop(self.items)[1]
    
    def top(self): return self.items[0][1]

    def __len__(self): return len(self.items)

#############################################################################

def breadth_first_search(problem, verbose = 0):
    "Search shallowest nodes in the search tree first."
    
    node = Node(problem.initial)
    frontier = FIFOQueue([node])
    reached = {problem.initial}
    
    expanded_count, queue_count = 0, 0
    
    if problem.is_goal(problem.initial):
        return node
    
    while frontier:
        node = frontier.pop()
        for child in expand(problem, node):
            expanded_count += 1
            s = child.state
            if verbose >= 2: print(f" Expand {expanded_count:>6} : {s}")
            if problem.is_goal(s):
                if verbose >= 1:
                    print(f"**STATS*: Expanded Count = {expanded_count}, Queue Count = {queue_count}, Remaining Frontier Count = {len(frontier)}")
                    print(f"Solution Node:")
                    print(child)
                return child
            if s not in reached:
                queue_count += 1
                reached.add(s)
                frontier.appendleft(child)
    
    return failure

#############################################################################

def best_first_search(problem, f, verbose = 0):
    "Search nodes with minimum f(node) value first."
    
    node = Node(problem.initial)
    frontier = PriorityQueue([node], key=f)
    reached = {problem.initial: node}

    expanded_count, queue_count = 0, 0
    
    while frontier:
        node = frontier.pop()
        if problem.is_goal(node.state):
            if verbose >= 1:
                print(f"**STATS*: Expanded Count = {expanded_count}, Queue Count = {queue_count}, Remaining Frontier Count = {len(frontier)}")
                print(f"Solution Node:")
                print(node)
            return node
    
        for child in expand(problem, node):
            expanded_count += 1
            s = child.state
            if verbose >= 2: print(f" Expand {expanded_count:>6} : {s}")
            if s not in reached or child.path_cost < reached[s].path_cost:
                queue_count += 1
                reached[s] = child
                frontier.add(child)
    
    return failure

#############################################################################

def g(n): 
    return n.path_cost

#############################################################################

def uniform_cost_search(problem, verbose = 0):
    "Search nodes with minimum path cost first."
    
    return best_first_search(problem, f=g, verbose=verbose)

#############################################################################

def greedy_bfs(problem, h=None, verbose = 0):
    """Search nodes with minimum h(n)."""
    
    h = h or problem.h
    return best_first_search(problem, f=h, verbose=verbose)

#############################################################################

def astar_search(problem, h=None, verbose = 0):
    """Search nodes with minimum f(n) = g(n) + h(n)."""
    
    h = h or problem.h
    return best_first_search(problem, f = lambda n: g(n) + h(n), verbose=verbose)

#############################################################################

def weighted_astar_search(problem, h=None, weight=1.4, verbose = 0):
    """Search nodes with minimum f(n) = g(n) + weight * h(n)."""
    
    h = h or problem.h
    return best_first_search(problem, f=lambda n: g(n) + weight * h(n), verbose=verbose)

#############################################################################


#############################################################################


