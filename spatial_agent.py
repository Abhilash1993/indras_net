"""
Filename: spatial_agent.py
Author: Gene Callahan
"""

import copy
import math
import cmath
import time
import random
import logging
import numpy as np
import matplotlib.pyplot as plt
import entity as ent
import display_methods as disp

MAX_ZERO_PER = 8


def rand_complex(initPos, radius):
    """Generates a random complex number 
        uniformly picked from a disk of radius.
    """
    radius = math.sqrt(radius * random.uniform(0.0, radius))
    theta  = random.random() * 2 * math.pi
    return initPos + cmath.rect(radius, theta)


def pos_to_str(pos):
    return str(int(pos.real)) + " , " + str(int(pos.imag))


class SpatialAgent(ent.Agent):

    """ This class is the parent of all entities that are
        located in space (and might or might not move in it)
    """


    def __init__(self, name, goal, max_move=0.0, max_detect=0.0):
        super().__init__(name, goal)
        self.max_move   = max_move
        self.max_detect = max_detect
        self.pos = None
        self.wandering = False


    def add_env(self, env):
        self.env = env


    def in_detect_range(self, prehended):
        return self.in_range(prehended, self.max_detect)


    def in_range(self, prey, dist):
        if prey == None:
            return False

        if SpatialEnvironment.get_distance(self.pos, prey.pos) < dist:
            return True
        else:
            return False


    def survey_env(self, universal):
        logging.debug("surveying env for " + universal)
        prehended_list = []
        prehends = ent.get_prehensions(
                prehender=type(self), universal=universal)
        if not prehends == None:
            for pre_type in prehends:
# this loop over all agents must be eliminated
#  before we do huge simulations!
                for agent in self.env.agents:
                    agent_type = ent.get_agent_type(agent)
                    if agent is not self:
                        if(self.in_detect_range(agent)
                                and agent_type == pre_type):
                            prehended_list.append(agent)
        return prehended_list


    def detect_behavior(self):
        pass


class MobileAgent(SpatialAgent):
    """
    Agents that can move in the env
    """


    def __init__(self, name, goal, max_move=20.0, max_detect=20.0):
        super().__init__(name, goal, 
                    max_move=max_move, max_detect=max_detect)
        self.wandering = True


    def get_max_move(self):
        return self.max_move


class SpatialEnvironment(ent.Environment):

    """ Extends the base Environment with entities located in the 
        complex plane """

    @staticmethod
    def get_distance(p1, p2):
        return abs(p1 - p2)


    def __init__(self, name, length, height, preact=True,
                    postact=False, model_nm=None):

        super().__init__(name, preact=preact,
                        postact=postact, model_nm=model_nm)

        self.length   = length
        self.height   = height
        self.max_dist = self.length * self.height
        self.num_zombies = 0
        self.varieties = {}
        self.do_census = True
# it only makes sense to plot agents in a spatial env, so add this here:
        self.add_menu_item("View", "p", "(p)lot agents", self.plot)


    def add_agent(self, agent):
        super().add_agent(agent)
        x = random.uniform(0, self.length - 1)
        y = random.uniform(0, self.height - 1)
        agent.pos = complex(x, y)

        v = ent.get_agent_type(agent)
        logging.debug("Adding " + agent.__str__()
                + " of variety " + v)

        if v in self.varieties:
            self.varieties[v]["pop"] += 1
        else:
            self.varieties[v] = {"pop": 1,
                           "pop_of_note": 0,
                           "pop_hist": [],
                           "zombies": [],
                           "zero_per": 0}
        if len(self.varieties[v]["zombies"]) < self.num_zombies:
            self.varieties[v]["zombies"].append(copy.copy(agent))


    def step(self, delay=0):
        if self.do_census: 
            self.census()
        super().step()


    def contains(self, agent_type):
        return agent_type in self.varieties


    def census(self):
        self.user.tell("Populations in period "
                        + str(self.period) + ":")
        for v in self.varieties:
            pop = self.get_pop(v)
            self.user.tell(v + ": " + str(pop))
            var = self.varieties[v]
            var["pop_hist"].append(pop)
            if pop == 0:
                var["zero_per"] += 1
                if var["zero_per"] >= MAX_ZERO_PER:
                    for agent in var["zombies"]:
                        self.add_agent(copy.copy(agent))
                    var["zero_per"] = 0


    def get_pop(self, s):
        return self.varieties[s]["pop"]


    def preact_loop(self):
        logging.debug("Calling preact_loop()")
        for agent in self.agents:
            if agent.wandering:
                agent.pos = self.get_new_wander_pos(agent)
                logging.debug(
                    "In preact_loop, getting new agent pos")
                logging.debug("We are about to survey the "
                    "env for "
                    + agent.name + " which has a goal of "
                    + agent.goal)
                agent.survey_env(agent.goal)
            else:
                agent.detect_behavior()


    def closest_x(self, seeker, pos, target_type, exclude):
        x = self.max_dist
        close_target = None
        for agent in self.agents:
            if seeker is not agent: # don't locate me!
                if ent.get_agent_type(agent) == target_type:
                    if (not exclude == None) and (not agent in exclude):
                        p_pos = agent.pos
                        d     = self.get_distance(pos, p_pos)
                        if d < x:
                            x = d
                            close_target = agent
        return close_target


    def pos_msg(self, agent, pos):
        x = pos.real
        y = pos.imag
        return("New position for " + 
                    agent.name + " is "
                    + str(int(x)) + ", "
                    + str(int(y)))

    def get_new_wander_pos(self, agent):
        new_pos = rand_complex(agent.pos, agent.get_max_move())
        x = new_pos.real
        y  = new_pos.imag
        if x < 0.0:
            x = 0.0
        if y  < 0.0:
            y  = 0.0
        if x > self.length:
            x = self.length
        if y  > self.height:
            y  = self.height
        pos = complex(x, y)
        logging.debug(self.pos_msg(agent, pos))
        return pos


    def plot(self):
        data = {}
        for v in self.varieties:
            data[v] = {"x": [], "y": []}
            for a in self.agents:
                if type(a).__name__ == v:
                    pos = a.pos
                    x = pos.real
                    y = pos.imag
                    data[v]["x"].append(x)
                    data[v]["y"].append(y)
                
        disp.display_scatter_plot("Agent Positions", data)


