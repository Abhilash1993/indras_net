"""
Filename: entity.py
Author: Gene Callahan and Brandon Logan
This module contains the base classes for agent-based modeling in Indra.
"""

from abc import ABCMeta, abstractmethod
import time
import logging
import pprint
import pdb
import random
import getpass
from collections import deque
import prop_args as pa


RUN_MODE  = 0
STEP_MODE = 1
INSP_MODE = 2
VISL_MODE = 3
CODE_MODE = 4
DBUG_MODE = 5
LIST_MODE = 6
QUIT_MODE = 7
PLOT_MODE = 8
EXMN_MODE = 9
WRIT_MODE = 10


pp = pprint.PrettyPrinter(indent=4)

def join_entities(prehender, rel, prehended):
    prehender.add_prehension(Prehension(rel, prehended))


class Entity:
    """
    This is the base class of all agents AND environments.
    """

    universals  = {}
    
    @classmethod
    def create_first_prehension(cls, prehended):
        vals = []
        vals.append(prehended)
        return vals


    @classmethod
    def get_class_name(cls, genera):
        return genera.__name__


    @classmethod
    def get_agent_type(self, agent):
        return(self.get_class_name(type(agent)))

            

    @classmethod
    def add_universal(cls, prehender, universal, prehended):
        prehender_type_name = cls.get_class_name(prehender)
        prehended_type_name = cls.get_class_name(prehended)
        if universal not in cls.universals:
            cls.universals[universal] = \
                {prehender_type_name:
                    cls.create_first_prehension(prehended)}
            logging.info(pp.pformat(cls.universals))
        elif prehender not in cls.universals[universal]:
            cls.universals[universal][prehender_type_name] = \
                cls.create_first_prehension(prehended)
            logging.info(pp.pformat(cls.universals))
        else:
            cls.universals[universal][prehender_type_name].append(
                        prehended)


    @classmethod
    def get_universal_instances(cls, prehender, universal):
        if universal in cls.universals:
            prehnder_cls = cls.get_class_name(prehender)
            if prehnder_cls in cls.universals[universal]:
                return cls.universals[universal][prehnder_cls]
            else:
                return None
        else:
            return None


    def __init__(self, name):
        self.name        = name
        self.prehensions = []
        self.env = None
        
    def add_env(self, env):
        self.env = env


    def __str__(self):
        return self.name


    def walk_graph_breadth_first(self, func, top):
        if top:
            func(self)
        for prehension in self.prehensions:
            func(prehension.prehended_entity)
        for prehension in self.prehensions:
            prehension.prehended_entity.walk_graph_breadth_first(func, 
                                                  False)


    def add_prehension(self, pre):
        self.prehensions.append(pre)


    def print_prehensions(self):
        for prehension in self.prehensions:
            print(prehension.prehended_entity.name 
                + " is my " + prehension.name)


    def pprint(self):
        for key, value in self.__dict__.items():
            print(key + " = " + str(value))


class Agent(Entity):

    """
    This class adds a goal to an entity and is the base for all other agents.
    """

    def __init__(self, name, goal=None):
        super().__init__(name)
        self.goal = goal


    @abstractmethod
    def act(self):
        pass

    def preact(self):
        pass
    
    def postact(self):
        pass
    

class User(Entity):
    """
    We will represent the user to the system as another entity.
    """

    # user types
    IPYTHON = "iPython"


    def __init__(self, nm, type):
        super().__init__(nm)
        self.type = type


    def tell(self, msg):
        if self.type == User.IPYTHON:
            print(msg)


    def ask(self, msg):
        if self.type == User.IPYTHON:
            return(input(msg))


class Environment(Entity):

    """
    A basic environment allowing starting, stopping, stepping, etc.
    """

    prev_period = 0  # in case we need to restore state

    keymap = { "c": CODE_MODE,
               "d": DBUG_MODE,
               "e": EXMN_MODE,
               "i": INSP_MODE,
               "l": LIST_MODE,
               "p": PLOT_MODE,
               "q": QUIT_MODE,
               "r": RUN_MODE,
               "s": STEP_MODE,
               "v": VISL_MODE,
               "w": WRIT_MODE}


    def __init__(self, name, preact = False, postact = False, model_nm=None):
        super().__init__(name)
        self.agents   = []
        self.womb = []
        self.period = 0
        self.preact = preact
        self.postact = postact
        self.model_nm = model_nm
        if model_nm is not None:
            self.props = pa.PropArgs.get_props(model_nm)
        else:
            self.props = None

        user_nm = getpass.getuser()
        self.props.set("user_name", user_nm)
        user_type = self.props.get("user_type", User.IPYTHON)
        self.user = User(user_nm, user_type)


    def add_agent(self, agent):
        self.agents.append(agent)
        agent.add_env(self)
    

    def add_child(self, agent):
        self.womb.append(agent)
        agent.add_env(self)


    def find_agent(self, name):
        for agent in self.agents:
            if agent.name == name:
                return agent
        return None


    def menu(self):
        self.user.tell("Running in " + self.name + ".")
        self.user.tell("Choose one and press Enter:")
        choice = self.user.ask(
            "(c)ode; "\
            "(d)ebug; "\
            "(e)xamine log file; "\
            "(i)nspect agent;\n"\
            "(l)ist agents; "\
            "(p)lot locations; "\
            "(r)un; "\
            "(s)tep (default); "\
            "(v)isualize;\n"\
            "(w)rite properties; "\
            "(q)uit: ")
        return self.keymap.get(choice.strip(), STEP_MODE)


    def list_agents(self):
        for agent in self.agents:
            self.user.tell(agent.name + " with a goal of " + agent.goal)
   

    def run(self, resume=False):
        if resume: self.period = Environment.prev_period
        else:      self.period = 0

        self.user.tell("Welcome, " + self.user.name)
        mode = self.menu()
        while mode != QUIT_MODE:
            if mode == RUN_MODE:
                self.user.tell("Running continously; press Ctrl-c to halt!")
                time.sleep(3)
                try:
                    while self.keep_running():
                        self.period += 1
                        self.step(delay=.3)
                except KeyboardInterrupt:
                    pass
            elif mode == STEP_MODE:
                self.period += 1
                self.step(delay=0)
            elif mode == INSP_MODE:
                name = self.user.ask("Type the name of the agent to inspect: ")
                entity = self.find_agent(name.strip())
                if entity == None: self.user.tell("No such agent")
                else: entity.pprint()
            elif mode == LIST_MODE:
                self.user.tell("Active agents in environment:")
                self.list_agents()
            elif mode == CODE_MODE:
                code = eval(self.user.ask("Type a line of code to run: "))
            elif mode == DBUG_MODE:
                pdb.set_trace()
            elif mode == EXMN_MODE:
                self.disp_log(self.props.get_logfile())
            elif mode == VISL_MODE:
                self.display()
            elif mode == PLOT_MODE:
                self.plot()
            elif mode == WRIT_MODE:
                file_nm = self.user.ask("Choose file name: ")
                self.write_props(file_nm)

            mode = self.menu()

        Environment.prev_period = self.period

        self.user.tell("Returning to run-time environment")


    def write_props(self, file_nm):
        if self.props is not None:
            self.props.write(file_nm)


    def disp_log(self, logfile):

        MAX_LINES = 16

        if logfile is None:
            self.user.tell("No log file to examine!")

        last_n_lines = deque(maxlen=MAX_LINES) # for now hard-coded

        with open(logfile, 'rt') as log:
            for line in log:
                last_n_lines.append(line)

        self.user.tell("Displaying the last " + str(MAX_LINES)
                + " lines of logfile " + logfile)
        for line in last_n_lines:
            self.user.tell(line.strip())


    def step(self, delay=0):
        if delay > 0: time.sleep(delay)

# agents might be waiting to be born       
        if self.womb != None:
            for agent in self.womb:
                self.add_agent(agent)
            del self.womb[:]  

# there might be state-setting to do before acting
        if(self.preact):
            self.preact_loop()

# now have everyone act in random order
        self.act_loop()
        
# there might be cleanup to do after acting
        if(self.postact):
            self.postact_loop()
        
    
    def act_loop(self):
        indices = list(range(len(self.agents)))
        random.shuffle(indices)
        for i in indices:
            self.agents[i].act()


    def preact_loop(self):
        for agent in self.agents:
            agent.preact()


    def postact_loop(self):
        for agent in self.agents:
            agent.postact()


    def keep_running(self):
        return False


    def display(self):
        pass


    def plot(self):
        pass


class Prehension():

    def __init__(self, name, entity):
        self.name   = name
        self.weight = 1.0;
        self.prehended_entity = entity



