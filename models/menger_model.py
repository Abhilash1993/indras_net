"""
menger_model.py
The aim of this model is to get money to arise
in a barter economy.
"""
import logging
import random
import edgebox_model as ebm
import barter_model as bm


class MengerAgent(bm.BarterAgent):
    """
    Agents who get continually endowed with goods (produce)
    and whom we hope will start to use money to trade them.
    """

    def __init__(self, name, goal=bm.TRADE,
                 max_detect=ebm.GLOBAL_KNOWLEDGE):
        super().__init__(name, goal=goal, max_detect=max_detect)
        self.prod_good = None
        self.prod_amt = 1

    def act(self):
        """
        Trade, but first, produce our good.
        """
        if self.prod_good is not None:
            print("Endowing da agent "
                  + self.name + " wid some " + self.prod_good)
            self.endow(self.prod_good, self.prod_amt)
        super().act()

    def trade(self, my_good, counterparty, his_good):
        """
        We are going to trade goods through
        our super(), but also up the utility
        of the good accepted in trade since it
        is exchangeable
        """
        super().trade(my_good, counterparty, his_good)


class MengerEnv(bm.BarterEnv):
    """
    An env to host money-using agents.
    """

    def __init__(self, name, length, height, model_nm=None):
        super().__init__("Menger environment",
                         length, height,
                         model_nm=model_nm,
                         preact=True)

    def add_prod_goods(self):
        """
        Add who produces which good, and
        make them a vendor of that good in the market.
        """
        print("In add_prod_goods")
        my_good = None
        for agent in self.agents:
            print("Adding prod goods to agents")
            for good in self.market.goods_iter():
                if not self.market.has_vendor(good):
                    my_good = good
                    break

            if my_good is None:
                my_good = random.choice(list(self.market.goods_iter()))

            agent.prod_good = my_good
            self.market.add_vendor(my_good, agent)

        print("Market = " + str(self.market))
