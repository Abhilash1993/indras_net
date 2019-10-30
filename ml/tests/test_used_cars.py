"""
This is the test suite for flocking.py.
"""

from unittest import TestCase, main
from propargs.propargs import PropArgs
from indra.env import Env
from ml.used_cars import *
from ml.used_cars import MIN_GOOD_CAR_LIFE, MAX_CAR_LIFE
from ml.used_cars import MIN_CAR_LIFE, MAX_BAD_CAR_LIFE

TEST_RAND_AMT = 20


class usedCarTestCase(TestCase):
    def setUp(self):
        self.pa = PropArgs.create_props('used_car_props',
                                        ds_file='props/used_cars.props.json')
        (self.car_market,  self.buyers, self.dealers) = set_up()

    def tearDown(self):
        (self.car_market,  self.buyers, self.dealers) = (None, None, None)

    def test_get_dealer_car(self):
        result = get_dealer_car("good")
        self.assertTrue(result >= MIN_GOOD_CAR_LIFE)
        self.assertTrue(result <= MAX_CAR_LIFE)
        result = get_dealer_car("bad")
        self.assertTrue(result >= MIN_CAR_LIFE)
        self.assertTrue(result <= MAX_BAD_CAR_LIFE)
    def test_create_buyer(self):
        buyer = create_buyer("Buyer", 0, None)
        self.assertTrue(buyer["has_car"]is False)
        self.assertTrue(buyer["car_life"] is None)
        self.assertTrue(buyer["interaction_res"] is None)
        self.assertTrue(buyer["dealer_his"] ==  [])
        self.assertTrue(buyer["emoji_carlife_assoc"] == {})
        self.assertTrue(buyer["emoji_life_avg"] == {})  
        self.assertTrue(buyer["emoji_indicator"] == {})
    
     
  


    if __name__ == '__main__':
        main()
