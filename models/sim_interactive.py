import indra.grid_env as grid
import indra.vs_agent as va

"""
Created on Mon Sep 10 17:30:05 2018
@authors: wenxuan ruan
    yadong Li
"""

X = 0
Y = 1


class Route:

    def __init__(self, name):
        self.intersections = []
        self.count = 0
        self.name = name
        self.heavy_p = 100
        self.light_p = 100
        return

    def travelRoute(self):
        self.count = self.count + 1
        for intersection in self.intersections:
            intersection.travelIntersection()
        return

    def getCount(self):
        return self.count


class RouteNetwork:

    routes = []

    def __init__(self):
        self.routes = []
        return

    def add(self, name):
        newRoute = Route(name)
        self.routes.append(newRoute)


class Car(va.VSAgent):

    def __init__(self, name, speed, direction):
        super().__init__(name, '')
        self.name = name
        self.speed = speed
        self.lane = "SLOW"
        self.direction = direction

    def travel(self):
        print(self.speed)
        x = self.pos[X]
        y = self.pos[Y]
        # If there is a car ahead
        if self.env.is_cell_empty(x + self.speed, y):
            self.env.move(self, x + self.speed, y)
        else:
            self.env.move(self, x + self.speed - 1, y)

    def to_json(self):
        safe_fields = super().to_json()
        safe_fields["lane"] = self.lane
        safe_fields["speed"] = self.speed
        return safe_fields


class EastCar(Car):

    def __init__(self, name, speed):
        super().__init__(name, speed, 'E')

    def eval_env(self, other_pre):
        x = self.pos[X]
        y = self.pos[Y]

        # If there is a car ahead
        newXPos = x + self.speed
        # Make cars loop around when reach the border
        while self.env.out_of_bounds(newXPos, y):
            newXPos -= self.env.width
        if self.lane == "SLOW":
            if self.env.is_cell_empty(newXPos, y):
                self.env.move(self, newXPos, y)
            else:
                # Switch lane if there is a car ahead to pass the car ahead
                self.env.move(self, newXPos, y + 5)
                self.lane = "FAST"
                print(self.name + " Passing")
        elif self.lane == "FAST":
            # Try to merge back if there is enough space
            if self.env.is_cell_empty(newXPos, y - 5):
                self.env.move(self, newXPos, y - 5)
                self.lane = "SLOW"
                print(self.name + " Merged back")
            else:
                # Keep moving in the fast lane
                if self.env.is_cell_empty(newXPos, y):
                    self.env.move(self, newXPos, y)
                else:
                    while self.env.is_cell_empty(newXPos, y):
                        newXPos -= 1
                        if newXPos == 0:
                            break

                    try:
                        self.env.move(self, newXPos, y)
                    except Exception:
                        print(self.name + ' stopped')
                        pass


class SouthCar(Car):

    def __init__(self, name, speed):
        super().__init__(name, speed, 'S')

    def eval_env(self, other_pre):
        x = self.pos[X]
        y = self.pos[Y]

        newYPos = y - self.speed
        while self.env.out_of_bounds(x, newYPos):
            newYPos += self.env.height

        if self.lane == "SLOW":
            if self.env.is_cell_empty(x, newYPos):
                self.env.move(self, x, newYPos)
            else:
                # Switch lane if there is a car ahead to pass the car ahead
                self.env.move(self, x + 5, newYPos)
                self.lane = "FAST"
                print(self.name + " Passing")
        elif self.lane == "FAST":
            # Try to merge back if there is enough space
            if self.env.is_cell_empty(x - 5, newYPos):
                self.env.move(self, x - 5, newYPos)
                self.lane = "SLOW"
                print(self.name + " Merged back")
            else:
                # Keep moving in the fast lane
                if self.env.is_cell_empty(x, newYPos):
                    self.env.move(self, x, newYPos)
                else:
                    while self.env.is_cell_empty(x, newYPos):
                        newYPos += 1
                        if newYPos == self.env.height:
                            break

                    try:
                        self.env.move(self, x, newYPos)
                    except Exception:
                        print(self.name + ' stopped')
                        pass


class Intersection:

    def __init__(self, name):
        self.neighbours = []
        self.name = name
        self.trafficCount = 0

    def travelIntersection(self):
        self.trafficCount += 1

    def getTrafficCount(self):
        return self.trafficCount

    def addNeighbour(self, newNeighbour):
        self.neighbours.append(newNeighbour)


class SimInteractiveEnv(grid.GridEnv):
    def __init__(self, name, width, height, model_nm=None, props=None):
        super().__init__(name, width, height, torus=False,
                         model_nm=model_nm, props=props)
        self.plot_title = name
        self.num_moves = 0
        self.move_hist = []
        self.menu.view.del_menu_item("v")  # no line graph in this model
        self.intersectionArr = []

    def set_agent_color(self):
        self.set_var_color('EastCar', 'b')
        self.set_var_color('SouthCar', 'r')

    def car_move(self, agent):
        agent.travel()

    def addRelation(self, intersection1, intersection2):
        intersection1.addNeighbour(intersection2)

    def addTwoWayRelation(self, inter1, inter2):
        intersection1 = self.get(inter1)
        intersection2 = self.get(inter2)
        self.addRelation(intersection1, intersection2)
        self.addRelation(intersection2, intersection1)

    def addOneWayRelation(self, inter1, inter2):
        intersection1 = self.get(inter1)
        intersection2 = self.get(inter2)
        self.addRelation(intersection1, intersection2)

    def getIntersection(self, interName):
        if len(self.intersectionArr) == 0:
            self.intersectionArr.append(Intersection(interName))
            return self.intersectionArr[0]

        for intersection in self.intersectionArr:
            if intersection.name == interName:
                return intersection

        self.intersectionArr.append(Intersection(interName))
        return self.intersectionArr[0]
