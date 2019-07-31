"""
El Farol Bar Problem
A problem to check if it's possible for the bar to be
occupied by 60% of the population every time
"""

import random

from propargs.propargs import PropArgs
from indra.utils import get_prop_path
from indra.agent import Agent
from indra.composite import Composite
from indra.space import DEF_HEIGHT, DEF_WIDTH
from indra.env import Env
from indra.display_methods import BLUE

MODEL_NAME = "drunks"

DEF_NUM_DRINKERS = 10

POPULATION = 10
OPTIMAL_OCCUPANCY = 0.6 * POPULATION
MOTIVATION = [0.6] * POPULATION

drinkers = None
bar = None


def get_decision(actor):
    random_integer = random.randint(1, 100) / 100
    if random_integer <= MOTIVATION[actor]:
        return 1

    return 0


def discourage(unwanted, attenders):
    while unwanted:
        demotivate_person = attenders[random.randint(0, len(attenders) - 1)]
        MOTIVATION[demotivate_person] -= 0.05
        unwanted -= 1

    return 0


def random_drunks(weekends=10):
    # print("Motivation: ", MOTIVATION)

    attendance_record = []
    while weekends > 0:
        person = 0
        attendance = 0
        attenders = []
        while person < POPULATION:
            decision = get_decision(person)
            if decision:
                attendance += 1
                attenders.append(person)

            person += 1

        if attendance > OPTIMAL_OCCUPANCY:
            extras = attendance - OPTIMAL_OCCUPANCY
            discourage(extras, attenders)

        attendance_record.append(attendance)
        weekends -= 1

    return attendance_record


def get_average_attendance(record):
    i = len(record)
    sum_attendance = 0
    while i:
        sum_attendance += record[i - 1]
        i -= 1

    return sum_attendance / len(record)


def drinker_action(agent):
    print("I'm " + agent.name + " and I need a drink.")
    # return False means to move
    return False


def create_drinker(color, i):
    """
    Create an agent.
    """
    return Agent("drunk" + str(i), action=drinker_action,
                 attrs={"going_to_bar": False})


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    ds_file = get_prop_path(MODEL_NAME)
    if props is None:
        pa = PropArgs.create_props(MODEL_NAME,
                                   ds_file=ds_file)
    else:
        pa = PropArgs.create_props(MODEL_NAME,
                                   prop_dict=props)

    drinkers = Composite("Drinkers", {"color": BLUE},
                         member_creator=create_drinker,
                         num_members=pa.get('num_drinkers',
                                            DEF_NUM_DRINKERS))

    bar = Env("env",
              height=pa.get('grid_height', DEF_HEIGHT),
              width=pa.get('grid_width', DEF_WIDTH),
              members=[drinkers],
              props=pa)

    return (bar, drinkers)


def main():
    global drinkers
    global bar

    (bar, drinkers) = set_up()

    bar()

    return 0


if __name__ == "__main__":
    main()