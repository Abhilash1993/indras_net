"""
This file contains general functions useful in trading goods.
"""
from indra.user import user_debug
from indra.registry import get_env
import random

ACCEPT = 1
INADEQ = 0
REJECT = -1

AMT_AVAILABLE = "amt_available"
GOODS = "goods"

answer_dict = {
    1: "I accept",
    0: "I'm indifferent about",
    -1: "I reject"
}

DEF_MAX_UTIL = 20  # this should be set by the models that use this module

max_util = DEF_MAX_UTIL


"""
    We expect goods dictionaries to look like:
        goods = {
            "houses": { AMT_AVAILABLE: int, "maybe more fields": vals ... },
            "trucks": { AMT_AVAILABLE: int, "maybe more fields": vals ... },
            "etc.": { AMT_AVAILABLE: int, "maybe more fields": vals ... },
        }
    A trader is an object that can be indexed to yield a goods dictionary.
"""


def is_depleted(goods_dict):
    """
    See if `goods_dict` has any non-zero amount of goods in it.
    """
    for good in goods_dict:
        if goods_dict[good][AMT_AVAILABLE] > 0:
            return False
    # if all goods are 0 (or less) dict is empty:
    return True


def transfer(to_goods, from_goods, good_nm, amt=None):
    """
    Transfer goods between two goods dicts.
    Use `amt` if it is not None.
    """
    if good_nm not in to_goods:
        to_goods[good_nm] = {AMT_AVAILABLE: 0}
    to_goods[good_nm][AMT_AVAILABLE] = (
        from_goods[good_nm][AMT_AVAILABLE])
    from_goods[good_nm][AMT_AVAILABLE] = 0


def get_rand_good(goods_dict):
    """
    What should this do with empty dict?
    """
    if goods_dict is None or not len(goods_dict):
        return None
    else:
        return random.choice(list(goods_dict.keys()))


def endow(trader, avail_goods):
    """
    This function is going to pick a good at random, and give the
    trader all of it, by default. We will write partial distributions
    later.
    """
    if is_depleted(avail_goods):
        # we can't allocate what we don't have!
        return

    # pick an item at random
    # stick all of it in trader's goods dictionary
    rand_good = get_rand_good(avail_goods)

    # pick again if the goods is endowed (amt is 0)
    # if we get big goods dicts, this could be slow:
    while avail_goods[rand_good][AMT_AVAILABLE] == 0:
        rand_good = get_rand_good(avail_goods)

    # get a random good
    transfer(trader[GOODS], avail_goods, rand_good)


def goods_to_str(goods):
    """
    take a goods dict to string
    """
    string = ', '.join([str(goods[k][AMT_AVAILABLE]) + " " + str(k)
                       for k in goods.keys()])
    return string


def answer_to_str(ans):
    """
    convert integer value of ans to string
    """
    return answer_dict[ans]


def gen_util_func(qty):
    return max_util - qty


def seek_a_trade(agent):
    nearby_agent = get_env().get_closest_agent(agent)
    if nearby_agent is not None:
        user_debug("I'm " + agent.name + " and I find "
                   + nearby_agent.name)
        # this_good is a dict
        # better to just give each agent at least 0
        # of every good to start
        for this_good in agent["goods"]:
            amt = 1
            while agent["goods"][this_good][AMT_AVAILABLE] >= amt:
                ans = rec_offer(nearby_agent, this_good, amt, agent)
                user_debug("I'm " + agent.name
                           + ", " + answer_to_str(ans) + " this offer")
                if ans == ACCEPT or ans == REJECT:
                    break
                amt += 1

    user_debug("I'm " + agent.name
               + ". I have " + goods_to_str(agent["goods"]))

    # return False means to move
    return False


def rec_offer(agent, his_good, his_amt, counterparty):
    """
    Receive an offer: we don't need to ever change my_amt
    in this function, because if the counter-party can't bid enough
    for a single unit, no trade is possible.
    """
    my_amt = 1
    gain = utility_delta(agent, his_good, his_amt)
    for my_good in agent["goods"]:
        if my_good != his_good and agent["goods"][my_good][AMT_AVAILABLE] > 0:
            loss = -utility_delta(agent, my_good, -my_amt)
            # user_tell("my good: " + my_good + "; his good: " + his_good
            #           + ", I gain: " + str(gain) +
            #           " and lose: " + str(loss))
            if gain > loss:
                if rec_reply(counterparty, his_good, his_amt, my_good, my_amt):
                    trade(agent, my_good, my_amt,
                          counterparty, his_good, his_amt)
                    return ACCEPT
                else:
                    return INADEQ
    return REJECT


def rec_reply(agent, my_good, my_amt, his_good, his_amt):
    gain = utility_delta(agent, his_good, his_amt)
    loss = utility_delta(agent, my_good, -my_amt)
    print(agent.name, "receiving a reply: gain = ",
          gain, "and loss =", abs(loss))
    if gain > abs(loss):
        return ACCEPT
    else:
        return INADEQ


def trade(agent, my_good, my_amt, counterparty, his_good, his_amt):
    adj_add_good(agent, my_good, -my_amt)
    adj_add_good(agent, his_good, his_amt)
    adj_add_good(counterparty, his_good, -his_amt)
    adj_add_good(counterparty, my_good, my_amt)


def utility_delta(agent, good, change):
    """
    We are going to determine the utility of goods gained
    (amt is positive) or lost (amt is negative).
    """
    curr_good = agent["goods"][good]
    curr_amt = curr_good[AMT_AVAILABLE]
    curr_util = curr_good["util_func"](curr_amt)
    new_util = curr_good["util_func"](curr_amt + change)
    return ((new_util + curr_util) / 2) * change


def adj_add_good(agent, good, amt):
    agent["util"] += utility_delta(agent, good, amt)
    agent["goods"][good][AMT_AVAILABLE] += amt
