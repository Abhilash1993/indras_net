"""
1. The name of this file is terrible: what is a `run_dict_helper`?
   It should be `function_registry`.
2. It is in the wrong place: we need a registry dir.
3. We don't need to register any member creator functions for
   models that don't birth new agents as they run. That means
   right now I believe *only* wolfsheep needs one!
"""
from APIServer.model_creator_api import generate_func
from models.bacteria import bacterium_action, toxin_action, nutrient_action
from models.bacteria import main as bactmain
from models.bacteria import set_up as bactset_up
from models.basic import agent_action
from models.basic import main as bamain
from models.basic import set_up as baset_up
from models.fashion import follower_action, common_action, tsetter_action
from models.fashion import main as famain
from models.fashion import set_up as faset_up
from models.fmarket import main as fmmain
from models.fmarket import market_maker_action, trend_follower_action
from models.fmarket import plot_asset_price
from models.fmarket import set_up as fmset_up
from models.fmarket import value_investor_action
from models.forestfire import main as ffmain
from models.forestfire import set_up as ffset_up
from models.forestfire import tree_action
from models.segregation import main as segmain
from models.segregation import set_up as segset_up
from models.segregation import seg_agent_action
from models.wolfsheep import main as wsmain
from models.wolfsheep import set_up as wsset_up
from models.wolfsheep import sheep_action, wolf_action

rdict = {
    "basic": bamain,
    "bacteria": bactmain,
    "fashion": famain,
    "fmarket": fmmain,
    "forestfire": ffmain,
    "segregation": segmain,
    "wolfsheep": wsmain,
}

setup_dict = {
    "basic": baset_up,
    "bacteria": bactset_up,
    "fashion": faset_up,
    "fmarket": fmset_up,
    "forestfire": ffset_up,
    "segregation": segset_up,
    "wolfsheep": wsset_up,
}

action_dict = {
    "agent_action": agent_action,
    "follower_action": follower_action,
    "common_action": common_action,
    "tsetter_action": tsetter_action,
    "tree_action": tree_action,
    "sheep_action": sheep_action,
    "wolf_action": wolf_action,
    "bacterium_action": bacterium_action,
    "toxin_action": toxin_action,
    "nutrient_action": nutrient_action,
    "market_maker_action": market_maker_action,
    "seg_agent_action": seg_agent_action,
    "trend_follower_action": trend_follower_action,
    "value_investor_action": value_investor_action,
    "generate_func": generate_func
}

aux_funcs_dict = {
    "plot_asset_price": plot_asset_price,
}
