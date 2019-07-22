"""
This file defines an Agent.
"""
import sys
import numpy as np
from math import pi, sin
import json
from random import random
from collections import OrderedDict


DEBUG = False  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

# x and y indices
X = 0
Y = 1
NEUTRAL = .7071068

# Set up constants for some common vectors: this will save time and memory.
X_VEC = np.array([1, 0])
Y_VEC = np.array([0, 1])
NULL_VEC = np.array([0, 0])
NEUT_VEC = np.array([NEUTRAL, NEUTRAL])

INF = sys.maxsize  # really any very big number would do here!

DEF_MAX_MOVE = None


def prob_state_trans(curr_state, states):
    """
    Do a probabilistic state transition.
    """
    new_state = curr_state
    r = random()
    cum_prob = 0.0
    for trans_state in range(len(states[curr_state])):
        cum_prob += states[curr_state][trans_state]
        if cum_prob >= r:
            new_state = trans_state
            break
    return new_state


def possible_trans(states, start_state, end_state):
    return states[start_state][end_state]


def ratio_to_sin(ratio):
    """
    Take a ratio of y to x and turn it into a sine.
    """
    return sin(ratio * pi / 2)


def type_hash(agent):
    """
    type_hash() will return an ID that identifies
    the ABM type of an entity.
    """
    return len(agent)  # temp solution!


def is_composite(thing):
    """
    Is this thing a composite?
    """
    return hasattr(thing, 'members')


def is_space(thing):
    """
    How do we determine if a group we are a member of is a space?
    """
    return hasattr(thing, "height")


def join(agent1, agent2):
    """
        Create connection between agent1 and agent2.
    """
    if not is_composite(agent1):
        print("Attempt to place " + str(agent2)
              + " in non-group " + str(agent1))
    else:
        agent1.add_member(agent2)
        agent2.add_group(agent1)


def split(agent1, agent2):
    """
        Break connection between agent1 and agent2.
    """
    if not is_composite(agent1):
        print("Attempt to remove " + str(agent2)
              + " from non-group " + str(agent1))
    else:
        agent1.del_member(agent2)
        agent2.del_group(agent1)


def switch(agent, grp1, grp2):
    """
        Move agent from grp1 to grp2.
    """
    split(grp1, agent)
    join(grp2, agent)


class AgentEncoder(json.JSONEncoder):
    """
    The JSON encoder base class for all descendants
    of Agent.
    """
    def default(self, o):
        if hasattr(o, 'to_json'):
            return o.to_json()
        elif isinstance(o, np.int64):
            return int(o)
        else:
            return json.JSONEncoder.default(self, o)


class Agent(object):
    """
    This is the base class of all agents, environments,
    and objects contained in an environment.
    Its basic character is that it is a vector, and basic
    vector and matrix operations will be implemented
    here.
    """
    def __init__(self, name, attrs=None, action=None, duration=INF,
                 prim_group=None):
        self.name = name
        self.action_key = None
        self.action = action
        if action is not None:
            self.action_key = action.__name__

        self.duration = duration
        self.attrs = OrderedDict()
        self.neighbors = None
        if attrs is not None:
            self.attrs = attrs
        self.type_sig = type_hash(self)
        self.active = True
        self.groups = {}
        self.pos = None
        self.locator = None
        self.prim_group = prim_group
        self.has_acted = False
        if self.prim_group is not None:
            self.groups[str(self.prim_group)] = self.prim_group
            if is_space(self.prim_group):
                self.locator = self.prim_group

    def to_json(self):
        # self.groups = {"name": Agent}
        # self.prim_group = Agent
        grp_nms = ""
        for grp in self.groups:
            grp_nms += grp + " "
        return {"name": self.name,
                "is_composite": 0,
                "duration": self.duration,
                "pos": self.pos,
                "attrs": self.attrs_to_dict(),
                "groups": grp_nms,
                "active": self.active,
                "type_sig": self.type_sig,
                "prim_group": str(self.prim_group),
                "locator": str(self.locator),
                "neighbors": self.neighbors,
                "has_acted": self.has_acted,
                "action_key": self.action_key
                }

    def from_json(self, serial_agent):
        from models.run_dict import action_dict
        self.action = action_dict[serial_agent["action_key"]]
        self.action_key = serial_agent["action_key"]
        self.has_acted = serial_agent["has_acted"]
        self.neighbors = serial_agent["neighbors"]
        self.type_sig = serial_agent["type_sig"]
        self.active = serial_agent["active"]
        # ret_group = serial_agent["groups"]
        # grp_nm = ret_group.split(" ")
        # for elem in grp_nm:
        #     self.groups[elem] = # Agent!!
        # self.prim_group = serial_agent["prim_group"] Agent
        # prob we want to create a dict with
        # "Agent Name" as key and the Agent as val
        # self.locator = self.prim_group
        self.attrs = serial_agent["attrs"]
        self.pos = serial_agent["pos"]
        self.duration = serial_agent["duration"]
        self.name = serial_agent["name"]

    def __repr__(self):
        return json.dumps(self.to_json(), cls=AgentEncoder, indent=4)

    def primary_group(self):
        # print("We are at primary_group FUNCTION: ", self.prim_group)
        return self.prim_group

    def islocated(self):
        return self.pos is not None

    def set_pos(self, locator, x, y):
        self.locator = locator  # whoever sets my pos is my locator!
        self.pos = (x, y)

    def get_pos(self):
        return self.pos

    def get_x(self):
        return self.pos[X]

    def get_y(self):
        return self.pos[Y]

    def __eq__(self, other):
        if (type(self) != type(other) or len(self) != len(other)):
            return False
        else:
            for key in self:
                if key not in other:
                    return False
                elif other[key] != self[key]:
                    return False
            return True

    def __str__(self):
        return self.name

    def __len__(self):
        return len(self.attrs)

    def __getitem__(self, key):
        return self.attrs[key]

    def __setitem__(self, key, value):
        self.attrs[key] = value

    def __contains__(self, item):
        return item in self.attrs

    def __iter__(self):
        return iter(self.attrs)

    def __call__(self, **kwargs):
        """
        Agents will 'act' by being called as a function.
        If the agent has no `action()` function, do nothing.
        If returns False, by default agent will move.
        """
        self.duration -= 1
        if self.duration > 0:
            if self.action is not None:
                # the action was defined outside this class, so pass self:
                if not self.action(self, **kwargs):
                    # False return means agent is "unhappy" and
                    # so agent will move (if located).
                    max_move = DEF_MAX_MOVE
                    if "max_move" in self:
                        max_move = self["max_move"]
                    angle = None
                    if "angle" in self:
                        angle = self["angle"]
                    self.move(max_move=max_move, angle=angle)
                return True
            elif DEBUG:
                print("I'm " + self.name
                      + " and I ain't got no action to do!")
        else:
            self.active = False
        return False

    def __iadd__(self, scalar):
        """
        Empty implementation for now.
        """
        return self

    def __isub__(self, scalar):
        """
        Empty implementation for now.
        """
        return self

    def __imul__(self, scalar):
        """
        Empty implementation for now.
        """
        return self

    def __add__(self, other):
        """
        Adds agent and group to make new group.
        """
        import composite
        if isinstance(other, Agent):
            return composite.Composite(
                self.name + other.name,
                members=[self, other])
        else:
            return None

    def move(self, max_move=DEF_MAX_MOVE, angle=None):
        """
        Move this agent to a random pos within max_move
        of its current pos.
        """
        if (self.islocated() and self.locator is not None
                and not self.locator.is_full()):
            if angle is not None:
                print("This is the pos:", self.pos)
                new_xy = self.locator.point_from_vector(angle,
                                                        max_move, self.pos)
                print("This is the max_move:", max_move)
                print("This is the new_xy:", new_xy)
                self.locator.place_member(self, max_move, new_xy)
            else:
                self.locator.place_member(self, max_move)

    def isactive(self):
        return self.active

    def die(self):
        self.duration = 0
        self.active = False

    def attrs_to_dict(self):
        """
        Now attrs ARE a dict, so just return 'em.
        """
        return self.attrs

    def same_type(self, other):
        return self.type_sig == other.type_sig

    def del_group(self, group):
        if str(group) in self.groups:
            del self.groups[str(group)]

        if group == self.prim_group:
            self.prim_group = None

    def add_group(self, group):
        if str(group) not in self.groups:
            if DEBUG2:
                print("Join group being called on " + str(self.pos)
                      + " to join group: " + group.name)
            self.groups[group.name] = group
            if is_space(group):
                self.locator = group

            if self.prim_group is None:
                self.prim_group = group

    def switch_groups(self, g1, g2):
        self.del_group(g1)
        self.add_group(g2)
