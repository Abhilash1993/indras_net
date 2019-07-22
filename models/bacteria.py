"""
    This is the fashion model re-written in indra.
"""

from propargs.propargs import PropArgs
from indra.utils import get_prop_path
from indra.agent import Agent
from indra.composite import Composite
from indra.space import DEF_HEIGHT, DEF_WIDTH, distance
from indra.env import Env
from indra.display_methods import RED, GREEN, YELLOW
from random import randint
import sys

MODEL_NAME = "bacteria"
DEBUG = True  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

DEF_NUM_BACT = 1
DEF_NUM_TOXINS = 1
DEF_NUM_NUTRIENTS = 1
DEF_THRESHOLD = -0.2
DEF_TOXIN_MOVE = 1
DEF_BACTERIUM_MOVE = 3
DEF_NUTRIENT_MOVE = 2

bacteria = None
toxins = None
nutrients = None
petri_dish = None


def calc_toxin(group, agent):
    """
    Calculate the strength of a toxin / nutrient field for an agent.
    """
    toxin_strength = float(distance(group["Toxins0"], agent)) * (-1)
    return toxin_strength


def calc_nutrient(group, agent):
    nutrient_strength = float(distance(group["Nutrients0"], agent))
    return nutrient_strength


def bacterium_action(agent, **kwargs):
    """
    Algorithm:
        1) sense env
            (toxin_level = calc_toxin(toxins, agent))
        2) see if it is worse or better than previous env
        3) if worse, change direction
            (agent["angle"] = new_angle)
        4) move (done automatically by returning False)
    """
    print("I'm " + agent.name + " and I'm hungry.")

    toxin_level = calc_toxin(toxins, agent)
    nutrient_level = calc_nutrient(nutrients, agent)

    if agent["prev_toxicity"] is not None:
        toxin_change = calc_toxin(toxins, agent) - agent["prev_toxicity"]
    else:
        toxin_change = sys.maxsize * (-1)

    if agent["prev_nutricity"] is not None:
        nutrient_change = calc_nutrient(nutrients,
                                        agent) - agent["prev_nutricity"]
    else:
        nutrient_change = sys.maxsize * (-1)

    threshold = DEF_THRESHOLD
    agent["prev_toxicity"] = toxin_level
    agent["prev_nutricity"] = nutrient_level

    if (toxin_change + nutrient_change <= 0) or (threshold - toxin_level >= 0):
        if agent["angle"] is None:
            new_angle = randint(0, 360)
        else:
            angle_shift = randint(45, 315)
            new_angle = agent["angle"] + angle_shift
        if (new_angle > 360):
            new_angle = new_angle % 360
        agent["angle"] = new_angle
        print("The new angle is:", agent["angle"])

    # return False means to move
    return False


def toxin_action(agent, **kwargs):
    print("I'm " + agent.name + " and I'm poisonous.")
    # return False means to move
    return False


def nutrient_action(agent, **kwargs):
    print("I'm " + agent.name + " and I'm nutrious.")
    # return False means to move
    return False


def create_bacterium(name, i, pa):
    """
    Create a baterium.
    """
    bacterium = Agent(name + str(i), action=bacterium_action)
    bacterium["prev_toxicity"] = None
    bacterium["prev_nutricity"] = None
    bacterium["angle"] = None
    bacterium["max_move"] = pa.get("bacterium_move", DEF_BACTERIUM_MOVE)
    print("the user input for bacterium_move:", bacterium["max_move"])
    return bacterium


def create_toxin(name, i, pa):
    """
    Create a toxin.
    """
    toxin = Agent(name + str(i), action=toxin_action)
    toxin["max_move"] = pa.get("toxin_move", DEF_TOXIN_MOVE)
    print("the user input for toxin_move:", toxin["max_move"])
    return toxin


def create_nutrient(name, i, pa):
    """
    Create a nutrient.
    """
    nutrient = Agent(name + str(i), action=nutrient_action)
    nutrient["max_move"] = pa.get("nutrient_move", DEF_NUTRIENT_MOVE)
    print("the user input for nutrient_move:", nutrient["max_move"])
    return nutrient


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

    toxins = Composite("Toxins", {"color": RED})
    for i in range(pa.get('num_toxins', DEF_NUM_TOXINS)):
        toxins += create_toxin("Toxins", i, pa)

    nutrients = Composite("Nutrients", {"color": YELLOW})
    for i in range(pa.get('num_nutrients', DEF_NUM_TOXINS)):
        nutrients += create_nutrient("Nutrients", i, pa)

    bacteria = Composite("Bacteria", {"color": GREEN})
    for i in range(pa.get('num_bacteria', DEF_NUM_BACT)):
        bacteria += create_bacterium("Bacteria", i, pa)

    petri_dish = Env("Petrie dish",
                     height=pa.get('grid_height', DEF_HEIGHT),
                     width=pa.get('grid_width', DEF_WIDTH),
                     members=[toxins, nutrients, bacteria],
                     props=pa)
    return (petri_dish, toxins, nutrients, bacteria)


def main():
    global bacteria
    global toxins
    global nutrients
    global env

    (petri_dish, toxins, nutrients, bacteria) = set_up()

    if DEBUG2:
        print(petri_dish.__repr__())

    petri_dish()
    return 0


if __name__ == "__main__":
    main()
