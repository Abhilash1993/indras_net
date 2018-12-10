"""
grid_env.py

This is an adaptation of the:

Mesa Space Module
=================================

From the GMU Mesa project.

Objects used to add a spatial component to a model.

GridEnv: base grid, a simple list-of-lists.

"""

# Instruction for PyLint to suppress variable name errors,
# since we have a good reason to use one-character variable names for x and y.
# pylint: disable=invalid-name

import math
import random
import itertools
import logging
import indra.node as node
import indra.spatial_env as se
import models.grid as ta
import indra.grid_agent as ga

RANDOM = -1

X = 0
Y = 1


def out_of_bounds(x, y, x1, y1, x2, y2):
    """
    Is point x, y off the grid defined by x1, y1, x2, y2?
    """
    return(x < x1 or x >= x2
           or y < y1 or y >= y2)


class Cell(node.Node):
    """
    Cells hold the grid contents.
    They also have a record of where they are in the grid.
    """
    def __init__(self, coords, contents=None):
        super().__init__(None)
        self.__contents = None
        self.coords = coords

    @property
    def contents(self):
        return self.__contents

    @contents.setter
    def contents(self, item):
        old_item = self.__contents
        self.__contents = item
        if item is not None:
            item.cell = self
        if old_item is not None:
            old_item.cell = None

    def is_empty(self):
        """
        Return True if cell empty, else False.
        """
        return not self.contents

    def add_item(self, new_item):
        """
        Add new_item to cell contents.
        Every cell item must have a cell
        field to store its location.
        """
        self.contents = new_item

    def remove_item(self, item):
        """
        If item is our object, set contents to None.
        If that is not our object, do nothing.
        """
        if item == self.contents:
            self.contents = None
            
    def to_json(self):
        """
        We're going to make a dictionary of the 'safe' parts of the object to
        output to a json file. (We can't output the env, for instance, since
        IT contains a reference to each agent!)
        """
        safe_fields = {}
        safe_fields["coordx"] = self.coords[0]
        safe_fields["coordy"] = self.coords[1]
        return safe_fields

    @classmethod
    def from_json(cls, json_input):
        coords = (json_input["coordx"],
                  json_input["coordy"])
        return cls(coords=coords)

class OutOfBounds(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class CompositeView(ga.GridView):
    """
    A composite view combines several other views.
    """
    def __init__(self, grid, views):
        self.grid = grid
        self.views = list(views)  # the parameter will be a tuple

    def __iter__(self):
        """
        Iterate over all our cells: note,
        right now, this return the center cell twice.
        """
        return itertools.chain(self.views)

    def out_of_bounds(self, x, y):
        """
        Is x, y not in this view?
        It is not only if it is not in ANY of the sub-views.
        """
        for view in self.views:
            if not view.out_of_bounds(x, y):
                return False
        return True

    def get_neighbors(self):
        """
        Return all of the occupied cells in this view.
        """
        neighbors = []
        for view in self.views:
            neighbors += view.get_neighbors()
        return neighbors


class GridEnv(se.SpatialEnv):
    """
    Base class for a rectangular grid.

    If a grid is toroidal, the top
    and bottom, and left and right, edges wrap to each other

    Properties:
        width, height: The grid's width and height.
        torus: Boolean which determines whether
            to treat the grid as a torus.

        grid: Internal list-of-lists which holds
            the grid cells themselves.

    Methods:
        get_neighbors: Returns the objects surrounding a given cell.
    """

    def __init__(self, name, width, height, torus=False,
                preact=False, postact=False, model_nm=None, props=None):
        """
        Create a new grid.

        Args:
            height, width: The height and width of the grid
            torus: Boolean whether the grid wraps or not.
        """
        super().__init__(name, width, height,
                         preact=preact, postact=postact,
                         model_nm=model_nm, props=props)

        self.torus = torus
        self.num_cells = width * height
        
        self.__init_unrestorables()
            
    def __init_unrestorables(self):
        self.grid = []
        self.empties = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                cell = self.__new_cell__((x, y))
                row.append(cell)
                self.empties.append(cell)
            self.grid.append(row)
        
        self.set_agent_color()

    def __iter__(self):
        # create an iterator that chains the
        #  rows of grid together as if one list:
        return itertools.chain(*self.grid)

    def __getitem__(self, index):
        return self.grid[index]

    def __new_cell__(self, coords):
        return Cell(coords)

    def add_agent(self, agent, x=RANDOM, y=RANDOM, position=True):
        """
        Add an agent and link to cell if present in agent.
        """
        super().add_agent(agent, x, y, position)
        if agent.cell is not None:
            if agent.cell.contents is not agent:
                agent.cell.add_item(agent)

    def remove_agent(self, agent):
        """
        Remove agent from pop and from grid.
        """
        super().remove_agent(agent)
        if agent.cell is not None:
            agent.cell.remove_item(agent)

    def torus_adj(self, coord, dim_len):
        """
        Convert coordinate, handling torus looping.
        """
        if self.torus:
            coord %= dim_len
        return coord

    def out_of_bounds(self, x, y):
        """
        Is point x, y off the grid?
        """
        return out_of_bounds(x, y, 0, 0, self.width, self.height)

    def get_max_dist(self):
        """
            Args: none

            Returns: The furthest move possible in this env.
        """
        return math.sqrt(self.width**2 + self.height**2)

    def get_col_view(self, col, low=None, high=None):
        """
        Return a view of a single column.
        It will be the whole column from the grid,
        unless low or high are passed.
        """
        if low is None:
            low = 0
        if high is None:
            high = self.height
        return ga.GridView(self, col, low, col + 1, high)

    def get_row_view(self, row, left=None, right=None):
        """
        Return a view of a single row
        It will be the whole row from the grid,
        unless left or right are passed.
        """
        if left is None:
            left = 0
        if right is None:
            right = self.width
        return ga.GridView(self, left, row, right, row + 1)

    def _adjust_coords(self, center, distance, max_val):
        coord1 = max(0, center - distance)
        coord2 = min(max_val, center + distance + 1)
        return (coord1, coord2)

    def get_vonneumann_view(self, center, distance):
        """
        Return a Von Neumann view (row and col)
        centered on center.
        """
        (x, y) = center
        (x1, x2) = self._adjust_coords(x, distance, self.width)
        (y1, y2) = self._adjust_coords(y, distance, self.height)
        col_view = self.get_col_view(x, y1, y2)
        row_view = self.get_row_view(y, x1, x2)
        return CompositeView(self, (col_view, row_view))

    def get_square_view(self, center, distance):
        """
        Attempt to return a view of a square centered on center.
        This might return a non-square rectangle
        if the center is near an edge.
        """
        (center_x, center_y) = center
        (x1, x2) = self._adjust_coords(center_x, distance, self.width)
        (y1, y2) = self._adjust_coords(center_y, distance, self.height)
        return ga.GridView(self, x1, y1, x2, y2)

    def neighbor_iter(self, x, y, distance=1, moore=True, view=None, shuffle=False):
        """
        Iterate over our neighbors.
        """
        neighbors = self.get_neighbors(x, y, distance, moore, view)
        if shuffle:
            random.shuffle(neighbors)
        return map(lambda x: x.contents, iter(neighbors))

    def get_neighbors(self, x, y, distance=1, moore=True, view=None):
        """
        Return a list of neighbors within a certain purview.

        Args:
            x, y: Coordinates for the neighborhood to get.
            distance: distance, in cells, of neighborhood to get.
            view: we may already have a view we are working with.

        Returns:
            A list of non-None objects in the given neighborhood;
            at most 9 if Moore, 5 if Von-Neumann
            (8 and 4 if not including the center).
        """
        if view is None:
            if moore:
                view = self.get_square_view((x, y), distance)
            else:
                view = self.get_vonneumann_view((x, y), distance)
        return view.get_neighbors()

    def exists_empty_cells(self, grid_view=None):
        """
        Return True if any cells empty else False.
        """
        if len(self.empties) <= 0:
            # if no empties anywhere then none in any view!
            return False
        elif grid_view is not None:
            if len(grid_view.empties) <= 0:
                return False
        return True

    def move_to_empty(self, agent, grid_view=None):
        """
        Moves agent to an empty cell, vacating agent's old cell.
        """
        empty_cell = self.find_empty(grid_view)
        if empty_cell is None:
            logging.error("Agent could not move because no cells are empty")
        else:
            self._move_item(agent, empty_cell)
    
    #Functions by JacEkko (John Knox)====================================================
    def get_angle(self, agent1, agent2, grid_view=None):
        """
        Use two agents to find the angle they make, using their coordinates
        """
        dy = abs(agent1.pos[Y] - agent2.pos[Y])
        dx = abs(agent1.pos[X] - agent2.pos[X])
        if(dy == 0):
            return 180
        if(dx == 0):
            return 90
        else:
            rad = math.atan(dy / dx)
            angle = rad * (180 / math.pi)
            return angle
        
    def move_to_agent(self, tar_agent, dest_agent, steps, grid_view=None):
        print("MTA Tar: ", tar_agent.pos[X], ",", tar_agent.pos[Y])
        print("MTA Dest: ", dest_agent.pos[X], ",", dest_agent.pos[Y])
        if(tar_agent.pos[X] > dest_agent.pos[X]):
            if self.is_cell_empty(tar_agent.pos[X] - steps,
                             tar_agent.pos[Y]):
                self.move(tar_agent, tar_agent.pos[X] - steps,
                         tar_agent.pos[Y])#tar_agent.pos[X] -= steps
        else:
            if self.is_cell_empty(tar_agent.pos[X] + steps,
                             tar_agent.pos[Y]):
                self.move(tar_agent, tar_agent.pos[X] + steps,
                         tar_agent.pos[Y])#tar_agent.pos[X] += steps
        if(tar_agent.pos[Y] < dest_agent.pos[Y]):
            if self.is_cell_empty(tar_agent.pos[X],
                             tar_agent.pos[Y] - steps):
                self.move(tar_agent, tar_agent.pos[X],
                         tar_agent.pos[Y] - steps)#tar_agent.pos[Y] -= steps
        else:
            if self.is_cell_empty(tar_agent.pos[X],
                             tar_agent.pos[Y] + steps):
                self.move(tar_agent, tar_agent.pos[X],
                         tar_agent.pos[Y] + steps)#tar_agent.pos[Y] += steps
        if(tar_agent.pos[Y] == dest_agent.pos[Y]):
            if(tar_agent.pos[X] == dest_agent.pos[X]):
                print("target at the destination")
            
    def move_from_agent(self, tar_agent, dest_agent, steps, grid_view=None):
        print("MFA Tar: ",tar_agent.pos[X], ",", tar_agent.pos[Y])
        print("MFA Dest: ",tar_agent.pos[X], ",", tar_agent.pos[Y])
        if(tar_agent.pos[X] > dest_agent.pos[X]):
            if self.is_cell_empty(tar_agent.pos[X] + steps,
                             tar_agent.pos[Y]):
                tar_agent.pos[X] += steps
        else:
            if self.is_cell_empty(tar_agent.pos[X] - steps,
                             tar_agent.pos[Y]):
                tar_agent.pos[X] -= steps
        if(tar_agent.pos[Y] < dest_agent.pos[Y]):
            if self.is_cell_empty(tar_agent.pos[X],
                             tar_agent.pos[Y] - steps):
                tar_agent.pos[Y] += steps
        else:
            if self.is_cell_empty(tar_agent.pos[X],
                             tar_agent.pos[Y] - steps):
                tar_agent.pos[Y] -= steps
    #=====================================================================================
        
    def find_empty(self, grid_view=None):
        """
        Return a random, empty cell.
        """
        if self.exists_empty_cells():
            if grid_view is None:
                return random.choice(self.empties)
            else:
                view_empties = grid_view.get_empties()
                if view_empties:
                    return random.choice(view_empties)
        return None

    def position_item(self, item, x=RANDOM, y=RANDOM, grid_view=None):
        """
        Position an agent on the grid.
        This is used when first placing agents! Use 'move_to_empty()'
        when you want agents to jump to an empty cell.
        If x or y are positive, they are used, but if RANDOM,
        we get a random position.
        Ensure this random position is not occupied (in Grid).
        """
        if x == RANDOM or y == RANDOM:
            cell = self.find_empty(grid_view)
            if cell is None:
                return None
        else:
            cell = self._get_cell(x, y)
        self._place_item(cell, item)
        return cell

    def _place_item(self, cell, item):
        """
        Place an agent in the grid.
        """
        cell.add_item(item)
        if cell in self.empties:
            self.empties.remove(cell)

    def _get_contents(self, x, y):
        """
        Extract contents from cell at x, y
        """
        return self._get_cell(x, y).contents

    def move(self, item, x, y):
        """
        Move item from its old cell to cell at x, y.
        """
        dest = self._get_cell(x, y)
        self._move_item(item, dest)

    def _move_item(self, item, dest):
        old_cell = item.cell
        if old_cell is not None:
            old_cell.remove_item(item)
            self._check_empty(old_cell)
        self._place_item(dest, item)

    def _check_empty(self, cell):
        if cell.is_empty():
            self.empties.append(cell)

    def _get_cell(self, x, y):
        return self.grid[y][x]

    def is_cell_empty(self, x, y):
        """
        Returns True if cell is empty, else False.
        A non-existent cell is NOT empty, i.e., not free
        to move to!
        """
        if self.out_of_bounds(x, y):
            return False
        else:
            return self._get_contents(x, y) is None
        
    def dist(self, agent1, agent2):
        """
        Arguments:
            Two grid agents.

        Returns:
            The Euclidian distance between the two
        agents. There isn't numerical ill-conditioning
        with this because the positions are integers. If 
        there are any applications where positions are given
        by nonintegral values, use caution.
        """
        return math.sqrt((agent1.pos[X]-agent2.pos[X])**2
                         + (agent1.pos[Y]-agent2.pos[Y])**2)

    def free_spot_near(self, agent):
        """
        Looks for an empty cell near agent. If the grid is full,
        returns None. 

        Argument:
            The agent whose nearest empty cell we look for.

        Returns:
            Either (a) the position of this empty cell or
            (b) null in which case the entire grid is full
            of agents.
        """

        max_poss_dist = max(self.width, self.height)
        for i in range(max_poss_dist):
            view = self.get_square_view(center=agent.pos, distance=i)
            for cell in view:
                if cell.is_empty():
                    return cell.coords

        return None
    
    def to_json(self):
        """
        We're going to make a dictionary of the 'safe' parts of the object to
        output to a json file. (We can't output the env, for instance, since
        IT contains a reference to each agent!)
        """
        safe_fields = super().to_json()
        safe_fields["torus"] = self.torus
        safe_fields["num_cells"] = self.num_cells
        
        return safe_fields
    
    def from_json(self, json_input):
        super().from_json(json_input)
        self.__init_unrestorables()
        self.torus = json_input["torus"]
        self.num_cells = json_input["num_cells"]
    
    def restore_agent(self, agent_json):            
        new_agent = ta.TestGridAgent(agent_json["name"], 
                                     agent_json["goal"],
                                     agent_json["max_move"], 
                                     agent_json["max_detect"])
        self.add_agent_to_grid(new_agent, agent_json)
        
    def add_agent_to_grid(self, agent, agent_json):
        x, y = agent_json["cell"]["coordx"], agent_json["cell"]["coordy"]
        agent.from_json_preadd(agent_json)
        self.add_agent(agent, x, y, True)
        agent.from_json_postadd(agent_json)
            
    def print_env(self):
        msg = ""
        for row in self.grid:
            for cell in row:
                msg += (str(cell.contents) + ", ")
            msg += "\n"
        logging.info(msg)

    def set_agent_color(self):
        logging.info("set_agent_color is not implemented")
