"""
Abelian sandpile model
"""
from propargs.propargs import PropArgs
from indra.utils import get_prop_path
from indra.agent import Agent
from indra.composite import Composite
from indra.space import DEF_HEIGHT, DEF_WIDTH
from indra.env import Env
from indra.display_methods import CIRCLE

MODEL_NAME = "sandpile"
DEBUG = False  # Turns debugging code on or off

NUM_GROUPS = 4

sandpile_env = None
groups = None
group_indices = None


def create_agent(x, y):
    """
    Create an agent with the passed x, y value as its name.
    """
    name = "(" + str(x) + "," + str(y) + ")"
    return Agent(name=name, action=place_action)


def add_grain(agent):
    """
    Add a grain to the agent that is passed in
    by changing the group that it is in.
    """
    global sandpile_env

    curr_group_idx = group_indices[agent.primary_group().name]
    next_group_idx = (curr_group_idx + 1) % NUM_GROUPS
    if DEBUG:
        print("Agent at", agent.pos, "is changing from",
              agent.primary_group(), "to", next_group_idx)
    sandpile_env.now_switch(agent, groups[curr_group_idx],
                            groups[next_group_idx])
    if DEBUG:
        print("Agent at", agent.pos, "has changed to", agent.primary_group())
    if next_group_idx == 0:
        topple(agent)


def topple(agent):
    """
    Called when height of an agent is greater than NUM_GROUPS.
    Calls add_grain for its Von Neumann neighbors
    and if those agents need to topple, recursively calls topple.
    """
    global sandpile_env

    if DEBUG:
        print("Sandpile in", agent.pos, "is toppling")
    if agent.neighbors is None:
        sandpile_env.get_vonneumann_hood(agent, save_neighbors=True)
    for neighbor in agent.neighbors:
        add_grain(agent.neighbors[neighbor])


def sandpile_action(sandpile_env):
    """
    The action that will be taken avery period.
    Adds a grain to the center agent.
    """
    if DEBUG:
        print("Adding a grain to sandpile in position",
              sandpile_env.attrs["center_agent"].pos,
              "which is in the group",
              sandpile_env.attrs["center_agent"].primary_group())
    add_grain(sandpile_env.attrs["center_agent"])
    return True


def place_action(agent):
    return True


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    global sandpile_env
    global groups
    global group_indices

    ds_file = get_prop_path(MODEL_NAME)
    if props is None:
        pa = PropArgs.create_props(MODEL_NAME,
                                   ds_file=ds_file)
    else:
        pa = PropArgs.create_props(MODEL_NAME,
                                   prop_dict=props)
    width = pa.get('grid_width', DEF_WIDTH)
    height = pa.get('grid_height', DEF_HEIGHT)
    groups = []
    group_indices = {}
    for i in range(NUM_GROUPS):
        groups.append(Composite(("Group" + str(i)), {"marker": CIRCLE}))
        group_indices[groups[i].name] = i
    for y in range(height):
        for x in range(width):
            groups[0] += create_agent(x, y)
    sandpile_env = Env("Sanpile",
                       action=sandpile_action,
                       members=groups,
                       height=height,
                       width=width,
                       random_placing=False,
                       props=pa)
    sandpile_env.attrs["center_agent"] = sandpile_env.get_agent_at(height // 2,
                                                                   width // 2)
    return (sandpile_env, groups, group_indices)


def main():
    global sandpile_env
    global groups
    global group_indices
    (sandpile_env, groups, group_indices) = set_up()
    sandpile_env()
    return 0


if __name__ == "__main__":
    main()
