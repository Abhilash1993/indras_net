# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 21:40:05 2015

@authors: Brandon Logan
    Gene Callahan
Implements Thomas Schelling's segregation model.
An agent moves when she finds herself to be "too small"
of a minority in a particular neighborhood.
"""


import random
import indra.prehension as pre
import indra.prehension_agent as pa
import indra.grid_env as grid

MOVE = True
STAY = False
RED = pre.X
BLUE = pre.Y
AGENT_TYPES = {RED: "RedAgent", BLUE: "BlueAgent"}
RED_AGENT = "RedAgent"
BLUE_AGENT = "BlueAgent"


class SegregationAgent(pa.PrehensionAgent):
    """
    An agent that moves location based on its neighbors' types
    """
    def __init__(self, name, goal, min_tol, max_tol, max_move=100,
                 max_detect=1):
        super().__init__(name, goal, max_move=max_move, max_detect=max_detect)
        self.tolerance = random.uniform(max_tol, min_tol)
        self.stance = None
        self.orientation = None

    def eval_env(self, other_pre):
        """
        Use the results of surveying the env to decide what to do.
        """
        if other_pre == pre.Prehension.NULL_PRE:  # no neighbors, we stay put
            return STAY

        # otherwise, see how we like the hood
        other_pre = other_pre.normalize()
        other_projection = other_pre.project(self.orientation)
        my_projection = self.stance.project(self.orientation)
        if other_projection < my_projection:
            return MOVE
        else:
            return STAY

    def respond_to_cond(self, env_vars=None):
        self.move_to_empty()


class BlueAgent(SegregationAgent):
    """
    We set our stance.
    """
    def __init__(self, name, goal, min_tol, max_tol, max_move=100,
                 max_detect=1):
        super().__init__(name, goal, min_tol, max_tol,
                         max_move=max_move, max_detect=max_detect)
        self.orientation = BLUE
        self.stance = pre.stance_pct_to_pre(self.tolerance, BLUE)


class RedAgent(SegregationAgent):
    """
    We set our stance.
    """
    def __init__(self, name, goal, min_tol, max_tol, max_move=100,
                 max_detect=1):
        super().__init__(name, goal, min_tol, max_tol,
                         max_move=max_move, max_detect=max_detect)
        self.orientation = RED
        self.stance = pre.stance_pct_to_pre(self.tolerance, RED)


class SegregationEnv(grid.GridEnv):
    """
    The segregation model environment, mostly concerned with bookkeeping.
    """

    def __init__(self, name, width, height, torus=False,
                 model_nm="Segregation"):

        super().__init__(name, width, height, torus=False,
                         model_nm=model_nm)
        self.plot_title = name
        # setting our colors adds varieties as well!
        self.set_var_color(AGENT_TYPES[BLUE], 'b')
        self.set_var_color(AGENT_TYPES[RED], 'r')
        self.num_moves = 0
        self.move_hist = []

    def move_to_empty(self, agent, grid_view=None):
        super().move_to_empty(agent, grid_view)
        self.num_moves += 1

    def census(self, disp=True):
        """
        Take a census recording the number of moves.
        """
        self.move_hist.append(self.num_moves)
        self.user.tell("Moves per turn: " + str(self.move_hist))
        self.num_moves = 0

    def record_results(self, file_nm):
        """
        """
        f = open(file_nm, 'w')
        for num_moves in self.move_hist:
            f.write(str(num_moves) + '\n')
        f.close()
