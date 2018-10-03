#!/usr/bin/env python3
"""
This is a simple test script. It can be cloned to
create new run scripts, and should be run to test
the system after library changes.
"""
MODEL_NM = "standing_ovation"

import random
import indra.prop_args2 as props
pa = props.PropArgs.create_props(MODEL_NM)

import indra.utils as utils
import models.standing_ovation as stov

def run(prop_dict=None):
    (prog_file, log_file, prop_file, results_file) = utils.gen_file_names(MODEL_NM)

    global pa
    #Create audience with width x height
    env = stov.AudienceEnv("Audience",
                           pa["grid_width"],
                           pa["grid_height"],
                           model_nm = MODEL_NM,
                           preact = True,
                           act = True,
                           props = pa
                           )
    #Generate audience members
    for i in range(30): #change this to width x height somehow
        noise = random.uniform(0.7,9.0)
        env.add_agent(stov.AudienceAgent("Member" + str(i), "Enjoying show",
                               pa["member_sitting"],
                               pa["noise_level"],
                               pa["member_standard"],
                               rand_age=True))
    #Saving these in case I have to test this
    # # test prop_args as an iterable:
    # for prop, val in pa.items():
    #     print(prop + ": " + str(val))
    #
    # # test that props work as a dictionary:
    # if "num_agents" in pa:
    #     print("In is working!")
    #
    # # test what pa["num_agents"] is:
    # num_agents = pa["num_agents"]
    # print("num_agents = " + str(num_agents))
    #
    # # make sure we can get props length:
    # print("Props length = " + str(len(pa)))
    #
    # # Now we create a minimal environment for our agents to act within:
    # env = bm.BasicEnv(model_nm=MODEL_NM, props=pa)
    #
    # # Now we loop creating multiple agents
    # #  with numbered names based on the loop variable:
    # for i in range(num_agents):
    #     env.add_agent(bm.BasicAgent(name="agent" + str(i),
    #                                 goal="acting up!"))

    return utils.run_model(env, prog_file, results_file)


if __name__ == "__main__":
    run()
