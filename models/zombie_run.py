#!/usr/bin/env python3
"""
A predator-prey model with wolves and sheep.
"""
MODEL_NM = "zombie"

import indra.prop_args2 as props
pa = props.PropArgs.create_props(MODEL_NM)

import indra.utils as utils
import indra.prop_args as props
import models.wolfsheep as wsm

# set up some file names:

def run(prop_dict=None):
    (prog_file, log_file, prop_file, results_file) = utils.gen_file_names(MODEL_NM)
    
    global pa

    # we create a meadow for our agents to act within:
    env = wsm.Meadow("Infected Zone",
                     pa["grid_width"],
                     pa["grid_height"],
                     model_nm=MODEL_NM,
                     preact=True,
                     postact=True,
                     props=pa)
    
    # Now we loop creating multiple agents with numbered names
    # based on the number of agents of that type to create:
    for i in range(pa["num_zombies"]):
        env.add_agent(wsm.Wolf("Zombie" + str(i), "Eating Human",
                               pa["zombie_repro"],
                               pa["zombie_lforce"],
                               rand_age=True))
    for i in range(pa["num_humans"]):
        env.add_agent(wsm.Sheep("Human" + str(i), "Reproducing",
                                pa["human_repro"],
                                pa["human_lforce"],
                                rand_age=True))
    
    return utils.run_model(env, prog_file, results_file)

if __name__ == "__main__":
    run()
