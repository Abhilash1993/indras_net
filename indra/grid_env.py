"""
grid_env.py

This is an adaptation of the:

Mesa Space Module
=================================

From the GMU Mesa project.

Objects used to add a spatial component to a model.

GridEnv: base grid, a simple list-of-lists.

MultiGridEnv: extension to Grid where each cell is a set of objects.

"""

# Instruction for PyLint to suppress variable name errors, 
# since we have a
# good reason to use one-character variable names for x and y.
# pylint: disable=invalid-name

import random
import itertools
import logging
import indra.spatial_env as se


RANDOM = -1


def pos_msg(agent):
    """
    A convenience function for displaying
    an entity's position.
    """
    if agent.pos is not None:
        x = agent.pos[0]
        y = agent.pos[1]
        return("Position for " + 
               agent.name + " is "
               + str(x) + ", " + str(y))
    else:
        return(agent.name + " is not located!")


class GridEnv(se.SpatialEnv):
    """
    Base class for a square grid.

    Grid cells are indexed by [y][x], 
    where [0][0] is assumed to be the top-left
    and [height-1][width-1] is the bottom-right.
    If a grid is toroidal, the top
    and bottom, and left and right, edges wrap to each other

    Properties:
        width, height: The grid's width and height.
        torus: Boolean which determines whether
            to treat the grid as a torus.

        grid: Internal list-of-lists which holds
            the grid cells themselves.
        default_val: Lambda function to populate
            each grid cell with None.

    Methods:
        get_neighbors: Returns the objects surrounding a given cell.
        get_neighborhood: Returns the cells surrounding a given cell.
        get_cell_list_contents: Returns the contents of a list of cells
            ((x,y) tuples)
    """

    torus = False
    grid = None
    default_val = lambda s: None


    class GridOccupiedIter:
        """
        Return just the occupied cells of the grid.
        """

        def __init__(self, grid):
            self.grid = grid
            self.x = 0
            self.y = 0


        def __iter__(self):
            return self


        def __next__(self):
            while self.y < self.grid.height:
                # print("in row " + str(self.y))
                while self.x < self.grid.width:
                    # print("in column " + str(self.x))
                    if not self.grid.is_cell_empty(self.x, self.y):
                        ret = [self.grid[self.y][self.x],
                              self.x, self.y]
                        self.x += 1
                        return ret
                    else:
                        self.x += 1
                self.x = 0
                self.y += 1
            else:
                raise StopIteration()


    def __init__(self, name, height, width, torus=torus,
                 model_nm=None):
        """
        Create a new grid.

        Args:
            height, width: The height and width of the grid
            torus: Boolean whether the grid wraps or not.
        """
        super().__init__(name, width, height, preact=True,
                         postact=False, model_nm=model_nm)

        self.torus = torus
        self.total_cells = self.height * self.width
        self.filled_cells = 0

        self.grid = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                row.append(self.default_val())
            self.grid.append(row)


    def __iter__(self):
        # create an iterator that chains the
        #  rows of grid together as if one list:
        return itertools.chain(*self.grid)


    def __getitem__(self, index):
        return self.grid[index]


    def _get_x(self, x):
        """
        Convert X coordinate, handling torus looping.
        """
        if x >= 0 and x < self.width:
            return x
        if not self.torus:
            raise Exception("Coordinate out of bounds.")
        else:
            return x % self.width


    def _get_y(self, y):
        """
        Convert Y coordinate, handling torus looping.
        """
        if y >= 0 and y < self.height:
            return y
        if not self.torus:
            raise Exception("Coordinate out of bounds.")
        else:
            return y % self.height


    def occupied_iter(self):
        return GridEnv.GridOccupiedIter(self)


    def get_neighborhood(self, x, y, moore,
                         include_center=False, radius=1):
        """
        Return a list of cells that are in the 
        neighborhood of a certain point.

        Args:
            x, y: Coordinates for the neighborhood to get.
            moore: If True, return Moore neighborhood
                        (including diagonals)
                   If False, return Von Neumann neighborhood 
                        (exclude diagonals)
            include_center: If True, return the (x, y) cell as well.
                            Otherwise, return surrounding cells only.
            radius: radius, in cells, of neighborhood to get.

        Returns:
            A list of coordinate tuples representing the neighborhood;
                at most 9 if
                Moore, 5 if Von Neumann
                (8 and 4 if not including the center).
        """
        coordinates = []
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                if dx == 0 and dy == 0 and not include_center:
                    continue
                # Skip diagonals in Von Neumann neighborhood.
                if not moore and dy != 0 and dx != 0:
                    continue
                # Skip diagonals in Moore neighborhood when distance > radius
                if moore and (dy ** 2 + dx ** 2) ** .5 > radius:
                    continue
                # Skip if not a torus and new coords out of bounds.
                if not self.torus and (not (0 < dx + x < self.width) or
                                           not (0 < dy + y < self.height)):
                    continue

                px = self._get_x(x + dx)
                py = self._get_y(y + dy)
                coordinates.append((px, py))
        return coordinates


    def get_neighbors(self, x, y, moore,
                      include_center=False, radius=1):
        """
        Return a list of neighbors to a certain point.

        Args:
            x, y: Coordinates for the neighborhood to get.
            moore: If True, return Moore neighborhood
                    (including diagonals)
                   If False, return Von Neumann neighborhood
                     (exclude diagonals)
            include_center: If True, return the (x, y) cell as well.
                            Otherwise,
                            return surrounding cells only.
            radius: radius, in cells, of neighborhood to get.

        Returns:
            A list of non-None objects in the given neighborhood;
            at most 9 if Moore, 5 if Von-Neumann
            (8 and 4 if not including the center).
        """
        neighborhood = self.get_neighborhood(x, y, moore,
                                             include_center,
                                             radius)
        print("For x = " + str(x)
              + " and y = " + str(y)
              + " we have nayb cells of: ")
        for nx, ny in neighborhood:
            print("nx = " + str(nx) + " ny = " + str(ny))
        return self.get_cell_list_contents(neighborhood)


    def get_cell_list_contents(self, cell_list):
        """
        Args:
            cell_list: Array-like of (x, y) tuples

        Returns:
            A list of the contents of the cells identified in cell_list
        """
        contents = []
        for x, y in cell_list:
            self._add_members(contents, x, y)
        return contents


    def exists_empty_cells(self):
        """
        Return True if any cells empty else False.
        """
#        print("Comparing filled " + 
#              str(self.filled_cells) + " total of "
#              + str(self.total_cells))
        return self.filled_cells < self.total_cells


    def position_agent(self, agent, x=RANDOM, y=RANDOM):
        """
        Position an agent on the grid.
        If x or y are positive, they are used, but if negative, 
        we get a random position.
        Ensure this random position is not occupied (in Grid).
        """
        print("Positioning " + agent.name)
        if x == RANDOM or y == RANDOM:
            got_cell = False
            while not got_cell and self.exists_empty_cells():
                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)
                if self.is_cell_empty(x, y):
                    got_cell = True

            if not got_cell:
                logging.error("Grid full; "
                              + agent.name + " not added.")
                return
                    

        self.grid[y][x] = agent
        self.filled_cells += 1

        agent.pos = [x, y]


    def _add_members(self, target_list, x, y):
        """
        Helper method to append the contents of a cell to the given list.
        Override for other grid types.
        """
        if self.grid[y][x] is not None:
            target_list.append(self.grid[y][x])


    def is_cell_empty(self, x, y):
        return self.grid[y][x] is None


class MultiGridEnv(GridEnv):
    """
    Grid where each cell can contain more than one object.

    Grid cells are indexed by [y][x], where [0][0] is assumed to be the top-left
    and [height-1][width-1] is the bottom-right. If a grid is toroidal, the top
    and bottom, and left and right, edges wrap to each other.

    Each grid cell holds a set object.

    Properties:
        width, height: The grid's width and height.

        torus: Boolean which determines whether to treat the grid as a torus.

        grid: Internal list-of-lists which holds the grid cells themselves.
        default_val: Lambda function to populate grid cells with an empty set.

    Methods:
        get_neighbors: Returns the objects surrounding a given cell.
    """

    default_val = lambda s: set()

    def _add_members(self, target_list, x, y):
        """
        Helper method to add all objects in the given cell to the target_list.
        """
        for a in self.grid[y][x]:
            target_list.append(a)


    def get_pos_components(self, agent):
        return a.pos


