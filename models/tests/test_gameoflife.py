from unittest import TestCase, main
from indra.agent import Agent
from indra.composite import Composite
from indra.space import Space
from indra.env import Env
from models.gameoflife import create_agent, set_up
from models.gameoflife import change_color, apply_live_rules, apply_dead_rules, gameoflife_action, agent_action, populate_board
import models.gameoflife as g

TEST_X = 1
TEST_Y = 1

gameoflife_env = None

class GameOfLifeTestCase(TestCase):
    def setUp(self):
        (g.gameoflife_env, g.groups) = set_up()
        pass

    def tearDown(self):
        g.gameoflife_env = None
        g.groups = None
        pass

    def test_create_agent(self):
        agent = create_agent(TEST_X, TEST_Y)
        test_name = "(" + str(TEST_X) + "," + str(TEST_Y) + ")"
        self.assertEqual(agent.name, test_name)

    def test_change_color(self):
        agent = create_agent(TEST_X, TEST_Y)
        g.groups =[]
        g.groups.append(Composite("white"))
        g.groups.append(Composite("black"))
        g.groups[0] += agent
        change_color(g.gameoflife_env, agent)
        self.assertEqual(agent.primary_group(), g.groups[1])

    def test_apply_live_rules(self):
        a = create_agent(TEST_X, TEST_Y)
        b = create_agent(TEST_X - 1, TEST_Y)
        c = create_agent(TEST_X + 1, TEST_Y)
        g.groups =[]
        g.groups.append(Composite("white"))
        g.groups.append(Composite("black"))
        g.groups[1] += a
        g.groups[1] += b
        g.groups[1] += c
        neighbors = Composite("agent_neighbors")
        neighbors += b
        a.neighbors = neighbors
        self.assertEqual(apply_live_rules(g.gameoflife_env, a), True)
        neighbors += c
        a.neighbors = neighbors
        self.assertEqual(apply_live_rules(g.gameoflife_env, a), False)

    def test_apply_dead_rules(self):
        a = create_agent(TEST_X, TEST_Y)
        b = create_agent(TEST_X - 1, TEST_Y)
        c = create_agent(TEST_X + 1, TEST_Y)
        d = create_agent(TEST_X, TEST_Y + 1)
        g.groups =[]
        g.groups.append(Composite("white"))
        g.groups.append(Composite("black"))
        g.groups[0] += a
        g.groups[1] += b
        g.groups[1] += c
        g.groups[1] += d
        neighbors = Composite("agent_neighbors")
        neighbors += b
        neighbors += c
        a.neighbors = neighbors
        self.assertEqual(apply_dead_rules(g.gameoflife_env, a), False)
        neighbors += d
        a.neighbors = neighbors
        self.assertEqual(apply_dead_rules(g.gameoflife_env, a), True)

    # def test_gameoflife_action(self):
    #     a = create_agent(TEST_ANUM, TEST_ANUM)
    #     b = create_agent(TEST_ANUM - 1, TEST_ANUM)
    #     c = create_agent(TEST_ANUM + 1, TEST_ANUM)
    #     d = create_agent(TEST_ANUM, TEST_ANUM + 1)
    #     g.groups = []
    #     g.groups.append(Composite("white"))
    #     g.groups.append(Composite("black"))
    #     g.groups[0] += a
    #     g.groups[1] += b
    #     g.groups[1] += c
    #     g.groups[1] += d
    #     lst = []
    #     neighbors_dict = {"neighbors": lst}
    #     neighbors_dict["neighbors"].append(b)
    #     neighbors_dict["neighbors"].append(c)
    #     neighbors_dict["neighbors"].append(d)
    #     neighbors_composite = grp_from_nm_dict("All neighbors", neighbors_dict["neighbors"])
    #     a.neighbors = neighbors_composite
    #     gameoflife_action(g.gameoflife_env)
    #     self.assertEqual(a.primary_group(), g.groups[1])
    #     self.assertEqual(len(a.neighbors), 3)

    # def test_agent_action(self):
    #     a = create_agent(TEST_ANUM, TEST_ANUM)
    #     b = create_agent(TEST_ANUM - 1, TEST_ANUM)
    #     c = create_agent(TEST_ANUM + 1, TEST_ANUM)
    #     d = create_agent(TEST_ANUM, TEST_ANUM + 1)
    #     g.groups = []
    #     g.groups.append(Composite("Group" + str(0)))
    #     g.groups += a
    #     g.groups += b
    #     g.groups += c
    #     g.groups += d
    #     neighbors = Composite("neighbors")
    #     neighbors += b
    #     neighbors += c
    #     neighbors += d
    #     g.gameoflife_env = Env("gameoflife", members = g.groups)
    #     agent_action(a)
    #     for i in a.neighbors:
    #     assertEqual(a.neighbors, neighbors)









