"""
A basic model.
Places two groups of agents in the enviornment randomly
and moves them around randomly.
"""
import copy
from indra.utils import get_props
from indra.agent import Agent
from indra.composite import Composite
from indra.space import DEF_HEIGHT, DEF_WIDTH
from indra.env import Env
from indra.display_methods import RED, BLUE

MODEL_NAME = "capital"
DEBUG = False  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

DEF_NUM_BLUE = 10
DEF_NUM_RED = 10

DEF_ENTR_CASH = 10000
DEF_RHOLDER_CASH = 0
DEF_K_PRICE = 1000

DEF_RESOURCE_HOLD = ["land", "track", "labor"]
DEF_CAP_WANTED = ["land", "track", "labor"]

resource_holders = None  # list of resource holders
entrepreneurs = None  # list of entrepreneur
market = None


def entr_action(agent):
    nearby_rholder = market.get_neighbor_of_groupX(agent,
                                                   resource_holders,
                                                   hood_size=4)
    if nearby_rholder is not None:
        if agent["cash"] > 0:

            # try to buy a resource if you have cash
            for need in agent["wants"]:
                # if find the resources entr want
                if need in resource_holders[nearby_rholder]["resources"]:
                    # update resources for the two groups
                    # print(agent.name,agent["wants"])
                    agent["wants"].remove(need)
                    # print(agent.name,agent["wants"])
                    agent["have"].append(need)
                    resource_holders[nearby_rholder]["resources"].remove(need)

                    # update cash for the two groups
                    agent["cash"] -= DEF_K_PRICE
                    resource_holders[nearby_rholder]["cash"] += DEF_K_PRICE
                    break

            if agent["wants"] and agent["have"]:
                print("I'm " + agent.name + " and I will buy resources from "
                      + str(nearby_rholder) + ". I have "
                      + str(agent["cash"]) + " dollars left."
                      + " I want " + str(agent["wants"])
                      + ", and I have " + str(agent["have"]) + ".")
            elif agent["wants"]:
                print("I'm " + agent.name + " and I will buy resources from "
                      + str(nearby_rholder) + ". I have "
                      + str(agent["cash"]) + " dollars left."
                      + " I want " + str(agent["wants"])
                      + ", and I don't have any capital.")
            elif agent["have"]:
                print("I'm " + agent.name + " and I will buy resources from "
                      + str(nearby_rholder) + ". I have "
                      + str(agent["cash"]) + " dollars left."
                      + " I got all I need, and I have "
                      + str(agent["have"]) + "!")
            return False
            # move to find resource holder

        else:
            print("I'm " + agent.name + " and I'm broke!")
    else:
        print("I'm " + agent.name + " and I can't find resources.")
    return True


def rholder_action(agent):
    if agent["resources"]:
        print("I'm " + agent.name + " and I've got resources. I have "
              + str(agent["cash"]) + " dollors now."
              + " I have " + str(agent["resources"]) + ".")
    else:
        print("I'm " + agent.name + " and I've got resources. I have "
              + str(agent["cash"]) + " dollors now."
              + " I ran out of resources!")
    # resource holder dont move
    return True


def create_entr(name, i, props=None):
    """
    Create an agent.
    """
    return Agent(name + str(i), action=entr_action,
                 attrs={"cash": DEF_ENTR_CASH,
                        "wants": copy.deepcopy(DEF_CAP_WANTED),
                        "have": []})


def create_rholder(name, i, props=None):
    """
    Create an agent.
    """
    return Agent(name + str(i), action=rholder_action,
                 attrs={"cash": DEF_RHOLDER_CASH,
                        "resources": copy.deepcopy(DEF_RESOURCE_HOLD)})


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """

    global resource_holders
    global entrepreneurs
    global market

    pa = get_props(MODEL_NAME, props)
    entrepreneurs = Composite("Entrepreneurs", {"color": BLUE},
                              member_creator=create_entr,
                              num_members=pa.get('num_blue',
                                                 DEF_NUM_BLUE))
    resource_holders = Composite("Resource_holders", {"color": RED},
                                 member_creator=create_rholder,
                                 num_members=pa.get('num_red',
                                                    DEF_NUM_RED))

    market = Env("neighborhood",
                 height=pa.get('grid_height', DEF_HEIGHT),
                 width=pa.get('grid_width', DEF_WIDTH),
                 members=[resource_holders, entrepreneurs],
                 props=pa)

    return (market, resource_holders, entrepreneurs)


def main():
    global resource_holders
    global entrepreneurs
    global market

    (market, blue_group, red_group) = set_up()

    if DEBUG2:
        print(market.__repr__())

    market()
    return 0


if __name__ == "__main__":
    main()
