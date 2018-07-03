#!/usr/bin/env python3
"""
This file runs the forestfire_model.
"""
MODEL_NM = "Forest Fire"

import indra.prop_args as props
pa = props.PropArgs.create_props(MODEL_NM)

import indra.prop_args as props
import indra.utils as utils
import models.forestfire_model as fm

DEF_GRID_DIM = 80
DEF_DENS = .43
DEF_REGEN = 20
DEF_LIGHTNING = 4

# set up some file names:


def run(prop_dict=None):
    (prog_file, log_file, prop_file, results_file) = utils.gen_file_names(MODEL_NM)
    
    # We store basic parameters in a
    # "property" file; this allows us to save
    #  multiple parameter sets, which is important in simulation work.
    #  We can read these in from file or set them here.
    global pa

    if prop_dict is not None:
        prop_dict[props.PERIODS] = 100
        pa.add_props(prop_dict)
    else:
        result = utils.read_props(MODEL_NM)
        if result:
            pa.add_props(result.props)
        else:
            utils.ask_for_params(pa)

    density = pa.get("density")
    grid_x = pa.get("grid_width")
    grid_y = pa.get("grid_height")
    
    # Now we create a forest environment for our agents to act within:
    env = fm.ForestEnv(grid_x, grid_y, density, pa.get("strike_freq"),
                       pa.get("regen_period"),
                       model_nm=MODEL_NM, torus=False,
                       props=pa)
    num_agents = int(grid_x * grid_y * density)
    
    for i in range(num_agents):
        env.add_agent(fm.Tree(name="tree" + str(i)))
    
    utils.run_model(env, prog_file, results_file)

if __name__ == "__main__":
    run()
