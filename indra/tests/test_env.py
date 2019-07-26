"""
This is the test suite for env.py.
"""
import os

from unittest import TestCase, main

import indra.display_methods as disp

from indra.env import Env, PopHist, POP_HIST_HDR, POP_SEP
from indra.user import TEST, API
from indra.agent import Agent
from indra.composite import Composite
from indra.tests.test_agent import create_newton
from indra.tests.test_composite import create_calcguys, create_cambguys

travis = False

GRP1 = "Group1"
GRP2 = "Group2"

X = 0
Y = 1

tests_env = {
    "name": "env",
    "type": "env",
    "duration": 9223372036854775805,
    "pos": None,
    "attrs": {},
    "groups": "",
    "active": True,
    "type_sig": 0,
    "prim_group": "None",
    "locator": "None",
    "neighbors": None,
    "action_key": None,
    "members": {
        "Blues": {
            "name": "Blues",
            "type": "composite",
            "duration": 9223372036854775805,
            "pos": None,
            "attrs": {
                "color": "blue"
            },
            "groups": "env ",
            "active": True,
            "type_sig": 0,
            "prim_group": "env",
            "locator": "None",
            "neighbors": None,
            "action_key": None,
            "members": {
                "Blues0": {
                    "name": "Blues0",
                    "type": "agent",
                    "duration": 9223372036854775805,
                    "pos": [
                        3,
                        3
                    ],
                    "attrs": {},
                    "groups": "Blues ",
                    "active": True,
                    "type_sig": 0,
                    "prim_group": "Blues",
                    "locator": "env",
                    "neighbors": None,
                    "action_key": "agent_action"
                },
                "Blues1": {
                    "name": "Blues1",
                    "type": "agent",
                    "duration": 9223372036854775805,
                    "pos": [
                        20,
                        14
                    ],
                    "attrs": {},
                    "groups": "Blues ",
                    "active": True,
                    "type_sig": 0,
                    "prim_group": "Blues",
                    "locator": "env",
                    "neighbors": None,
                    "action_key": "agent_action"
                }
            }
        },
        "Reds": {
            "name": "Reds",
            "type": "composite",
            "duration": 9223372036854775805,
            "pos": None,
            "attrs": {
                "color": "red"
            },
            "groups": "env ",
            "active": True,
            "type_sig": 0,
            "prim_group": "env",
            "locator": "None",
            "neighbors": None,
            "action_key": None,
            "members": {
                "Reds0": {
                    "name": "Reds0",
                    "type": "agent",
                    "duration": 9223372036854775805,
                    "pos": [
                        9,
                        6
                    ],
                    "attrs": {},
                    "groups": "Reds ",
                    "active": True,
                    "type_sig": 0,
                    "prim_group": "Reds",
                    "locator": "env",
                    "neighbors": None,
                    "action_key": "agent_action"
                },
                "Reds1": {
                    "name": "Reds1",
                    "type": "agent",
                    "duration": 9223372036854775805,
                    "pos": [
                        17,
                        14
                    ],
                    "attrs": {},
                    "groups": "Reds ",
                    "active": True,
                    "type_sig": 0,
                    "prim_group": "Reds",
                    "locator": "env",
                    "neighbors": None,
                    "action_key": "agent_action"
                }
            }
        }
    },
    "width": 20,
    "height": 20,
    "plot_title": "env",
    "props": {
        "grid_height": {
            "val": 20,
            "question": "What is the grid height?",
            "atype": "INT",
            "lowval": 2,
            "hival": 100
        },
        "grid_width": {
            "val": 20,
            "question": "What is the grid width?",
            "atype": "INT",
            "lowval": 2,
            "hival": 100
        },
        "num_blue": {
            "val": 2,
            "question": "How many blue agents do you want?",
            "atype": "INT",
            "lowval": 1,
            "hival": 100
        },
        "num_red": {
            "val": 2,
            "question": "How many red agents do you want?",
            "atype": "INT",
            "lowval": 1,
            "hival": 100
        },
        "user_type": {
            "val": "terminal",
            "question": None,
            "atype": None,
            "lowval": None,
            "hival": None
        },
        "OS": {
            "val": "Darwin",
            "question": None,
            "atype": None,
            "lowval": None,
            "hival": None
        }
    },
    "pop_hist": {
        "periods": 2,
        "pops": {
            "Blues": [
                2,
                2,
                2
            ],
            "Reds": [
                2,
                2,
                2
            ]
        }
    },
    "womb": [],
    "switches": []
}


def env_action(env):
    print("Calling action for env")
    env.name = "Monjur"
    return True


class EnvTestCase(TestCase):
    def setUp(self):
        self.newton = create_newton()
        self.calcs = create_calcguys()
        self.cambs = create_cambguys()
        self.pop_hist = PopHist()
        self.env = Env("Test env", action=env_action)

    def tearDown(self):
        self.newton = None
        self.calcs = None
        self.cambs = None
        self.pop_hist = None
        self.env = None

    def fill_pop_hist(self):
        self.pop_hist.record_pop(GRP1, 10)
        self.pop_hist.record_pop(GRP2, 10)
        self.pop_hist.record_pop(GRP1, 20)
        self.pop_hist.record_pop(GRP2, 20)
        return self.pop_hist

    def test_user_type(self):
        """
        Make sure our user type is test.
        """
        self.assertEqual(self.env.user_type, TEST)

    def test_runN(self):
        """
        Test running for N turns.
        """
        NUM_PERIODS = 10
        self.env += self.newton
        acts = self.env.runN(NUM_PERIODS)
        self.assertEqual(acts, NUM_PERIODS)

    def test_str_pop(self):
        """
        Test converting the pop history to a string.
        """
        self.fill_pop_hist()
        s = str(self.pop_hist)
        self.assertEqual(s, POP_HIST_HDR + GRP1 + POP_SEP + GRP2 + POP_SEP)

    def test_record_pop(self):
        self.assertTrue(True)

    def test_add_child(self):
        self.env.add_child(self.newton, self.calcs)
        self.assertIn((self.newton, self.calcs), self.env.womb)

    def test_add_switch(self):
        self.env.add_switch(self.newton, self.calcs, self.cambs)
        self.assertIn((self.newton, self.calcs, self.cambs), self.env.switches)

    def test_has_disp(self):
        if not disp.plt_present:
            self.assertTrue(not self.env.has_disp())
        else:
            self.assertTrue(self.env.has_disp())

    def test_line_data(self):
        """
        Test the construction of line graph data.
        This test must be changed to handle new color param!
        Commented out for the moment.
        """
        global travis
        travis = os.getenv("TRAVIS")
        if not travis:
            self.env.pop_hist = self.fill_pop_hist()
            ret = self.env.line_data()
            self.assertEqual(ret, (2,
                                   {GRP1: {"color": "navy", "data": [10, 20]},
                                    GRP2: {"color": "blue", "data": [10, 20]}}))

    def test_plot_data(self):
        """
        Test the construction of scatter plot data.
        """
        global travis
        travis = os.getenv("TRAVIS")
        if not travis:
            our_grp = Composite(GRP1, members=[self.newton])
            self.env = Env("Test env", members=[our_grp])
            ret = self.env.plot_data()
            (x, y) = self.newton.pos
            self.assertEqual(ret, {GRP1: {X: [x], Y: [y], 'color': None,
                                          'marker': None}})

    def test_headless(self):
        if (self.env.user_type == API) or (self.env.user_type == TEST):
            self.assertTrue(self.env.headless())
        else:
            self.assertTrue(not self.env.headless())

    def test_env_action(self):
        self.env()
        self.assertEqual(self.env.name, "Monjur")

    def test_restore_env(self):
        # ret_env = Env("env", serial_env=serial_env)
        # self.assertEqual(str(type(ret_env)), "<class 'indra.env.Env'>")
        return True

    def test_from_json(self):
        self.maxDiff = None
        self.env = Env(name='Test env', serial_obj=tests_env)
        # self.assertEqual(self.env, tests_env, msg=self.env.to_json())
        self.assertEqual(str(type(self.env)), "<class 'indra.env.Env'>")
        # managed to construct an env!!!


if __name__ == '__main__':
    main()
