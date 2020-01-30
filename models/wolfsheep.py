"""
    This is wolf-sheep re-written in indra.
"""
from indra.agent import Agent
from indra.composite import Composite
from indra.display_methods import TAN, GRAY
from indra.env import Env
from indra.registry import get_registration
from indra.space import in_hood
from indra.utils import get_props

MODEL_NAME = "wolfsheep"
DEBUG = False  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off
NUM_WOLVES = 8
NUM_SHEEP = 20
HOOD_SIZE = 3
MEADOW_HEIGHT = 10
MEADOW_WIDTH = 10

WOLF_LIFESPAN = 5
WOLF_REPRO_PERIOD = 6

SHEEP_LIFESPAN = 8
SHEEP_REPRO_PERIOD = 3

AGT_WOLF_NAME = "wolf"
AGT_SHEEP_NAME = "sheep"

COMP_WOLF_NAME = "wolves"
COMP_SHEEP_NAME = "sheep"

ERR_MSG = "Invalid agent name"

wolves = None
sheep = None
meadow = None
wolves_created = 0
sheep_created = 0

wolf_repro = WOLF_REPRO_PERIOD
wolf_life = WOLF_LIFESPAN
sheep_repro = SHEEP_REPRO_PERIOD
sheep_life = SHEEP_LIFESPAN


def isactive(agent, *args):
    """
    See if what wolf is going to eat is alive!
    """
    return agent.is_active()


def live_and_close(agent, *args):
    return in_hood(agent, *args) and isactive(agent, *args)


def eat(agent, prey):
    """
     Wolf's duration increases by sheep's duration
     """
    if DEBUG:
        print("The prey is alive? ", isactive(prey))
        print(str(agent) + " is eating " + str(prey))
    agent.duration += prey.duration
    prey.die()


def get_prey(agent, sheep):
    """
        Wolves eat active sheep from the neighbourhood
    """
    prey = None
    hood = sheep.subset(in_hood, agent, HOOD_SIZE, name="hood")
    if len(hood) > 0:
        live_hood = hood.subset(isactive, agent, name="livehood")
        if len(live_hood) > 0:
            prey = live_hood.rand_member()
    return prey


def reproduce(agent, create_func, num_created, group):
    """
    Agents reproduce when "time_to_repr" reaches 0
    """
    if agent["time_to_repr"] == 0:
        meadow.add_child(group)
        agent["time_to_repr"] = agent["orig_repr_time"]
        return True
    else:
        return False


def sheep_action(agent):
    global sheep
    global sheep_created

    agent["time_to_repr"] -= 1
    reproduce(agent, create_sheep, sheep_created, sheep)
    return False


def wolf_action(agent):
    global wolves
    global wolves_created
    global sheep

    prey = get_prey(agent, sheep)
    if prey is not None:
        eat(agent, prey)
    agent["time_to_repr"] -= 1
    reproduce(agent, create_wolf, wolves_created, wolves)
    return False


def create_wolf(name, i, props=None):
    """
    Method to create wolf
    """
    global wolves_created
    global meadow

    wolves_created += 1
    return Agent(AGT_WOLF_NAME + str(i),
                 duration=wolf_life,
                 action=wolf_action,
                 env=meadow,
                 attrs={"time_to_repr": wolf_repro,
                        "orig_repr_time": wolf_repro})


def create_sheep(name, i, props=None):
    """
    Method to create sheep
    """
    global sheep_created
    global meadow

    sheep_created += 1
    return Agent(AGT_SHEEP_NAME + str(i), duration=sheep_life,
                 action=sheep_action,
                 env=meadow,
                 attrs={"time_to_repr": sheep_repro,
                        "orig_repr_time": sheep_repro})


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    global wolves
    global sheep
    global meadow

    pa = get_props(MODEL_NAME, props)

    wolves = Composite(COMP_WOLF_NAME, {"color": TAN}, props=pa,
                       member_creator=create_wolf,
                       num_members=pa.get('num_wolves', NUM_WOLVES))

    if DEBUG2:
        print(wolves.__repr__())

    sheep = Composite(COMP_SHEEP_NAME, {"color": GRAY}, props=pa,
                      member_creator=create_sheep,
                      num_members=pa.get('num_sheep', NUM_SHEEP))

    if DEBUG2:
        print(sheep.__repr__())

    meadow = Env("meadow", members=[wolves, sheep],
                 height=pa.get('meadow_height', MEADOW_HEIGHT),
                 width=pa.get('meadow_width', MEADOW_WIDTH),
                 props=pa)
    return (meadow, wolves, sheep)


def restore_globals(env):
    global wolves
    global sheep
    global meadow
    meadow = env
    wolves = get_registration(COMP_WOLF_NAME)
    sheep = get_registration(COMP_SHEEP_NAME)


def main():
    global wolves
    global sheep
    global meadow

    (meadow, wolves, sheep) = set_up()

    if DEBUG2:
        print(meadow.__repr__())

    meadow()
    return 0


if __name__ == "__main__":
    main()
