"space_mdl_helper.py""""
    This is the fashion model re-written in indra.
"""

import math
from operator import gt, lt

import numpy as np

from indra.agent import Agent, X_VEC, Y_VEC, NEUTRAL
from indra.agent import ratio_to_sin
from indra.composite import Composite
from indra.display_methods import NAVY, DARKRED, RED, BLUE
from indra.env import Env
from indra.registry import get_env, get_group, get_prop
from indra.space import in_hood
from indra.utils import init_props

MODEL_NAME = "fashion"
DEBUG = True  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

NUM_TSETTERS = 5
NUM_FOLLOWERS = 55

ENV_WEIGHT = 0.6
weightings = [1.0, ENV_WEIGHT]

COLOR_PREF = "color_pref"
DISPLAY_COLOR = "display_color"

BLUE_SIN = 0.0
RED_SIN = 1.0

# for future use as we move to vector representation:
BLUE_VEC = X_VEC
RED_VEC = Y_VEC

NOT_ZERO = .001

TOO_SMALL = .01
BIG_ENOUGH = .03

HOOD_SIZE = 4

FOLLOWER_PRENM = "follower"
TSETTER_PRENM = "tsetter"

RED_FOLLOWERS = "Red Followers"
BLUE_FOLLOWERS = "Blue Followers"
RED_TSETTERS = "Red Trendsetters"
BLUE_TSETTERS = "Blue Trendsetters"

opp_group = None


def change_color(agent, society, opp_group):
    """
    change agent's DISPLAY_COLOR to its opposite color
    """
    agent[DISPLAY_COLOR] = not agent[DISPLAY_COLOR]
    society.add_switch(agent, agent.prim_group,
                       opp_group[str(agent.prim_group)])


def new_color_pref(old_pref, env_color):
    """
    Calculate new color pref with the formula below:
    new_color = sin(avg(asin(old_pref) + asin(env_color)))
    """
    me = math.asin(old_pref)
    env = math.asin(env_color)
    avg = np.average([me, env], weights=weightings)
    new_color = math.sin(avg)
    return new_color


def env_unfavorable(my_color, my_pref, op1, op2):
    # we're going to add a small value to NEUTRAL so we sit on fence
    # op1 and op2 should be greater than or less than comparisons
    if my_color == RED_SIN:
        return op1(my_pref, (NEUTRAL - TOO_SMALL))
    else:
        return op2(my_pref, (NEUTRAL + TOO_SMALL))


def follower_action(agent):
    return common_action(agent,
                         get_group(RED_TSETTERS),
                         get_group(BLUE_TSETTERS),
                         lt, gt)


def tsetter_action(agent):
    return common_action(agent,
                         get_group(RED_FOLLOWERS),
                         get_group(BLUE_FOLLOWERS),
                         gt,
                         lt)


def common_action(agent, others_red, others_blue, op1, op2):
    """
    The actions for both followers and trendsetters
    """

    num_others_red = len(others_red.subset(in_hood, agent, HOOD_SIZE))
    num_others_blue = len(others_blue.subset(in_hood, agent, HOOD_SIZE))
    total_others = num_others_red + num_others_blue
    if total_others <= 0:
        return False

    env_color = ratio_to_sin(num_others_red / total_others)

    agent[COLOR_PREF] = new_color_pref(agent[COLOR_PREF], env_color)
    if env_unfavorable(agent[DISPLAY_COLOR], agent[COLOR_PREF], op1, op2):
        change_color(agent, get_env(), opp_group)
        return True
    else:
        return False


def create_tsetter(name, i, props=None, color=RED_SIN):
    """
    Create a trendsetter: all RED to start.
    """
    return Agent(TSETTER_PRENM + str(i),
                 action=tsetter_action,
                 attrs={COLOR_PREF: color,
                        DISPLAY_COLOR: color})


def create_follower(name, i, props=None, color=BLUE_SIN):
    """
    Create a follower: all BLUE to start.
    """
    return Agent(FOLLOWER_PRENM + str(i),
                 action=follower_action,
                 attrs={COLOR_PREF: color,
                        DISPLAY_COLOR: color})


def create_opp_group():
    return {RED_TSETTERS: get_group(BLUE_TSETTERS),
            BLUE_TSETTERS: get_group(RED_TSETTERS),
            RED_FOLLOWERS: get_group(BLUE_FOLLOWERS),
            BLUE_FOLLOWERS: get_group(RED_FOLLOWERS)}


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    init_props(MODEL_NAME, props)
    groups = []

    groups.append(Composite(BLUE_TSETTERS, {"color": NAVY}))
    groups.append(Composite(RED_TSETTERS, {"color": DARKRED},
                            member_creator=create_tsetter,
                            num_members=get_prop('num_tsetters',
                                                 NUM_TSETTERS)))

    groups.append(Composite(RED_FOLLOWERS, {"color": RED}))
    groups.append(Composite(BLUE_FOLLOWERS, {"color": BLUE},
                            member_creator=create_follower,
                            num_members=get_prop('num_followers',
                                                 NUM_FOLLOWERS)))

    global opp_group
    opp_group = create_opp_group()

    Env("Society", members=groups)


def main():
    set_up()

    # get_env() returns a callable object:
    get_env()()
    return 0


if __name__ == "__main__":
    main()
