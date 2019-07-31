"""
This is the test suite for space.py.
"""

from propargs.propargs import PropArgs
from unittest import TestCase, main
from indra.env import Env
from indra.composite import Composite
from models.fmarket import set_up, create_market_maker, create_trend_follower
from models.fmarket import create_value_investor, DEF_PRICE, trend_direction
from models.fmarket import trend_follower_action, DEF_REAL_VALUE, DEF_PERIODS, value_investor_action, DEF_MIN_PRICE_MOVE, DEF_MAX_PRICE_MOVE
from models.fmarket import market_maker_action, calc_price_change, buy, sell
from models.fmarket import DEF_NUM_ASSET, market_report, DEF_DISCOUNT, DEF_SIGMA, gaussian_distribution
import models.fmarket as fm
import random

TEST_INVESTOR_NUM = 3
TEST_FOLLOWER_NUM = 3

class FMarketTestCase(TestCase):
    def setUp(self):
        self.pa = PropArgs.create_props('fmarket_props',
                                        ds_file='props/fmarket.props.json')
        (fm.market,fm.value_investors, fm.trend_followers, fm.market_maker) = set_up()
        self.value_investor = create_value_investor("value_investors",
                                                    TEST_INVESTOR_NUM,
                                                    self.pa.get("discount",
                                                                DEF_DISCOUNT),
                                                    self.pa.get("deviation_investor",
                                                                DEF_SIGMA))
        self.trend_follower = create_trend_follower("trend_followers",
                                                    TEST_FOLLOWER_NUM,
                                                    self.pa.get("average_period",
                                                                DEF_PERIODS),
                                                    self.pa.get("deviation_follower",
                                                                DEF_SIGMA))
        self.market_maker = create_market_maker("market_maker")

    def tearDown(self):
        self.test_value_investors = None
        self.test_trend_followers = None
        self.test_market_maker = None

    def test_create_trend_follower(self):
        """
         Test to see if trend_follower is created
        """
        new_trend_follower = create_trend_follower("trend_followers", 0,
                                                   DEF_PERIODS, DEF_SIGMA)
        self.assertTrue(new_trend_follower["capital"] >= 0)
        self.assertTrue(new_trend_follower["num_stock"] == 0)

    def test_create_value_investor(self):
        """
         Test to see if value_investor is created
        """
        new_value_investor = create_value_investor("value_investors", 0,
                                                   DEF_DISCOUNT, DEF_SIGMA)
        self.assertTrue(new_value_investor["capital"] >= 0)
        self.assertTrue(new_value_investor["num_stock"] == 0)

    def test_create_market_maker(self):
        """
        Test to see if market_maker is created
        """
        new_market_maker = create_market_maker("market_maker")
        self.assertTrue(new_market_maker["buy"] == 0)
        self.assertTrue(new_market_maker["sell"] == 0)
        self.assertTrue(new_market_maker["asset_price"] == DEF_PRICE)
        self.assertTrue(new_market_maker["prev_asset_price"] == DEF_PRICE)
        self.assertTrue(new_market_maker["price_hist"] == [DEF_PRICE])

    def test_buy(self):
        '''
        Test the buy action of the investors
        '''
        new_market_maker = create_market_maker("market_maker")
        new_value_investor = create_value_investor("value_investors", 0, DEF_DISCOUNT, DEF_SIGMA)
        new_market_maker["asset_price"] = DEF_PRICE
        new_value_investor["capital"] = DEF_PRICE * DEF_NUM_ASSET + 1
        price = new_market_maker["asset_price"] * DEF_NUM_ASSET
        buy(new_value_investor)
        self.assertTrue(new_value_investor["capital"] == 1)

    def test_sell(self):
        '''
        Test the sell action of the investors
        '''
        new_market_maker = create_market_maker("market_maker")
        new_value_investor = create_value_investor("value_investors", 0,
                                                   DEF_DISCOUNT, DEF_SIGMA)
        new_market_maker["asset_price"] = DEF_PRICE
        new_value_investor["capital"] = 0
        new_value_investor["num_stock"] = DEF_NUM_ASSET + 1
        price = new_market_maker["asset_price"] * DEF_NUM_ASSET
        sell(new_value_investor)
        self.assertTrue(new_value_investor["capital"] == price)


    def test_calc_price_change(self):
        '''
        Test if the function calculate the price change correctly.
        '''
        new_market_maker = create_market_maker("market_maker")
        new_market_maker["sell"] = 2
        new_market_maker["buy"]  = 4
        ratio = new_market_maker["buy"] / new_market_maker["sell"]
        self.assertTrue(calc_price_change(ratio) > 0)

    def test_market_report(self):
        self.pa = PropArgs.create_props('fmarket_props',
                                        ds_file='props/fmarket.props.json')
        new_market_maker = create_market_maker("market_maker")
        value_investors = Composite("value_investors")
        trend_followers = Composite("trend_followers")
        market = Env("env",                  
                     members=[value_investors, trend_followers, new_market_maker],
                     props=self.pa,
                     census=market_report)
        self.assertEqual(market_report(market), "Asset price on the market: " \
        + str(DEF_PRICE) + "\n")

    def test_gaussian_distribution(self):
        '''
        Test the Gaussian distribution
        '''
        new_target = gaussian_distribution(DEF_PERIODS, DEF_SIGMA)
        self.assertTrue(new_target >= 0)

    def test_trend_follower_action(self):
        '''
        Test the trend follower action
        '''
        new_market_maker = create_market_maker("market_maker")
        new_market_maker["price_hist"] = [DEF_PRICE]
        new_market_maker["asset_price"] = DEF_PRICE
        new_trend_follower = create_trend_follower("trend_follower", 0,
                                                   DEF_PERIODS, DEF_SIGMA)
        trend_follower_action(new_trend_follower)
        trend = trend_direction(new_trend_follower, new_market_maker["asset_price"],
                                new_market_maker["price_hist"])
        self.assertEqual(trend, 0)

    def test_market_maker_action(self):
        '''
        Test the market maker action
        '''
        new_market_maker = create_market_maker("market_maker")
        new_market_maker["sell"] = 2
        new_market_maker["buy"]  = 4
        ratio = new_market_maker["buy"] / new_market_maker["sell"]
        new_market_maker["asset_price"] = DEF_REAL_VALUE
        market_maker_action(new_market_maker)
        price_change = calc_price_change(ratio)
        self.assertTrue(new_market_maker["asset_price"] == DEF_REAL_VALUE + price_change)

    def test_trend_direction(self):
        '''
        Test the trend direction of the market
        '''
        new_market_maker = create_market_maker("market_maker")
        new_trend_follower = create_trend_follower("trend_follower", 0,
                                                   DEF_PERIODS, DEF_SIGMA)
        new_trend_follower["change_period"] = DEF_PERIODS
        new_market_maker["asset_price"] = DEF_REAL_VALUE
        new_market_maker["price_hist"] = [DEF_REAL_VALUE]
        self.assertEqual(trend_direction(new_trend_follower, new_market_maker["asset_price"],
                                         new_market_maker["price_hist"]), 0)


    if __name__ == '__main__':
        main()
