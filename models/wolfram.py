"""

"""

from propargs.propargs import PropArgs

from indra.agent import Agent, switch
from indra.env import Env
from indra.space import DEF_HEIGHT, DEF_WIDTH
from indra.composite import Composite
from indra.display_methods import BLACK, WHITE, BLUE

X = 0
Y = 1

DEBUG = True  # Turns debugging code on or off
DEBUG2 = False  # Turns deeper debugging code on or off

# States
B = 1
W = 0

STATE_MAP = {B: BLACK, W: WHITE}

# Some dictionaries of rules:
RULE30 = {
    (B, B, B): W,
    (B, B, W): W,
    (B, W, B): W,
    (B, W, W): B,
    (W, B, B): B,
    (W, B, W): B,
    (W, W, B): B,
    (W, W, W): W
}

GRID_WIDTH = 31
GRID_HEIGHT = 31

groups = []


def create_agent(name):
    """
    Create an agent with the passed in name
    """
    return Agent(str(name), action=agent_action)


def change_color(wolfram_env, agent):
    """
    Automatically change color from one group to the other
    """
    curr_group = agent.primary_group()
    next_group = groups[0]
    if curr_group == next_group:
        next_group = groups[1]
    switch(agent, curr_group, next_group)


def get_current_row(wolfram_env):
    """
    Returns an int of the current row, which is the bottom most row with
    an alive agent
    """


def wolfram_action(wolfram_env):
    #  y = get_current_row(wolfram_env)
    #  row = get_row_hood(y)
    if DEBUG:
        print("In wolfram_action")


def agent_action(agent):
    print("I'm " + agent.name + " and I'm acting.")
    # Returning false means to move
    return False


def set_up():
    """
    A func to set up run that can also be used by test code.
    """
    pa = PropArgs.create_props('basic_props',
                               ds_file='props/basic.props.json')
    width = pa.get('grid_width', DEF_WIDTH)
    height = pa.get('grid_height', DEF_HEIGHT)
    black = Composite("black", {"color": BLACK})
    white = Composite("blue", {"color": BLUE})
    groups.append(white)
    groups.append(black)
    print("Height and width: ", height, width)
    for i in range(height * width):
        groups[0] += create_agent(i)
    wolfram_env = Env("wolfram env",
                      action=wolfram_action,
                      height=height,
                      width=width,
                      members=groups,
                      random_placing=False)
    first_agent = wolfram_env.get_agent_at(height // 2, width - 1)
    change_color(wolfram_env, first_agent)
    return (groups, wolfram_env)


def main():
    global groups
    global wolfram_env
    (groups, wolfram_env) = set_up()
    wolfram_env()
    return 0


if __name__ == "__main__":
    main()
