"""
This file defines Space, which is a collection
of agents related spatially.
"""
from random import randint
from math import sqrt
from indra2.agent import is_composite
from indra2.composite import Composite

DEF_WIDTH = 10
DEF_HEIGHT = 10

MAX_WIDTH = 200
MAX_HEIGHT = 200

DEBUG = True
DEBUG2 = False


def out_of_bounds(x, y, x1, y1, x2, y2):
    """
    Is point x, y off the grid defined by x1, y1, x2, y2?
    """
    return(x < x1 or x >= x2
           or y < y1 or y >= y2)


def distance(a1, a2):
    """
    We're going to return the distance between two objects. That calculation
    is easy if they are both located in space, but what if one of them is
    not? For now, we will return 0, but is that right?
    """
    if (not a1.islocated()) or (not a2.islocated()):
        return 0.0
    else:
        return sqrt(
            ((a2.get_x() - a1.get_x()) ** 2)
            + ((a2.get_y() - a1.get_y()) ** 2)
        )


def in_hood(agent, other, hood_sz):
    d = distance(agent, other)
    if DEBUG2:
        print("Distance between " + str(agent)
              + " and " + str(other) + " is "
              + str(d))
    return d < hood_sz


class Space(Composite):
    """
    A collection of entities that share a space.
    The way we handle space assignment is, default to random,
    and assign locations after we get our members.
    """

    def __init__(self, name, width=DEF_WIDTH, height=DEF_HEIGHT,
                 attrs=None, members=None):
        super().__init__(name, attrs=attrs, members=members)
        self.width = width
        self.height = height

        # the location of members in the space
        self.locations = {}

        # by making two class methods for place_members and
        # place_member, we allow two places to override
        self.place_members(self.members)

    def grid_size(self):
        """
        How big is da grid?
        """
        return self.width * self.height

    def is_full(self):
        """
        Is da grid full?
        """
        return len(self.locations) >= self.grid_size()

    def place_members(self, members):
        """
        Locate all members of this space in x, y grid.
        Default is to randomly place members.
        """
        if members is not None:
            for nm, mbr in members.items():
                if not is_composite(mbr):  # by default don't locate groups
                    self.place_member(mbr)
                else:  # place composite's members
                    self.place_members(mbr.members)

    def rand_x(self, low=0, high=None):
        """
        Return a random x-value between 0 and this space's width,
        if no constraints are passed.
        With constraints, narrow to that range.
        """
        high = self.width - 1 if high is None else high
        return randint(low, high)

    def rand_y(self, low=0, high=None):
        """
        Return a random y-value between 0 and this space's height
        if no constraints are passed.
        With constraints, narrow to that range.
        """
        high = self.height - 1 if high is None else high
        return randint(low, high)

    def place_member(self, mbr, max_move=MAX_WIDTH):
        """
        By default, locate a member at a random x, y spot in our grid.
        max_move is not used yet!
        """
        if self.is_full():
            self.user.log("Can't fit no more folks in this space!")
            return None

        if not is_composite(mbr):
            x, y = self.rand_x(), self.rand_y()
            if (x, y) not in self.locations:
                if mbr.islocated():
                    self.move_location(x, y, mbr.get_x(), mbr.get_y())
                else:
                    self.add_location(x, y, mbr)
                mbr.set_pos(x, y)
                return (x, y)
            else:
                # if the random position is already taken,
                # find the member a new position
                return self.place_member(mbr)
        else:
            return self.place_members(mbr.members)

    def move(self, mbr, max_move=2):
        self.place_member(mbr, max_move)

    def __iadd__(self, other):
        super().__iadd__(other)
        self.place_member(other)
        return self

    def add_location(self, x, y, member):
        """
        Add a new member to the locations of positions of members.
        """
        self.locations[(x, y)] = member

    def move_location(self, nx, ny, ox, oy):
        """
        Move a member to a new position.
        """
        self.locations[(nx, ny)] = self.locations[(ox, oy)]
        del self.locations[(ox, oy)]

    def remove_location(self, x, y):
        """
        Remove a member from the locations.
        """
        del self.locations[(x, y)]
