"""
    This is the flocking model written in indra.
"""
import math
import random

from indra.utils import get_props
from indra.agent import Agent, X, Y
from indra.composite import Composite
from indra.space import DEF_HEIGHT, DEF_WIDTH, distance
from indra.env import Env
from indra.display_methods import BLUE, TREE
MODEL_NAME = "flocking"
DEBUG = True  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

DEF_NUM_BIRDS = 2
DEF_DESIRED_DISTANCE = 2
ACCEPTABLE_DEV = .05
BIRD_MAX_MOVE = 1

HALF_CIRCLE = 180
FULL_CIRCLE = 360

flock = None
the_sky = None


def invert_direction(angle):
    """
    Inverts the current angle.
    """
    return (angle + HALF_CIRCLE) % FULL_CIRCLE


def random_direction():
    """
    Returns a random angle of direction.
    """
    return random.randint(0, FULL_CIRCLE)


def calc_angle(agent1, agent2):
    """
    Calculates the angle between two agents and returns the
    angle
    """
    pos1 = agent1.get_pos()
    pos2 = agent2.get_pos()
    x = pos2[X] - pos1[X]
    y = pos2[Y] - pos1[Y]
    angle = math.degrees(math.atan2(y, x))
    if angle < 0:
        angle = angle + FULL_CIRCLE
    return angle


def bird_action(this_bird):
    """
    Finds the closest agent to the current agent and calculates
    the distance between the two, inverting the direction if the
    distance is too close.
    """
    nearest_bird = this_bird.locator.get_closest_agent(this_bird)
    if nearest_bird is not None:
        curr_distance = distance(this_bird, nearest_bird)
        if DEBUG:
            print("Distance between ", nearest_bird, " and ", this_bird,
                  " is ", curr_distance)
        if abs(curr_distance - DEF_DESIRED_DISTANCE) < (DEF_DESIRED_DISTANCE
                                                        * ACCEPTABLE_DEV):
            this_bird["angle"] = random_direction()
        else:
            this_bird["angle"] = calc_angle(this_bird, nearest_bird)
        if DEBUG:
            print(this_bird.name, "'s angle rel. to ", nearest_bird.name,
                  "is", this_bird["angle"])

        if curr_distance < DEF_DESIRED_DISTANCE:
            this_bird["angle"] = invert_direction(this_bird["angle"])

    return False


def create_bird(name, i, props=None):
    """
    Creates a bird with a numbered name and an action function
    making it flock.
    """
    return Agent(name + str(i), action=bird_action,
                 attrs={"max_move": BIRD_MAX_MOVE,
                        "angle": 0})


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    pa = get_props(MODEL_NAME, props)

    flock = Composite("Birds", {"color": BLUE, "marker": TREE},
                      member_creator=create_bird,
                      num_members=pa.get('num_birds', DEF_NUM_BIRDS))

    the_sky = Env("the_sky",
                  height=pa.get('grid_height', DEF_HEIGHT),
                  width=pa.get('grid_width', DEF_WIDTH),
                  members=[flock])
    return (the_sky, flock)


def fl_unrestorable(env):
    global flock
    global the_sky
    the_sky = env
    flock = env.registry["Birds"]


def main():
    global flock
    global the_sky

    (the_sky, flock) = set_up()
    the_sky()
    return 0


if __name__ == "__main__":
    main()
