"""
Filename: predator_prey.py
Author: Gene Callahan
"""

import math
import cmath
import time
import random
import logging
import pprint
import numpy as np
import matplotlib.pyplot as plt
import node
import entity as ent
import spatial_agent as sa
import display_methods as disp
from collections import deque


EAT          = "eat"
AVOID        = "avoid"
REPRODUCE    = "reproduce"
MAX_EXCLUDE  = 10

pp = pprint.PrettyPrinter(indent=4)


def print_creature(creature):
    print(creature.__str__())


class Creature(sa.SpatialAgent):

    """ This class is the parent of all things that:
        1) eat; 2) age; and 3) reproduce """

    def __init__(self, name, life_force, repro_age,
            decay_rate, max_move=0.0, max_detect=10.0,
            goal=EAT, rand_age=False):

        super().__init__(name, goal, max_move, max_detect)

        self.life_force = random.uniform(life_force * .8,
                    life_force * 1.2)
        self.orig_force = self.life_force
        self.decay_rate = decay_rate
        self.repro_age  = repro_age
        self.env        = None

        if not rand_age: self.age = 0
        else           : self.age = random.uniform(0, self.repro_age)


    def __str__(self):
        return(self.name + " with " + str(self.life_force)
                    + " life force")

    def get_life_force(self):
        return self.life_force

    def is_alive(self):
        return self.life_force > 0

    def act(self):
        self.age += 1.0
        if (int(math.floor(self.age)) % self.repro_age) < 1:
            offspring = self.reproduce()
            assert self.env  != None
            if offspring != None:
                d, i = math.modf(self.age)
                offspring.age += d
                self.env.add_agent(offspring)
        self.life_force -= self.decay_rate


    def reproduce(self):
        return None


    def eat(self, prey):
        self.life_force += prey.get_life_force()
        prey.be_eaten()
        logging.info(self.name + " has eaten " + prey.name)


    def be_eaten(self):
        self.life_force = 0


class Grass(Creature):

    """ This class defines grass, a type of herb 
        and a likely prey creature """

    MAX_GRASS = 200


    def __init__(self, name, life_force, repro_age, decay_rate,
            max_move=0.0, max_detect=0.0, goal=REPRODUCE,
            rand_age=False):

        super().__init__(name, life_force, repro_age, decay_rate,
                max_move=max_move, max_detect=max_detect,
                goal=goal, rand_age=rand_age)


    def reproduce(self):
        my_pop = self.env.get_my_pop(self)
        if my_pop < self.MAX_GRASS:
            return Grass("herb" + str(my_pop), self.orig_force, 
                    self.repro_age, self.decay_rate)
        else: return None


class MobileCreature(Creature, sa.MobileAgent):

    """ This class is the parent of all creatures
        that can move around.
    """

    def __init__(self, name, life_force, repro_age, 
            decay_rate, max_move=0.0, max_detect=10.0,
            max_eat=2.0, goal=EAT, rand_age=False):

        super().__init__(name, life_force, repro_age, 
                decay_rate, max_move, max_detect,
                goal=goal, rand_age=rand_age)

        self.max_eat    = max_eat
        self.wandering  = True
        self.focus      = None
        self.exclude    = deque(maxlen=MAX_EXCLUDE)


    def survey_env(self, universal):
        logging.debug("scanning env for " + universal)
        prehends = node.get_prehensions(
                prehender=type(self), universal=universal)
        if not prehends == None:
            for pre_type in prehends:
                if self.env.contains(pre_type):
                    prehended = self.env.closest_x(self,
                                    self.pos, pre_type,
                            self.exclude)
                    if self.in_detect_range(prehended):
                        self.wandering = False
                        self.focus = prehended
                        logging.debug(self.name
                                + " has spotted prehension: "
                                + prehended.name)
                        return prehended
        return None


    def in_gobble_range(self):
        return self.in_range(self.focus, self.max_eat)


class Predator(MobileCreature):

    def detect_behavior(self):
        self.pursue_prey()


    def pursue_prey(self):
        prey = self.focus
        logging.info(self.name + " is pursuing " + prey.name)
        if prey.is_alive():
            new_pos = self.pos
            vector = prey.pos - self.pos
            dist   = abs(vector)
            if dist < self.max_move:
                new_pos = prey.pos
            else:
                new_pos += (vector / dist) * self.max_move

            self.pos = new_pos
            if self.in_gobble_range():
                self.eat(prey)
                self.wandering = True
                self.focus = None


class MobilePrey(MobileCreature):

    def __init__(self, name, life_force, repro_age, 
            decay_rate, max_move=0.0, max_detect=10.0,
            max_eat=2.0, goal=AVOID, rand_age=False):

        super().__init__(name, life_force, repro_age, 
                decay_rate, max_move, max_detect,
                goal=goal, rand_age=rand_age)


    def detect_behavior(self):
        self.avoid_predator()


    def avoid_predator(self):
        pass



class Fox(Predator):

    """
    This class defines foxes, a type of predator.
    """

    def __init__(self, name, life_force, repro_age, decay_rate,
            max_move=10.0, max_detect=10.0, goal=EAT, rand_age=False):

        super().__init__(name, life_force, repro_age, decay_rate,
                max_move, max_detect, goal=goal, rand_age=rand_age)


    def reproduce(self):
        return Fox("brer" + str(self.env.get_my_pop(self)),
                self.orig_force, self.repro_age,
                self.decay_rate, self.max_move,
                self.max_detect)


class Mouse(MobilePrey):

    """ This class defines mice, a type of herbivore
        and a likely prey creature """

    AVG_MOUSE_FORCE = 10.0


    def __init__(self, name, life_force, repro_age, decay_rate,
            max_move, max_detect=10.0, goal=EAT, rand_age=False):

        super().__init__(name, life_force, repro_age, decay_rate,
                max_move, max_detect, goal=goal, rand_age=rand_age)


    def reproduce(self):
# revert to mean:
        force = (self.orig_force + self.AVG_MOUSE_FORCE) / 2.0
        return Mouse("mickey" + str(self.env.get_my_pop(self)),
                    force, self.repro_age, self.decay_rate,
                    self.max_move)


class Rabbit(MobilePrey):

    """ This class defines rabbits, a type of herbivore
    and a likely prey creature
    """

    AVG_RABBIT_FORCE = 20.0


    def __init__(self, name, life_force, repro_age, decay_rate,
            max_move, max_detect=10.0, goal=AVOID, rand_age=False):

        super().__init__(name, life_force, repro_age, decay_rate,
                max_move, max_detect, goal=goal, rand_age=rand_age)


    def reproduce(self):
# revert to mean:
        force = (self.orig_force + self.AVG_RABBIT_FORCE) / 2.0
        return Rabbit("bunny" + str(self.env.get_my_pop(self)),
                force, self.repro_age,
                self.decay_rate, self.max_move)


class PredPreyEnv(sa.SpatialEnvironment):

    """ This class creates an environment for predators
        to chase and eat prey """

    repop = True

    def __init__(self, name, length, height, preact=True,
            postact=True, model_nm="predprey_model"):
        super().__init__(name, length, height, preact,
                        postact, model_nm=model_nm)
        self.num_zombies = 10


    def keep_running(self):
        return len(self.agents) > 0


    def display(self):
        if self.period < 4:
            print("Too little data to display")
            return

        pop_hist = {}
        for s in self.varieties:
            pop_hist[s] = self.varieties[s]["pop_hist"]

        disp.display_line_graph('Populations in '
                                + self.name,
                                pop_hist,
                                self.period)


    def postact_loop(self):
# since we will be culling let's walk list in reverse
        for creature in reversed(self.agents):
            if not creature.is_alive():
                self.cull(creature)


    def cull(self, creature):
        s = node.get_node_type(creature)
        assert self.varieties[s]["pop"] > 0
        self.varieties[s]["pop"] -= 1
        self.agents.remove(creature)


