import random
import math
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, CheckButtons, TextBox


from mdp_helpers import MDPtiny, partyMDP, Monster_game

def flip(prob):
    """return true with probability prob"""
    return random.random() < prob

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

#####

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

####

class Agent(Displayable):

    def initial_action(self, percept):
        """return the initial action."""
        return self.select_action(percept)   # same as select_action

    def select_action(self, percept):
        """return the next action (and update internal state) given percept
        percept is variable:value dictionary
        """
        raise NotImplementedError("go")   # abstract method

 ###

class Environment(Displayable):
    def initial_percept(self):
        """returns the initial percept for the agent"""
        raise NotImplementedError("initial_percept")   # abstract method

    def do(self, action):
        """does the action in the environment
        returns the next percept """
        raise NotImplementedError("Environment.do")   # abstract method

 ###

class RL_env(Environment):
    def __init__(self, name, actions, state):
        """creates an environment given name, list of actions, and initial state"""
        self.name = name         # the role for an agent 
        self.actions = actions   # list of all actions
        self.state = state       # initial state
        self.reward = None       # last reward

    # must implement do(action)->(reward,state)

###

class RL_agent(Agent):
    """An RL_Agent 
    has percepts (s, r) for some state s and real reward r
    """
    def __init__(self, actions):
       self.actions = actions

    def initial_action(self, env_state):
        """return the initial action, and remember the state and action
        Act randomly initially
        Could be overridden to initialize data structures (as the agent now knows about one state)
        """
        self.state = env_state
        self.action = random.choice(self.actions)
        return self.action

    def select_action(self, reward, state):
        """ 
        Select the action given the reward and next state
        Remember the action in self.action
        This implements "Act randomly" and should  be overridden!
        """
        self.reward = reward
        self.action = random.choice(self.actions)
        return self.action

    def v(self, state):
        "v needed for GUI; an agent must also implement q()"
        return max(self.q(state,a) for a in self.actions)

###

class Simulate(Displayable):
    """simulate the interaction between the agent and the environment
    for n time steps.
    Returns a pair of the agent state and the environment state.
    """
    def __init__(self, agent, environment):
        self.agent = agent
        self.env = environment
        self.reward_history = []  # for plotting
        self.step = 0
        self.sum_rewards = 0

    def start(self):
        self.action = self.agent.initial_action(self.env.state)
        return self

    def go(self, n):
        for i in range(n):
            self.step += 1
            (reward,state) = self.env.do(self.action)
            self.display(2,f"step={self.step} reward={reward}, state={state}")
            self.sum_rewards += reward
            self.reward_history.append(reward)
            self.action = self.agent.select_action(reward,state)
            self.display(2,f"      action={self.action}")
        return self

    def plot(self, label=None, step_size=None, xscale='linear'):
        """
        plots the rewards history in the simulation
        label is the label for the plot
        step_size is the number of steps between each point plotted
        xscale is 'log' or 'linear'

        returns sum of rewards
        """
        if step_size is None: #for long simulations (> 999), only plot some points
            step_size = max(1,len(self.reward_history)//500)
        if label is None:
            label = self.agent.method
        plt.ion()
        plt.xscale(xscale)
        plt.xlabel("step")
        plt.ylabel("Sum of rewards")
        sum_history, sum_rewards = acc_rews(self.reward_history, step_size)
        plt.plot(range(0,len(self.reward_history),step_size), sum_history, label=label)
        plt.legend()
        plt.draw()
        return sum_rewards

def acc_rews(rews,step_size):
    """returns the rolling sum of the values, sampled each step_size, and the sum
    """
    acc = []
    sumr = 0; i=0
    for e in rews:
       sumr += e
       i += 1
       if (i%step_size == 0): 
           acc.append(sumr)
    return acc, sumr

###

class Party_env(RL_env):
    def __init__(self):
        RL_env.__init__(self, "Party Decision", ["party", "relax"], "healthy")

    def do(self, action):
        """updates the state based on the agent doing action.
        returns reward,state
        """
        if self.state=="healthy":
            if action=="party":
                self.state = "healthy" if flip(0.7) else "sick"
                self.reward = 10
            else:  # action=="relax"
                self.state = "healthy" if flip(0.95) else "sick"
                self.reward = 7
        else:  # self.state=="sick"
            if action=="party":
                self.state = "healthy" if flip(0.1) else "sick"
                self.reward = 2
            else:
                self.state = "healthy" if flip(0.5) else "sick"
                self.reward = 0
                
        return self.reward, self.state

###

class Env_from_ProblemDomain(RL_env):
    def __init__(self, prob_dom):
        RL_env.__init__(self, prob_dom.title, prob_dom.actions, prob_dom.state)
        self.problem_domain = prob_dom
        self.state = prob_dom.state
        self.x_dim = prob_dom.x_dim
        self.y_dim = prob_dom.y_dim 
        self.offsets = prob_dom.offsets
        self.state2pos = self.problem_domain.state2pos
        self.state2goal = self.problem_domain.state2goal
        self.pos2state = self.problem_domain.pos2state
        
    def do(self, action):
        """updates the state based on the agent doing action.
        returns state,reward
        """
        (self.reward, self.state) = select_from_dist(
            self.problem_domain.result(self.state, action))
        
        self.problem_domain.state = self.state
        self.display(2,f"do({action} -> ({self.reward}, {self.state})")
        return (self.reward, self.state)


####

class Monster_game_env(RL_env):
    x_dim = 5
    y_dim = 5

    vwalls = [(0,3), (0,4), (1,4)]  # vertical walls right of these locations
    hwalls = [] # not implemented
    crashed_reward = -1
    
    prize_locs = [(0,0), (0,4), (4,0), (4,4)]
    prize_apears_prob = 0.3
    prize_reward = 10

    monster_locs = [(0,1), (1,1), (2,3), (3,1), (4,2)]
    monster_appears_prob = 0.4
    monster_reward_when_damaged = -10
    repair_stations = [(1,4)]

    actions = ["up","down","left","right"]
    
    def __init__(self):
        # State:
        self.x = 2
        self.y = 2
        self.damaged = False
        self.prize = None
        # Statistics
        self.number_steps = 0
        self.accumulated_rewards = 0   # sum of rewards received
        self.min_accumulated_rewards = 0
        self.min_step = 0
        self.zero_crossing = 0
        RL_env.__init__(self, "Monster Game", self.actions, (self.x, self.y, self.damaged, self.prize))
        self.display(2,"","Step","Tot Rew","Ave Rew",sep="\t")

    def do(self,action):
        """updates the state based on the agent doing action.
        returns reward,state
        """
        assert action in self.actions, f"Monster game, unknown action: {action}"
        
        self.reward = 0.0
        
        # A prize can appear:
        if self.prize is None and flip(self.prize_apears_prob):
                self.prize = random.choice(self.prize_locs)
        
        # Actions can be noisy
        if flip(0.4):
            actual_direction = random.choice(self.actions)
        else:
            actual_direction = action
        
        # Modeling the actions given the actual direction
        if actual_direction == "right":
            if self.x==self.x_dim-1 or (self.x,self.y) in self.vwalls:
                self.reward += self.crashed_reward
            else:
                self.x += 1
        elif actual_direction == "left":
            if self.x==0 or (self.x-1,self.y) in self.vwalls:
                self.reward += self.crashed_reward
            else:
                self.x += -1
        elif actual_direction == "up":
            if self.y==self.y_dim-1:
                self.reward += self.crashed_reward
            else:
                self.y += 1
        elif actual_direction == "down":
            if self.y==0:
                self.reward += self.crashed_reward
            else:
                self.y += -1
        else:
            raise RuntimeError(f"unknown_direction: {actual_direction}")

        # Monsters
        if (self.x,self.y) in self.monster_locs and flip(self.monster_appears_prob):
            if self.damaged:
                self.reward += self.monster_reward_when_damaged
            else:
                self.damaged = True
        if (self.x,self.y) in self.repair_stations:
            self.damaged = False

        # Prizes
        if (self.x,self.y) == self.prize:
            self.reward += self.prize_reward
            self.prize = None

        # Statistics
        self.number_steps += 1
        self.accumulated_rewards += self.reward
        if self.accumulated_rewards < self.min_accumulated_rewards:
            self.min_accumulated_rewards = self.accumulated_rewards
            self.min_step = self.number_steps
        if self.accumulated_rewards>0 and self.reward>self.accumulated_rewards:
            self.zero_crossing = self.number_steps
        
        self.display(2,"",self.number_steps,self.accumulated_rewards,
                      self.accumulated_rewards/self.number_steps,sep="\t")

        return self.reward, (self.x, self.y, self.damaged, self.prize)
        
    ### For GUI
    def state2pos(self,state):
        """the (x,y) position for the state
        """
        (x, y, damaged, prize) = state
        return (x,y)
        
    def state2goal(self,state):
        """the (x,y) position for the goal
        """
        (x, y, damaged, prize) = state
        return prize
        
    def pos2state(self,pos):
        """the state corresponding to the (x,y) position.
        The damages and prize are not shown in the GUI
        """
        (x,y) = pos
        return (x, y, self.damaged, self.prize)
        
###

def epsilon_greedy(state, Qs, Vs={}, epsilon=0.2):
        """select action given epsilon greedy
        Qs is the {action:Q-value} dictionary for current state
        Vs is ignored
        epsilon is the probability of acting randomly
        """
        if flip(epsilon):
            return random.choice(list(Qs.keys())) # act randomly
        else:
            return argmaxd(Qs) # pick an action with max Q

###

def ucb(state, Qs, Vs, c=1.4):
        """select action given upper-confidence bound
        Qs is the  {action:Q-value} dictionary for current state
        Vs is the {action:visits} dictionary for current state

        0.01 is to prevent divide-by zero when Vs[a]==0
        """
        Ns = sum(Vs.values())
        ucb1 = {a:Qs[a]+c*math.sqrt(Ns/(0.01+Vs[a]))
                    for a in Qs.keys()}
        action = argmaxd(ucb1)
        return action

###

class Q_learner(RL_agent):
    """A Q-learning agent has
    belief-state consisting of
        state is the previous state (initialized by RL_agent
        q is a {(state,action):value} dict
        visits is a {(state,action):n} dict.  n is how many times action was done in state
        acc_rewards is the accumulated reward
    """
    
    def __init__(self, role, actions, discount,
                 exploration_strategy=epsilon_greedy, es_kwargs={},
                 alpha_fun=lambda _:0.2,
                 Qinit=0, method="Q_learner"):
        """
        role is the role of the agent (e.g., in a game)
        actions is the set of actions the agent can do
        discount is the discount factor
        exploration_strategy is the exploration function, default "epsilon_greedy"
        es_kwargs is extra arguments of exploration_strategy 
        alpha_fun is a function that computes alpha from the number of visits
        Qinit is the initial q-value
        method gives the method used to implement the role (for plotting)
        """
        RL_agent.__init__(self, actions)
        self.role = role
        self.discount = discount
        self.exploration_strategy = exploration_strategy
        self.es_kwargs = es_kwargs
        self.alpha_fun = alpha_fun
        self.Qinit = Qinit
        self.method = method
        self.acc_rewards = 0
        self.Q = {}
        self.visits = {}

    def initial_action(self, state):
        """ Returns the initial action; selected at random
        Initialize Data Structures
        """
        self.state = state
        self.Q[state] = {act:self.Qinit for act in self.actions}
        self.visits[state] = {act:0 for act in self.actions}
        self.action = self.exploration_strategy(state, self.Q[state],
                                     self.visits[state],**self.es_kwargs)
        self.display(2, f"Initial State: {state} Action {self.action}")
        self.display(2,"s\ta\tr\ts'\tQ")
        return self.action
        
    def select_action(self, reward, next_state):
        """give reward and next state, select next action to be carried out"""
        if next_state not in self.visits:  # next state not seen before
            self.Q[next_state] = {act:self.Qinit for act in self.actions}
            self.visits[next_state] = {act:0 for act in self.actions}
        self.visits[self.state][self.action] +=1
        alpha = self.alpha_fun(self.visits[self.state][self.action])
        self.Q[self.state][self.action] += alpha*(
                            reward
                            + self.discount * max(self.Q[next_state].values())
                            - self.Q[self.state][self.action])
        self.display(2,self.state, self.action, reward, next_state, 
                     self.Q[self.state][self.action], sep='\t')
        self.action = self.exploration_strategy(next_state, self.Q[next_state],
                                     self.visits[next_state],**self.es_kwargs)
        self.state = next_state
        self.display(3,f"Agent {self.role} doing {self.action} in state {self.state}")
        return self.action

    def q(self,s,a):
        if s in self.Q and a in self.Q[s]:
            return self.Q[s][a]
        else:
            return self.Qinit
            
    def v(self,s):
        if s in self.Q:
            return max(self.Q[s].values())
        else:
            return self.Qinit
    
###

class SARSA(Q_learner):
    def __init__(self,*args, **nargs):
        Q_learner.__init__(self,*args, **nargs)
        self.method = "SARSA"
        
    def select_action(self, reward, next_state):
        """give reward and next state, select next action to be carried out"""
        if next_state not in self.visits:  # next state not seen before
            self.Q[next_state] = {act:self.Qinit for act in self.actions}
            self.visits[next_state] = {act:0 for act in self.actions}
        self.visits[self.state][self.action] +=1
        alpha = self.alpha_fun(self.visits[self.state][self.action])
        next_action = self.exploration_strategy(next_state, self.Q[next_state],
                                     self.visits[next_state],**self.es_kwargs)
        self.Q[self.state][self.action] += alpha*(
                            reward
                            + self.discount * self.Q[next_state][next_action]
                            - self.Q[self.state][self.action])
        self.display(2,self.state, self.action, reward, next_state, 
                     self.Q[self.state][self.action], sep='\t')
        self.state = next_state
        self.action = next_action
        self.display(3,f"Agent {self.role} doing {self.action} in state {self.state}")
        return self.action

###

class rlGUI(object):
    def __init__(self, env, agent):
        """
        """
        self.env = env
        self.agent = agent
        self.state = self.env.state
        self.x_dim = env.x_dim
        self.y_dim = env.y_dim
        if 'offsets' in vars(env):  # 'offsets' is defined in environment
            self.offsets = env.offsets
        else: # should be more general
            self.offsets = {'right':(0.25,0), 'up':(0,0.25), 'left':(-0.25,0), 'down':(0,-0.25)}
        # replace the exploration strategy with GUI
        self.orig_exp_strategy = self.agent.exploration_strategy
        self.agent.exploration_strategy = self.actionFromGUI
        self.do_steps = 0
        self.quit = False
        self.action = None

    def go(self):
        self.q = self.agent.q
        self.v = self.agent.v
        try:
            self.fig,self.ax = plt.subplots()
            plt.subplots_adjust(bottom=0.2)
            self.actButtons = {self.fig.text(0.8+self.offsets[a][0]*0.4,0.1+self.offsets[a][1]*0.1,a,
                                    bbox={'boxstyle':'square','color':'yellow','ec':'black'},
                                    picker=True):a #, fontsize=fontsize):a
                 for a in self.env.actions}
            self.fig.canvas.mpl_connect('pick_event', self.sel_action)
            self.sim = Simulate(self.agent, self.env)
            self.show()
            self.sim.start()
            self.sim.go(1000000000000) # go forever
        except ExitGUI:
            plt.close()



    def show(self):
        #plt.ion()   # interactive (why doesn't this work?)
        self.qcheck = CheckButtons(plt.axes([0.2,0.05,0.25,0.075]),
                                       ["show q-values","show policy","show visits"])
        self.qcheck.on_clicked(self.show_vals)
        self.font_box = TextBox(plt.axes([0.125,0.05,0.05,0.05]),"Font:", textalignment="center")
        self.font_box.on_submit(self.set_font_size)
        self.font_box.set_val(str(plt.rcParams['font.size']))
        self.step_box = TextBox(plt.axes([0.5,0.05,0.1,0.05]),"", textalignment="center")
        self.step_box.set_val("100")
        self.stepsButton = Button(plt.axes([0.6,0.05,0.075,0.05]), "steps", color='yellow')
        self.stepsButton.on_clicked(self.steps)
        self.exitButton = Button(plt.axes([0.0,0.05,0.05,0.05]), "exit", color='yellow')
        self.exitButton.on_clicked(self.exit)
        self.show_vals(None)

    def set_font_size(self, s):
        plt.rcParams.update({'font.size': eval(s)})
        plt.draw()

    def exit(self, s):
        self.quit = True
        raise ExitGUI
        
    def show_vals(self,event):
        self.ax.cla()
        self.ax.set_title(f"{self.sim.step}: State: {self.state} Reward: {self.env.reward} Sum rewards: {self.sim.sum_rewards}")
        array = [[self.v(self.env.pos2state((x,y))) for x in range(self.x_dim)]
                                             for y in range(self.y_dim)]
        self.ax.pcolormesh([x-0.5  for x in range(self.x_dim+1)],
                               [x-0.5  for x in range(self.y_dim+1)],
                               array, edgecolors='black',cmap='summer')
            # for cmap see https://matplotlib.org/stable/tutorials/colors/colormaps.html
        if self.qcheck.get_status()[1]:  # "show policy"
                for x in range(self.x_dim):
                    for y in range(self.y_dim):
                       state = self.env.pos2state((x,y))
                       maxv = max(self.agent.q(state,a) for a in self.env.actions)
                       for a in self.env.actions:
                           xoff, yoff = self.offsets[a]
                           if self.agent.q(state,a) == maxv:
                              # draw arrow in appropriate direction
                              self.ax.arrow(x,y,xoff*2,yoff*2,
                                    color='red',width=0.05, head_width=0.2, length_includes_head=True)
        
        if goal := self.env.state2goal(self.state):
            self.ax.add_patch(plt.Circle(goal, 0.1, color='lime'))
        self.ax.add_patch(plt.Circle(self.env.state2pos(self.state), 0.1, color='w'))
        if self.qcheck.get_status()[0]:  # "show q-values"
           self.show_q(event)
        elif self.qcheck.get_status()[2] and 'visits' in vars(self.agent):  # "show visits"
           self.show_visits(event)
        else:
           self.show_v(event)
        self.ax.set_xticks(range(self.x_dim))
        self.ax.set_xticklabels(range(self.x_dim))
        self.ax.set_yticks(range(self.y_dim))
        self.ax.set_yticklabels(range(self.y_dim))
        plt.draw()
        
    def sel_action(self,event):
        self.action = self.actButtons[event.artist]

    def show_v(self,event):
        """show values"""
        for x in range(self.x_dim):
            for y in range(self.y_dim):
                state = self.env.pos2state((x,y))
                self.ax.text(x,y,"{val:.2f}".format(val=self.agent.v(state)),ha='center')

    def show_q(self,event):
        """show q-values"""
        for x in range(self.x_dim):
            for y in range(self.y_dim):
                state = self.env.pos2state((x,y))
                for a in self.env.actions:
                    xoff, yoff = self.offsets[a]
                    self.ax.text(x+xoff,y+yoff,
                                 "{val:.2f}".format(val=self.agent.q(state,a)),ha='center')

    def show_visits(self,event):
        """show q-values"""
        for x in range(self.x_dim):
            for y in range(self.y_dim):
                state = self.env.pos2state((x,y))
                for a in self.env.actions:
                    xoff, yoff = self.offsets[a]
                    if state in self.agent.visits and a in self.agent.visits[state]:
                        num_visits = self.agent.visits[state][a]
                    else:
                        num_visits = 0
                    self.ax.text(x+xoff,y+yoff,
                                 str(num_visits),ha='center')
                                 
    def steps(self,event):
        "do the steps given in step box"
        num_steps = int(self.step_box.text)
        if num_steps > 0:
            self.do_steps = num_steps-1
            self.action = self.action_from_orig_exp_strategy()

    def action_from_orig_exp_strategy(self):
        """reutns the action from the original explorations strategy"""
        visits = self.agent.visits[self.state] if 'visits' in vars(self.agent) else {}
        return self.orig_exp_strategy(self.state,{a:self.agent.q(self.state,a) for a in self.agent.actions},
                                     visits,**self.agent.es_kwargs)
        
    def actionFromGUI(self, state, *args, **kwargs):
        """called as the exploration strategy by the RL agent. 
        returns an action, either from the GUI or the original exploration strategy
        """
        self.state = state
        if self.do_steps > 0:  # use the original
            self.do_steps -= 1
            return self.action_from_orig_exp_strategy()
        else:  # get action from the user
            self.show_vals(None)
            while self.action == None and not self.quit: #wait for user action
                plt.pause(0.05) # controls reaction time of GUI
            act = self.action
            self.action = None
            return act

class ExitGUI(Exception):
    pass



###



env = Env_from_ProblemDomain(MDPtiny())
# Some RL agents with different parameters:
ag = Q_learner(env.name, env.actions, 0.7, method="eps (0.1) greedy" )
ag_ucb = Q_learner(env.name, env.actions, 0.7, exploration_strategy = ucb, es_kwargs={'c':0.1}, method="ucb")
ag_opt = Q_learner(env.name, env.actions, 0.7, Qinit=100,  es_kwargs={'epsilon':0}, method="optimistic" )
ag_exp_m = Q_learner(env.name, env.actions, 0.7, es_kwargs={'epsilon':0.5}, method="more explore")
ag_greedy = Q_learner(env.name, env.actions, 0.1, Qinit=100, method="disc 0.1")
sa = SARSA(env.name, env.actions, 0.9, method="SARSA")
sucb = SARSA(env.name, env.actions, 0.9, exploration_strategy = ucb, es_kwargs={'c':1}, method="SARSA ucb")

sim_ag = Simulate(ag,env).start()

sim_ag.go(1000)
ag.Q    # get the learned Q-values
#sim_ag.plot()
#sim_ucb = Simulate(ag_ucb,env).start(); sim_ucb.go(1000); sim_ucb.plot()
#Simulate(ag_opt,env).start().go(1000).plot()
#Simulate(ag_exp_m,env).start().go(1000).plot()
#Simulate(ag_greedy,env).start().go(1000).plot()
#Simulate(sa,env).start().go(1000).plot()
#Simulate(sucb,env).start().go(1000).plot()

###

##### Monster Game ####
mon_env = Monster_game_env()
mag1 = Q_learner(mon_env.name, mon_env.actions, 0.9,
                     method="alpha=0.2")
#Simulate(mag1,mon_env).start().go(100000).plot()
mag_ucb = Q_learner(mon_env.name, mon_env.actions, 0.9,
                        exploration_strategy = ucb, es_kwargs={'c':0.1}, method="UCB(0.1),alpha=0.2")
#Simulate(mag_ucb,mon_env).start().go(100000).plot()

mag2 = Q_learner(mon_env.name, mon_env.actions, 0.9,
                     alpha_fun=lambda k:1/k,method="alpha=1/k")
#Simulate(mag2,mon_env).start().go(100000).plot()
mag3 = Q_learner(mon_env.name, mon_env.actions, 0.9,
                     alpha_fun=lambda k:10/(9+k), method="alpha=10/(9+k)")
#Simulate(mag3,mon_env).start().go(100000).plot()

mag4 = Q_learner(mon_env.name, mon_env.actions, 0.9,
                 alpha_fun=lambda k:10/(9+k),
                 exploration_strategy = ucb, es_kwargs={'c':0.1},
                 method="ucb & alpha=10/(9+k)")
#Simulate(mag4,mon_env).start().go(100000).plot()


#########

env = Env_from_ProblemDomain(MDPtiny())
env = Env_from_ProblemDomain(Monster_game())
env = Monster_game_env()
#gui = rlGUI(env, Q_learner("Q", env.actions, 0.9)); gui.go()
# gui = rlGUI(env, SARSA("Q", env.actions, 0.9)); gui.go()
# gui = rlGUI(env, SARSA("Q", env.actions, 0.9, alpha_fun=lambda k:10/(9+k))); gui.go()
gui = rlGUI(env, SARSA("SARSA-UCB", env.actions, 0.9, exploration_strategy = ucb, es_kwargs={'c':0.1})); gui.go()


