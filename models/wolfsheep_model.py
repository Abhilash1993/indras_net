"""
wolfsheep_model.py
Wolves and sheep roaming a meadow, with wolves eating sheep
that get near them.
"""
import indra.grid_env as ge
import indra.grid_agent as ga

WOLF_REPRO = 10
WOLF_LFORCE = 9

SHEEP_REPRO = 3
SHEEP_LFORCE = 5


class Creature(ga.GridAgent):
    """
    A creature: moves around randomly.
    Reproduction to be added.
    """
    def __init__(self, name, goal, repro_age, life_force):
        super().__init__(name, goal)
        self.age = 0
        self.alive = True
        self.repro_age = repro_age
        self.life_force = life_force

    def died(self):
        if self.alive:
            self.alive = False
            self.env.died(self)

    def act(self):
        self.age += 1
        self.life_force -= 1
        if self.life_force <= 0:
            self.died()
        if self.age % self.repro_age == 0:
            self.reproduce()

    def preact(self):
        self.env.move_to_empty(self)

    def reproduce(self):
        if self.alive:
            creature = self.__class__(self.name + "x", self.goal)
            self.env.add_agent(creature)


class Wolf(Creature):
    """
    A wolf: moves around randomly and eats any sheep
    nearby.
    """
    def __init__(self, name, goal):
        super().__init__(name, goal, WOLF_REPRO, WOLF_LFORCE)

    def act(self):
        super().act()
        if self.alive:
            for sheep in filter(lambda a: isinstance(a, Sheep),
                                self.neighbor_iter()):
                if sheep.alive:
                    self.eat(sheep)
                    break  # don't be greedy! eat one sheep per turn!

    def eat(self, sheep):
        self.env.user.tell("%s eating sheep: %s" % (self.name, sheep.name))
        self.life_force += sheep.life_force
        sheep.died()


class Sheep(Creature):
    """
    A sheep: moves around randomly and sometimes gets eaten.
    """
    def __init__(self, name, goal):
        super().__init__(name, goal, SHEEP_REPRO, SHEEP_LFORCE)


class Meadow(ge.GridEnv):
    """
    A meadow in which wolf eat sheep.
    """

    def died(self, prey):
        self.remove_agent(prey)
