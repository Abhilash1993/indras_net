"""
A edgeworthbox model.
Places two groups of agents in the enviornment randomly
and moves them around randomly.
"""

from indra.agent import Agent
from indra.composite import Composite
from indra.env import Env
from indra.registry import get_env, get_prop
from indra.space import DEF_HEIGHT, DEF_WIDTH
from indra.utils import init_props
from capital.trade_utils import seek_a_trade, GEN_UTIL_FUNC
from capital.trade_utils import AMT_AVAILABLE, endow, UTIL_FUNC

MODEL_NAME = "money"
DEBUG = True  # turns debugging code on or off
DEBUG2 = False  # turns deeper debugging code on or off

DEF_NUM_TRADERS = 2


# these are the goods we hand out at the start:
natures_goods = {
    "cow": {AMT_AVAILABLE: 10, UTIL_FUNC: GEN_UTIL_FUNC,
            "incr": 0, "durability": 0.9, "divisibility": 1.0, },
    "gold": {AMT_AVAILABLE: 8, UTIL_FUNC: GEN_UTIL_FUNC,
             "incr": 0, "durability": 1.0, "divisibility": 0.1, },
    "cheese": {AMT_AVAILABLE: 2, UTIL_FUNC: GEN_UTIL_FUNC,
               "incr": 0, "durability": 0.8, "divisibility": 0.3, },
    "banana": {AMT_AVAILABLE: 7, UTIL_FUNC: GEN_UTIL_FUNC,
               "incr": 0, "durability": 0.2, "divisibility": 0.9, },
    "diamond": {AMT_AVAILABLE: 8, UTIL_FUNC: GEN_UTIL_FUNC,
                "incr": 0, "durability": 1.0, "divisibility": 0.2, },
}


def good_decay(goods):
    """
    This must be re-written to change the amount of a good
    available based on its durability, not change its durability.
    """
    for good in goods:
        goods[good]["durability"] *= goods[good]["durability"]
        # if the good the durability is too low, the good can't to be traded
        if goods[good]["durability"] < 0.001:
            goods[good][AMT_AVAILABLE] = 0


def trader_action(agent):
    ret = seek_a_trade(agent)
    good_decay(agent["goods"])
    return ret


def create_trader(name, i):
    """
    A func to create a trader.
    """
    return Agent(name + str(i), action=trader_action,
                 attrs={"goods": {},
                        "util": 0,
                        "pre_trade_util": 0})


def nature_to_traders(traders, nature):
    """
    A func to do the initial endowment from nature to all traders
    """
    for trader in traders:
        endow(traders[trader], nature)
        for good in nature:
            if good not in traders[trader]["goods"]:
                traders[trader]["goods"][good] = nature[good].copy()
                traders[trader]["goods"][good][AMT_AVAILABLE] = 0
            else:
                # put attributes other than AMT_AVAILABLE into trader dict
                temp_amt = traders[trader]["goods"][good][AMT_AVAILABLE]
                traders[trader]["goods"][good] = nature[good].copy()
                traders[trader]["goods"][good][AMT_AVAILABLE] = temp_amt
    # each trader is given goods and knows all goods in nature
        print(repr(traders[trader]))


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    # global max_util -> not in use now
    init_props(MODEL_NAME, props, model_dir="capital")
    traders = Composite("Traders",
                        member_creator=create_trader,
                        num_members=get_prop('num_traders',
                                             DEF_NUM_TRADERS))

    nature_to_traders(traders, natures_goods)

    Env("MengerMoney",
        height=get_prop('grid_height', DEF_HEIGHT),
        width=get_prop('grid_width', DEF_WIDTH),
        members=[traders],
        attrs={"goods": natures_goods})


def main():
    set_up()
    # `get_env()` returns an env, which itself is a callable object
    get_env()()
    return 0


if __name__ == "__main__":
    main()
