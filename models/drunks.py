"""
El Farol Bar Problem
A problem to check if it's possible for the bar to be
occupied by 60% of the population every time
"""

import random


from indra.utils import get_props
from indra.agent import Agent
from indra.composite import Composite
from indra.space import DEF_HEIGHT, DEF_WIDTH
from indra.env import Env
from indra.display_methods import BLUE, RED

DEBUG = False

MODEL_NAME = "drunks"

DEF_POPULATION = 10
DEF_OPTIMAL_OCCUPANCY = int(0.6 * DEF_POPULATION)
MOTIVATION = [0.6] * DEF_POPULATION
NUM_DRINKERS = DEF_POPULATION // 2
NUM_NON_DRINKERS = DEF_POPULATION - NUM_DRINKERS

population = 0
optimal_occupancy = 0
attendance_record = []
attendance = 0
agents_decided = 0

drinkers = None
non_drinkers = None
bar = None


def get_decision(agent):
    """
    Makes a decision randomly for the agent whether or not to go to the bar
    """
    random_num = random.random()
    if random_num <= agent["motivation"]:
        return True

    return False


def discourage(unwanted):
    """
    Discourages extra drinkers from going to the bar by decreasing motivation.
    Chooses drinkers randomly from the drinkers that went to the bar.
    """
    discouraged = 0
    while unwanted:

        if DEBUG:
            print("The members are: ", drinkers.members)
        random_drunk = random.choice(list(drinkers.members))

        if DEBUG:
            print("drinker ", random_drunk, " = ",
                  repr(drinkers[random_drunk]))

        drinkers[random_drunk]["motivation"] -= 0.05
        discouraged += 1
        unwanted -= 1

    return discouraged


def get_average_attendance(record):
    return sum(record) / len(record)


def drinker_action(agent):

    global attendance
    global attendance_record
    global agents_decided

    changed = True
    decision = get_decision(agent)
    agents_decided += 1

    if agents_decided == population:
        attendance_record.append(attendance)
        if attendance > optimal_occupancy:
            extras = attendance - optimal_occupancy
            discourage(extras)

        agents_decided = 0
        attendance = 0
        print("Avg attendance so far: ",
              get_average_attendance(attendance_record))

    if decision:
        attendance += 1

        if agent.primary_group() == non_drinkers:
            changed = False
            bar.add_switch(agent, non_drinkers,
                           drinkers)

    else:
        if agent.primary_group() == drinkers:
            changed = False
            bar.add_switch(agent, drinkers,
                           non_drinkers)

    # return False means to move
    return changed


def create_drinker(name, i, props=None):
    """
    Create an agent.
    """
    return Agent(name + str(i), action=drinker_action,
                 attrs={"motivation": 0.6})


def create_non_drinker(name, i, props=None):
    """
    Create an agent.
    """
    return Agent(name + str(i), action=drinker_action,
                 attrs={"motivation": 0.6})


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    global drinkers
    global non_drinkers
    global bar
    global population
    global optimal_occupancy
    global agents_decided

    pa = get_props(MODEL_NAME, props)
    agents_decided = 0

    drinkers = Composite("Drinkers", {"color": RED}, props=pa,
                         member_creator=create_drinker,
                         num_members=pa.get('population', DEF_POPULATION) // 2)

    non_drinkers = Composite("Non-Drinkers", {"color": BLUE}, props=pa,
                             member_creator=create_non_drinker,
                             num_members=pa.get('population',
                                                DEF_POPULATION) // 2)

    population = len(drinkers) + len(non_drinkers)
    optimal_occupancy = int(population * 0.6)

    bar = Env("bar",
              height=pa.get('grid_height', DEF_HEIGHT),
              width=pa.get('grid_width', DEF_WIDTH),
              members=[drinkers, non_drinkers],
              props=pa)

    return (bar, drinkers, non_drinkers)


def main():
    global drinkers
    global non_drinkers
    global bar

    (bar, drinkers, non_drinkers) = set_up()
    bar()

    return 0


if __name__ == "__main__":
    main()
