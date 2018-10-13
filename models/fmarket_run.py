#!/usr/bin/env python3
"""
Runs a financial market model with value investors and chart followers.
"""

import indra.prop_args2 as props

MODEL_NM = "fmarket"


def run(prop_dict=None):
    pa = props.PropArgs.create_props(MODEL_NM, prop_dict)
    import indra.utils as utils
    import models.fmarket as fm

    (prog_file, log_file, prop_file, results_file) = utils.gen_file_names(MODEL_NM)
    
    # Now we create a asset environment for our agents to act within:
    env = fm.FinMarket("Financial Market",
                       pa["grid_height"],
                       pa["grid_width"],
                       torus=False,
                       model_nm=MODEL_NM,
                       props=pa)
    
    # Now we loop creating multiple agents with numbered names
    # based on the loop variable:
    for i in range(pa["num_followers"]):
        env.add_agent(fm.ChartFollower("follower" + str(i),
                                       "Following trend",
                                       pa["fmax_move"],
                                       pa["variability"]))
    for i in range(pa["num_vinvestors"]):
        env.add_agent(fm.ValueInvestor("value_inv" + str(i), "Buying value",
                                       pa["vmax_move"],
                                       pa["variability"]))
    
    return utils.run_model(env, prog_file, results_file)


if __name__ == "__main__":
    run()
