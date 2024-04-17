import random
import math
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, CheckButtons, TextBox


class Displayable(object):
    """Class that uses 'display'.
    The amount of detail is controlled by max_display_level
    """
    max_display_level = 1   # can be overridden in subclasses or instances

    def display(self,level,*args,**nargs):
        """print the arguments if level is less than or equal to the
        current max_display_level.
        level is an integer.
        the other arguments are whatever arguments print can take.
        """
        if level <= self.max_display_level:
            print(*args, **nargs) 

###

def argmaxall(gen):
    """gen is a generator of (element,value) pairs, where value is a real.
    argmaxall returns a list of all of the elements with maximal value.
    """
    maxv = -math.inf       # negative infinity
    maxvals = []      # list of maximal elements
    for (e,v) in gen:
        if v>maxv:
            maxvals,maxv = [e], v
        elif v==maxv:
            maxvals.append(e)
    return maxvals

def argmaxe(gen):
    """gen is a generator of (element,value) pairs, where value is a real.
    argmaxe returns an element with maximal value.
    If there are multiple elements with the max value, one is returned at random.
    """
    return random.choice(argmaxall(gen))

def argmax(lst):
    """returns maximum index in a list"""
    return argmaxe(enumerate(lst))

def argmaxd(dct):
   """returns the arg max of a dictionary dct"""
   return argmaxe(dct.items())

def select_from_dist(item_prob_dist):
    """ returns a value from a distribution.
    item_prob_dist is an item:probability dictionary, where the
        probabilities sum to 1.
    returns an item chosen in proportion to its probability
    """
    ranreal = random.random()
    for (it,prob) in item_prob_dist.items():
        if ranreal < prob:
            return it
        else:
            ranreal -= prob
    raise RuntimeError(f"{item_prob_dist} is not a probability distribution")

###

class MDP(Displayable):
    """A Markov Decision Process. Must define:
    title a string that gives the title of the MDP
    states the set (or list) of states
    actions the set (or list) of actions
    discount a real-valued discount
    """

    def __init__(self, title, states, actions, discount, init=0):
        self.title = title
        self.states = states
        self.actions = actions
        self.discount = discount
        self.initv = self.V = {s:init for s in self.states}
        self.initq = self.Q = {s: {a: init for a in self.actions} for s in self.states}

    def P(self,s,a):
        """Transition probability function
        returns a dictionary of {s1:p1} such that P(s1 | s,a)=p1. Other probabilities are zero.
        """
        raise NotImplementedError("P")   # abstract method

    def R(self,s,a):
        """Reward function R(s,a)
        returns the expected reward for doing a in state s.
        """
        raise NotImplementedError("R")   # abstract method


###

def vi(self,  n):
        """carries out n iterations of value iteration, updating value function self.V
        Returns a Q-function, value function, policy
        """
        self.display(3,f"calling vi({n})")
        for i in range(n):
            self.Q = {s: {a: self.R(s,a)
                            +self.discount*sum(p1*self.V[s1]
                                                for (s1,p1) in self.P(s,a).items())
                          for a in self.actions}
                     for s in self.states}
            self.V = {s: max(self.Q[s][a] for a in self.actions)
                      for s in self.states}
    
        self.pi = {s: argmaxd(self.Q[s])
                      for s in self.states}
    
        return self.Q, self.V, self.pi

MDP.vi = vi

###

class distribution(dict):
    """A distribution is an item:prob dictionary.
    The only new part is when a new item:pr is added, and item is already there, the values are summed
    """
    def __init__(self,d):
        dict.__init__(self,d)

    def add_prob(self, item, pr):
        if item in self:
            self[item] += pr
        else:
            self[item] = pr
        return self 
###

class ProblemDomain(MDP):
    """A ProblemDomain implements
    self.result(state, action) -> {(reward, state):probability}. 
    Other pairs have probability are zero.
    The probabilities must sum to 1.
    """
    def __init__(self, title, states, actions, discount,
                     initial_state=None, x_dim=0, y_dim = 0,
                     vinit=0, offsets={}):
        """A problem domain
        * title is list of titles
        * states is the list of states
        * actions is the list of actions
        * discount is the discount factor
        * initial_state is the state the agent starts at (for simulation) if known
        * x_dim and y_dim are the dimensions used by the GUI to show the states in 2-dimensions
        * vinit is the initial value
        * offsets is a {action:(x,y)} map which specifies how actions are displayed in GUI
        """
        MDP.__init__(self, title, states, actions, discount)
        if initial_state is not None:
            self.state = initial_state
        else:
            self.state = random.choice(states)
        self.vinit = vinit # value to reset v,q to
        # The following are for the GUI:
        self.x_dim = x_dim
        self.y_dim = y_dim
        self.offsets = offsets

    def state2pos(self,state):
        """When displaying as a grid, this specifies how the state is mapped to (x,y) position.
        The default is for domains where the (x,y) position is the state
        """
        return state
        
    def state2goal(self,state):
        """When displaying as a grid, this specifies how the state is mapped to goal position.
        The default is for domains where there is no goal
        """
        return None
        
    def pos2state(self,pos):
        """When displaying as a grid, this specifies how the state is mapped to (x,y) position.
        The default is for domains where the (x,y) position is the state
        """
        return pos

    def P(self, state, action):
        """Transition probability function
        returns a dictionary of {s1:p1} such that P(s1 | state,action)=p1. 
        Other probabilities are zero.
        """
        res = self.result(state, action)
        acc = 1e-6  # accuracy for test of equality
        assert 1-acc<sum(res.values())<1+acc, f"result({state},{action}) not a distribution, sum={sum(res.values())}"
        dist = distribution({}) 
        for ((r,s),p) in res.items():
            dist.add_prob(s,p)
        return dist

    def R(self, state, action):
        """Reward function R(s,a)
        returns the expected reward for doing a in state s.
        """
        return sum(r*p for ((r,s),p) in self.result(state, action).items())

###

class GridDomain(object):

    def viGUI(self):
        #plt.ion()   # interactive
        fig,self.ax = plt.subplots()
        plt.subplots_adjust(bottom=0.2)
        stepB = Button(plt.axes([0.8,0.05,0.1,0.075]), "step")
        stepB.on_clicked(self.on_step)
        resetB = Button(plt.axes([0.65,0.05,0.1,0.075]), "reset")
        resetB.on_clicked(self.on_reset)
        self.qcheck = CheckButtons(plt.axes([0.2,0.05,0.35,0.075]),
                                       ["show Q-values","show policy"])
        self.qcheck.on_clicked(self.show_vals)
        self.font_box = TextBox(plt.axes([0.1,0.05,0.05,0.075]),"Font:", textalignment="center")
        self.font_box.on_submit(self.set_font_size)
        self.font_box.set_val(str(plt.rcParams['font.size']))
        self.show_vals(None)
        plt.show()

    def set_font_size(self, s):
        plt.rcParams.update({'font.size': eval(s)})
        plt.draw()
        
    def show_vals(self,event):
        self.ax.cla() # clear the axes
        
        array = [[self.V[self.pos2state((x,y))] for x in range(self.x_dim)]
                                             for y in range(self.y_dim)]
        self.ax.pcolormesh([x-0.5  for x in range(self.x_dim+1)],
                               [y-0.5  for y in range(self.y_dim+1)],
                               array, edgecolors='black',cmap='summer')
            # for cmap see https://matplotlib.org/stable/tutorials/colors/colormaps.html
        if self.qcheck.get_status()[1]:  # "show policy"
                for x in range(self.x_dim):
                   for y in range(self.y_dim):
                      state = self.pos2state((x,y))
                      maxv = max(self.Q[state][a] for a in self.actions)
                      for a in self.actions:
                          if self.Q[state][a] == maxv:
                              # draw arrow in appropriate direction
                              xoff, yoff = self.offsets[a]
                              self.ax.arrow(x,y,xoff*2,yoff*2,
                                    color='red',width=0.05, head_width=0.2,
                                    length_includes_head=True)
        if self.qcheck.get_status()[0]:  # "show q-values"
           self.show_q(event)
        else:
           self.show_v(event)
        self.ax.set_xticks(range(self.x_dim))
        self.ax.set_xticklabels(range(self.x_dim))
        self.ax.set_yticks(range(self.y_dim))
        self.ax.set_yticklabels(range(self.y_dim))
        plt.draw()
        
    def on_step(self,event):
        self.step()
        self.show_vals(event)

    def step(self):
        """The default step is one step of value iteration"""
        self.vi(1)

    def show_v(self,event):
        """show values"""
        for x in range(self.x_dim):
            for y in range(self.y_dim):
                state = self.pos2state((x,y))
                self.ax.text(x,y,"{val:.2f}".format(val=self.V[state]),ha='center')

    def show_q(self,event):
        """show q-values"""
        for x in range(self.x_dim):
            for y in range(self.y_dim):
                state = self.pos2state((x,y))
                for a in self.actions:
                    xoff, yoff = self.offsets[a]
                    self.ax.text(x+xoff,y+yoff,
                                 "{val:.2f}".format(val=self.Q[state][a]),ha='center')

    def on_reset(self,event):
       self.V = {s:self.vinit for s in self.states}
       self.Q = {s: {a: self.vinit for a in self.actions} for s in self.states}
       self.show_vals(event)


###


class partyMDP(MDP): 
    """Simple 2-state, 2-Action Partying MDP Example"""
    def __init__(self, discount=0.9):
        states = {'healthy','sick'}
        actions = {'relax', 'party'}
        MDP.__init__(self, "party MDP", states, actions, discount)

    def R(self,s,a):
        "R(s,a)"
        return { 'healthy': {'relax': 7, 'party': 10},
                 'sick':    {'relax': 0, 'party': 2 }}[s][a]

    def P(self,s,a):
        "returns a dictionary of {s1:p1} such that P(s1 | s,a)=p1. Other probabilities are zero."
        phealthy = {  # P('healthy' | s, a)
                     'healthy': {'relax': 0.95, 'party': 0.7},
                     'sick': {'relax': 0.5, 'party': 0.1 }}[s][a]
        return {'healthy':phealthy, 'sick':1-phealthy}

###

class MDPtiny(ProblemDomain, GridDomain):
    def __init__(self, discount=0.9):
        x_dim = 2   # x-dimension
        y_dim = 3
        ProblemDomain.__init__(self,
            "Tiny MDP", # title
            [(x,y) for x in range(x_dim) for y in range(y_dim)], #states
            ['right', 'upC', 'left', 'upR'], #actions
            discount,
            x_dim=x_dim, y_dim = y_dim,
            offsets = {'right':(0.25,0), 'upC':(0,-0.25), 'left':(-0.25,0), 'upR':(0,0.25)}
            )

    def result(self, state, action):
        """return a dictionary of {(r,s):p} where p is the probability of reward r, state s
        a state is an (x,y) pair
        """
        (x,y) = state
        right = (-x,(1,y)) # reward is -1 if x was 1
        left =  (0,(0,y)) if x==1 else [(-1,(0,0)), (-100,(0,1)), (10,(0,0))][y]
        up = (0,(x,y+1)) if y<2 else (-1,(x,y))
        if action == 'right':
            return {right:1}
        elif action == 'upC':
            (r,s) = up
            return {(r-1,s):1}
        elif action == 'left':
           return {left:1}
        elif action == 'upR':
            return distribution({left: 0.1}).add_prob(right,0.1).add_prob(up,0.8)
####

class grid(ProblemDomain, GridDomain):
    """ x_dim * y_dim grid with rewarding states"""
    def __init__(self, discount=0.9, x_dim=10, y_dim=10):
        ProblemDomain.__init__(self,
            "Grid World",
            [(x,y) for x in range(y_dim) for y in range(y_dim)], #states
            ['up', 'down', 'right', 'left'], #actions
            discount,
            x_dim = x_dim, y_dim = y_dim,
            offsets = {'right':(0.25,0), 'up':(0,0.25), 'left':(-0.25,0), 'down':(0,-0.25)})
        self.rewarding_states = {(3,2):-10, (3,5):-5, (8,2):10, (7,7):3 }
        self.fling_states = {(8,2), (7,7)}  # assumed a subset of rewarding_states
 
    def intended_next(self,s,a):
        """returns the (reward, state)  in the direction a.
        This is where the agent will end up if to goes in its intended_direction
             (which it does with probability 0.7).
        """
        (x,y) = s
        if a=='up':
            return (0, (x,y+1)) if y+1 < self.y_dim else (-1, (x,y))
        if a=='down':
            return (0, (x,y-1)) if y > 0 else (-1, (x,y))
        if a=='right':
            return (0, (x+1,y)) if x+1 < self.x_dim else (-1, (x,y))
        if a=='left':
            return (0, (x-1,y)) if x > 0 else (-1, (x,y))

    def result(self,s,a):
        """return a dictionary of {(r,s):p} where p is the probability of reward r, state s.
        a state is an (x,y) pair
        """
        r0 = self.rewarding_states[s] if s in self.rewarding_states else 0
        if s in self.fling_states:
            return {(r0,(0,0)): 0.25, (r0,(self.x_dim-1,0)):0.25,
                        (r0,(0,self.y_dim-1)):0.25, (r0,(self.x_dim-1,self.y_dim-1)):0.25}
        dist = distribution({})
        for a1 in self.actions:
            (r1,s1) = self.intended_next(s,a1)
            rs = (r1+r0, s1)
            p = 0.7 if a1==a else 0.1
            dist.add_prob(rs,p)
        return dist

###

class Monster_game(ProblemDomain, GridDomain):

    vwalls = [(0,3), (0,4), (1,4)]  # vertical walls right of these locations
    crash_reward = -1
    
    prize_locs = [(0,0), (0,4), (4,0), (4,4)]
    prize_apears_prob = 0.3
    prize_reward = 10

    monster_locs = [(0,1), (1,1), (2,3), (3,1), (4,2)]
    monster_appears_prob = 0.4
    monster_reward_when_damaged = -10
    repair_stations = [(1,4)]

    def __init__(self, discount=0.9):
        x_dim = 5
        y_dim = 5
            # which damaged and prize to show
        ProblemDomain.__init__(self,
            "Monster Game",
            [(x,y,damaged,prize)
                 for x in range(x_dim)
                 for y in range(y_dim)
                 for damaged in [False,True]
                 for prize in [None]+self.prize_locs], #states
            ['up', 'down', 'right', 'left'], #actions
            discount,
            x_dim = x_dim, y_dim = y_dim,
            offsets = {'right':(0.25,0), 'up':(0,0.25), 'left':(-0.25,0), 'down':(0,-0.25)})
        self.state = (2,2,False,None)
        
    def intended_next(self,xy,a):
        """returns the (reward, (x,y))  in the direction a.
        This is where the agent will end up if to goes in its intended_direction
             (which it does with probability 0.7).
        """
        (x,y) = xy # original x-y position
        if a=='up':
            return (0, (x,y+1)) if y+1 < self.y_dim else (self.crash_reward, (x,y))
        if a=='down':
            return (0, (x,y-1)) if y > 0 else (self.crash_reward, (x,y))
        if a=='right':
            if (x,y) in self.vwalls or x+1==self.x_dim: # hit wall
                return (self.crash_reward, (x,y))
            else:
                return (0, (x+1,y)) 
        if a=='left':
            if (x-1,y) in self.vwalls or x==0: # hit wall
                            return (self.crash_reward, (x,y))
            else:
                return (0, (x-1,y)) 

    def result(self,s,a):
        """return a dictionary of {(r,s):p} where p is the probability of reward r, state s.
        a state is an (x,y) pair
        """
        (x,y,damaged,prize) = s
        dist = distribution({})
        for a1 in self.actions: # possible results
            mp = 0.7 if a1==a else 0.1
            mr,(xn,yn) = self.intended_next((x,y),a1)
            if (xn,yn) in self.monster_locs:
                if damaged:
                    dist.add_prob((mr+self.monster_reward_when_damaged,(xn,yn,True,prize)), mp*self.monster_appears_prob)
                    dist.add_prob((mr,(xn,yn,True,prize)), mp*(1-self.monster_appears_prob))
                else:
                   dist.add_prob((mr,(xn,yn,True,prize)), mp*self.monster_appears_prob)
                   dist.add_prob((mr,(xn,yn,False,prize)), mp*(1-self.monster_appears_prob))
            elif (xn,yn) == prize:
                dist.add_prob((mr+self.prize_reward,(xn,yn,damaged,None)), mp)
            elif (xn,yn) in self.repair_stations:
                dist.add_prob((mr,(xn,yn,False,prize)), mp)
            else:
                dist.add_prob((mr,(xn,yn,damaged,prize)), mp)
        if prize is None:
            res = distribution({})
            for (r,(x2,y2,d,p2)),p in dist.items():
                res.add_prob((r,(x2,y2,d,None)), p*(1-self.prize_apears_prob))
                for pz in self.prize_locs:
                    res.add_prob((r,(x2,y2,d,pz)), p*self.prize_apears_prob/len(self.prize_locs))
            return res
        else:
            return dist
            
    def state2pos(self, state):
        """When displaying as a grid, this specifies how the state is mapped to (x,y) position.
        The default is for domains where the (x,y) position is the state
        """
        (x,y,d,p) = state
        return (x,y)
        
    def pos2state(self, pos):
        """When displaying as a grid, this specifies how the state is mapped to (x,y) position.
        """
        (x,y) = pos
        (xs, ys, damaged, prize) = self.state
        return (x, y, damaged, prize)
        
    def state2goal(self,state):
        """the (x,y) position for the goal
        """
        (x, y, damaged, prize) = state
        return prize


###




