#!/usr/bin/env python3
"""
Runs a fashion model with hipsters and followers.
"""

import indra.utils as utils
import indra.prop_args as props
import fashion_model as fm

# set up some file names:
MODEL_NM = "fashion_model"
(prog_file, log_file, prop_file, results_file) = utils.gen_file_names(MODEL_NM)

# We store basic parameters in a "property" file; this allows us to save
#  multiple parameter sets, which is important in simulation work.
#  We can read these in from file or set them here.
pa = utils.read_props(MODEL_NM)
if pa is None:
    pa = props.PropArgs(MODEL_NM, logfile=log_file, props=None)
    pa.set("model", MODEL_NM)
    utils.get_grid_dims(pa, 16)
    utils.get_agent_num(pa, "num_followers", "followers", 48)
    utils.get_agent_num(pa, "num_hipsters", "hipsters", 16)
    pa.ask("fmax_move", "What is the follower's max move?", int, default=4,
           limits=utils.GRID_LIMITS)
    pa.ask("hmax_move", "What is the hipster's max move?", int, default=4,
           limits=utils.GRID_LIMITS)
    pa.ask("min_adv_periods", "What are the minimum adverse periods?", int,
           default=6, limits=(1, 100))


# Now we create a minimal environment for our agents to act within:
env = fm.Society("Society",
                 pa.get("grid_height"),
                 pa.get("grid_width"),
                 torus=False,
                 model_nm=MODEL_NM)

# Now we loop creating multiple agents with numbered names
# based on the loop variable:
for i in range(pa.get("num_followers")):
    env.add_agent(fm.Follower("follower" + str(i), "Looking like hipsters",
                              pa.get("fmax_move")))
for i in range(pa.get("num_hipsters")):
    env.add_agent(fm.Hipster("hipster" + str(i), "Looking trendy",
                             pa.get("hmax_move")))

utils.run_model(env, prog_file, results_file)
