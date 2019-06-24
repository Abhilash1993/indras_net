"""
    This is the fashion model re-written in indra.
"""

from propargs.propargs import PropArgs

from indra.agent import Agent
from indra.composite import Composite
from indra.space import DEF_HEIGHT, DEF_WIDTH
from indra.env import Env
from indra.display_methods import BLUE

DEBUG = True  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

DEF_NUM_BIRDS = 10

bird_group = None
env = None


def agent_action(agent):
    print("I'm " + agent.name + " and I'm acting.")
    # return False means to move
    return False


def create_agent(color, i):
    """
    Create an agent.
    """
    return Agent(color + str(i), action=agent_action)


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    pa = props
    if pa is None:
        pa = PropArgs.create_props('flocking_props',
                                   ds_file='props/flocking.props.json')
    bird_group = Composite("Birds", {"color": BLUE},
                           member_creator=create_agent,
                           num_members=pa.get('num_birds', DEF_NUM_BIRDS))

    env = Env("env",
              height=pa.get('grid_height', DEF_HEIGHT),
              width=pa.get('grid_width', DEF_WIDTH),
              members=[bird_group])
    return (bird_group, env)


def main():
    global bird_group
    global env

    (bird_group, env) = set_up()

    if DEBUG2:
        print(env.__repr__())

    env()
    return 0


if __name__ == "__main__":
    main()
