"""
This is the test suite for space.py.
"""

from unittest import TestCase, main

from propargs.propargs import PropArgs

import models.coop as coop
from models.coop import act, DEF_COUPON
from models.coop import babysitter_action
from models.coop import set_up, create_babysitter, create_central_bank

TEST_BABYSITTER_NUM = 3
TEST_CENTRAL_BANK_NUM = 3


class coopTestCase(TestCase):
    def setUp(self):
        self.pa = PropArgs.create_props('coop_props',
                                        ds_file='props/coop.props.json')
        (coop.coop_members, central_bank) = set_up()

    def tearDown(self):
        coop.groups = None
        coop.group_indices = None

    def test_create_babysitter(self):
        """
         Test to see if babysitter is created
        """
        new_babysitter = create_babysitter("babysitters", 0, self.pa)
        self.assertTrue(new_babysitter["desired_cash"] >= 0)
        self.assertTrue(new_babysitter["goal"] is None)
        self.assertTrue(new_babysitter["coupons"] > 0)

    def test_create_central_bank(self):
        """
        Test to see if central bank is created
        """
        new_central_bank = create_central_bank("central_bank", 0, self.pa)
        self.assertTrue(new_central_bank["percent_change"] >= 0)
        self.assertTrue(new_central_bank["extra_coupons"] >= 0)
        self.assertTrue(new_central_bank["extra_dev"] >= 0)

    def test_exchange(self):
        pass

    def test_act(self):
        new_babysitter0 = create_babysitter("babysitters", 0, self.pa)
        new_babysitter0["goal"] = None
        new_babysitter0["coupons"] = DEF_COUPON - 1
        new_babysitter0["desired_cash"] = DEF_COUPON
        act(new_babysitter0)
        self.assertEqual(new_babysitter0["goal"], "BABYSITTING")
        # self.assertTrue(new_babysitter0["sitting"])

    def test_coup_action(self):
        pass

    def test_babysitter_action(self):
        """
        Test the babysitter action
        """
        new_babysitter0 = create_babysitter("babysitters", 0, self.pa)
        new_babysitter0["coupons"] = 0
        babysitter_action(new_babysitter0)
        # self.assertTrue(new_babysitter0["sitting"] == True)
        # self.assertTrue(new_babysitter0["going_out"] == False)

    def test_central_bank_action(self):
        """
        Test the central bank action
        """
        pass

    if __name__ == '__main__':
        main()
