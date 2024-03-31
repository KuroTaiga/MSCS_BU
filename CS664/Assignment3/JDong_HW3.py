from ortools.sat.python import cp_model
"""
Exams:
programming exam: gives initial code, can use reference
review the game (HW2)

paper:
how agorithm reduce the domain - constrain
when give a tree, mini max/ alpha beta proning, how those algorithms are done - game

module 1
programming: refer to HW1
paper: 
review A* and other search algorithms (from root to node, from node to the end) how the algorithm
go through the tree
(when given the tree, how the algorithm will go through and search)

basically how would things work

no reference for paper, can use reference for programming 
5*1opt, programming: one from each section
"""


from csp_helpers import *
# Alice = 0
# Bob = 0
# Chalie = 0
# Dave = 0
# var_List = [Alice,Bob,Chalie,Dave]
# neighbors = parse_neighbors('Alice: Bob, Chalie, Dave; Bob: Alice, Chalie, Dave; Chalie: Alice, Bob, Dave; Dave: Alice, Bob, Chalie')
# domains = {'Alice': [1, 2, 3, 4], 'Bob': [1, 2, 3, 4], 'Chalie':[1,2,3,4], 'Dave':[1,2,3,4]}
def Housing_constrain(A,a,B,b):
    if a==b:
        return False
    if A == 'Dave' and B == 'Bob':
        if a >b : return False
    if B == 'Dave' and A == 'Bob':
        if a <b : return False
    if (A == 'Chalie' and B == 'Bob')or (B == 'Chalie' and A == 'Bob'):
        if abs(a-b) == 1 : return False
    if A == 'Alice' and B == 'Bob':
        if a-b != -1: return False
    if A == 'Bob' and B == 'Alice':
        if a-b != 1: return False
    if A == 'Chalie' and a == 4: return False
    if B == 'Chalie' and b == 4: return False
    if A == 'Dave' and a == 2: return False
    if B == 'Dave' and b == 2: return False
    return True
def HousingCSP(values, neighbors):
    if isinstance(neighbors, str):
        neighbors = parse_neighbors(neighbors)
    
    return CSP(list(neighbors.keys()), 
               UniversalDict(values), neighbors, 
               Housing_constrain)
HW3_CSP = HousingCSP([1,2,3,4],
                     """Alice: Bob Chalie Dave; Bob: Chalie Dave; Chalie: Dave""")
def neq_c(x,y):
    return x!=y
def oneLess_c(x,y):
    return x-y ==-1
def oneMore_c(x,y):
    return x-y ==1
def toLeft_c(x,y):
    return x<y
def toRight_c(x,y):
    return x>y
def notNeighbor_c(x,y):
    return abs(x-y)>1
cmap = {('Alice','Bob'): [oneLess_c], ('Bob', 'Alice'):[oneMore_c],
        ('Alice','Chalie'):[neq_c],('Alice','Dave'):[neq_c],('Chalie','Alice'):[neq_c],('Dave','Alice'):[neq_c],
        ('Bob','Chalie'):[notNeighbor_c],('Chalie','Bob'):[notNeighbor_c],
        ('Bob','Dave'):[toRight_c],('Dave','Bob'):[toLeft_c],
        ('Chalie','Dave'):[neq_c],('Dave','Chalie'):[neq_c]}
def check_constrains(X,x,Y,y):
    global cmap
    return all(constraint(x,y) for constraint in cmap[(X,Y)])
def HousingProfCSP(values, neighbors):
    if isinstance(neighbors, str):
        neighbors = parse_neighbors(neighbors)
    
    return CSP(list(neighbors.keys()), 
               {'Alice':[1,2,3,4],'Bob':[1,2,3,4],'Chalie':[1,2,3],'Dave':[1,3,4]}, neighbors, 
               check_constrains)

HW3_Prof_wayCSP = HousingProfCSP([1,2,3,4],
                                 """Alice: Bob Chalie Dave; Bob: Chalie Dave; Chalie: Dave""")

print("This is my implementation")
random.seed(123)
#min_conflicts(make_instru(HW3_CSP))
backtracking_search(make_instru(HW3_CSP), inference = mac)

random.seed(0)
print("This is the way shown in class")
#min_conflicts(make_instru(HW3_Prof_wayCSP))
backtracking_search(make_instru(HW3_Prof_wayCSP),inference = mac)
