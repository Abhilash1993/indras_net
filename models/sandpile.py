"""
    This is an abelican sandpile model.
    Starting life of sandpile as segregation clone.
"""

from indra.agent import Agent
from indra.composite import Composite
# from indra.space import in_hood
from indra.env import Env
import indra.display_methods as disp


DEBUG = True  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

HEIGHT = 2
WIDTH = 2

MAX_SAND = 5

SAND_PREFIX = "sand location"

NEARBY = 1

sandpile = None

group0 = None
group1 = None
group2 = None
group3 = None
group4 = None
group5 = None


def env_unfavorable(sand_height):
    """
    Is the environment to our agent's liking or not??
    Here, the question is, "Is there too much sand?"
    """
    return sand_height > MAX_SAND


def change_color(agent, sandpile, opp_group):
    if DEBUG2:
        print("Agent " + str(agent) + " is changing colors from "
              + str(agent.primary_group()) + " to "
              + str(opp_group[str(agent.primary_group())]))
    sandpile.add_switch(agent, agent.primary_group(),
                        opp_group[str(agent.primary_group())])


def grain_action(agent):
    """
    If the agent is surrounded by more "others" than it is comfortable
    with, the agent will move.
    """
    print("from grain_action")
    neighbors = sandpile.get_vonneumann_hood(agent)
    for neighbor in neighbors:
        print(neighbor)


def sandpile_action(sanpile):
    sandpile.attrs["center agent"]["grains"] += 1
    print("test_env_action")


def create_agent(i):
    """
    Creates agent for holding sand.
    """
    return Agent(SAND_PREFIX + str(i),
                 action=grain_action,
                 attrs={"grains": 0})


def set_up():
    """
    A func to set up run that can also be used by test code.
    """
    group0 = Composite("Group0", {"color": disp.BLACK})
    group1 = Composite("Group1", {"color": disp.MAGENTA})
    group2 = Composite("Group2", {"color": disp.BLUE})
    group3 = Composite("Group3", {"color": disp.CYAN})
    group4 = Composite("Group4", {"color": disp.RED})
    group5 = Composite("Group5", {"color": disp.YELLOW})
    for i in range(HEIGHT * WIDTH):
        group0 += create_agent(i)

    sandpile = Env("A sandpile", action=sandpile_action, members=[
                   group0,
                   group1,
                   group2,
                   group3,
                   group4,
                   group5
                   ],
                   height=HEIGHT, width=WIDTH)
    sandpile.attrs["center agent"] = sandpile.get_agent_at(HEIGHT / 2,
                                                           WIDTH / 2)

    return (group0,
            group1,
            group2,
            group3,
            group4,
            group5,
            sandpile)


def main():
    global sandpile
    global group0
    global group1
    global group2
    global group3
    global group4
    global group5
    (group0, group1, group2, group3, group4, group5,
     sandpile) = set_up()

    if DEBUG2:
        print(sandpile.__repr__())

    sandpile()
    return 0


if __name__ == "__main__":
    main()
