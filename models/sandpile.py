"""
This is an abelian sandpile model.
Starting life of sandpile as segregation clone.
"""

from propargs.propargs import PropArgs

from indra.agent import Agent, switch
from indra.composite import Composite
from indra.env import Env


DEBUG = False  # turns debugging code on or off

DEF_HEIGHT = 10
DEF_WIDTH = 10

SAND_PREFIX = "sand_location "

NEARBY = 1

NUM_GROUPS = 4

sandpile = None

groups = None
group_indices = {}


def create_agent(x, y):
    """
    Create an agent with the passed x, y value as its name.
    """
    name = "(" + str(x) + "," + str(y) + ")"
    return Agent(name=name, action=place_action)


def get_curr_group_idx(agent):
    """
    Returns the int index of the current group
    Ex) returns 0 if group is Group 0
    """
    return group_indices[agent.primary_group().name]


def get_next_group_idx(curr_group_idx):
    """
    Returns the int index of the next group
    Ex) returns 1 if curr_group_idx group is Group 0
    """
    return (curr_group_idx + 1) % NUM_GROUPS


def change_group(agent, sandpile, curr_group_idx, next_group_idx):  # noqa F811
    """
    Change group from current group index passed in
    to the next group index passed in
    """
    switch(agent, groups[curr_group_idx], groups[next_group_idx])


def add_grain(sandpile, agent):
    """
    Addd a grain to whichever agent is passed in
    """
    curr_group_idx = get_curr_group_idx(agent)
    next_group_idx = get_next_group_idx(curr_group_idx)
    if DEBUG:
        print("Agent at", agent.pos, "is changing group from",
              agent.primary_group(), "to", next_group_idx)
    change_group(agent, sandpile, curr_group_idx, next_group_idx)
    if DEBUG:
        print("Agent at", agent.pos, "has changed to", agent.primary_group())
    if next_group_idx == 0:
        topple(sandpile, agent)


def topple(sandpile, agent):
    if DEBUG:
        print("Sandpile in", agent.pos, "is toppling")
    for neighbor in agent.neighbors:
        add_grain(sandpile, neighbor)


def sandpile_action(sandpile):
    """
    Drop a grain on the center agent.
    """
    if DEBUG:
        print("Adding a grain to sandpile in position",
              sandpile.attrs["center_agent"].pos,
              "which is in the group",
              sandpile.attrs["center_agent"].primary_group())
    add_grain(sandpile, sandpile.attrs["center_agent"])


def place_action(agent):
    if agent.neighbors is None:
        neighbors = sandpile.get_vonneumann_hood(agent)
        agent.neighbors = neighbors


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    global groups

    if props is None:
        pa = PropArgs.create_props('sandpile_props',
                                   ds_file='props/sandpile.props.json')
    else:
        pa = PropArgs.create_props('sandpile_props',
                                   prop_dict=props)

    width = pa.get('grid_width', DEF_WIDTH)
    height = pa.get('grid_height', DEF_HEIGHT)
    groups = []
    for i in range(NUM_GROUPS):
        groups.append(Composite("Group" + str(i)))
        group_indices[groups[i].name] = i
    for y in range(height):
        for x in range(width):
            groups[0] += create_agent(x, y)
    sandpile = Env("A sandpile",
                   action=sandpile_action,
                   members=groups,
                   height=height,
                   width=width,
                   random_placing=False)
    sandpile.attrs["center_agent"] = sandpile.get_agent_at(height // 2,
                                                           width // 2)

    return (groups, group_indices, sandpile)


def main():
    global sandpile
    global groups
    (groups, group_indices, sandpile) = set_up()
    sandpile()
    return 0


if __name__ == "__main__":
    main()
