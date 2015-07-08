#!/usr/bin/env python3
"""
A predator-prey model with wolves and sheep.
"""

import indra.utils as utils
import indra.prop_args as props
import wolfsheep_model as wsm

# set up some file names:
MODEL_NM = "wolfsheep_model"
(prog_file, log_file, prop_file, results_file) = utils.gen_file_names(MODEL_NM)

# We store basic parameters in a "property" file; this allows us to save
#  multiple parameter sets, which is important in simulation work.
#  We can read these in from file or set them here.
pa = utils.read_props(MODEL_NM)
if pa is None:
    pa = props.PropArgs(MODEL_NM, logfile=log_file, props=None)
    pa.set("model", MODEL_NM)
    pa.ask("num_wolves", "What is num wolves?", int, default=4)
    pa.ask("num_sheep", "What is num sheep?", int, default=16)
    pa.ask("grid_width", "What is grid width?", int, default=16)
    pa.ask("grid_height", "What is grid height?", int, default=16)
    pa.ask("wolf_repro", "What is the wolf reproduction age?", int, default=8)
    pa.ask("wolf_lforce", "What is the wolf life force?", int, default=7)
    pa.ask("sheep_repro", "What is the sheep reproduction age?", int,
           default=4)
    pa.ask("sheep_lforce", "What is the sheep life force?", int, default=5)

# Now we create a meadow for our agents to act within:
env = wsm.Meadow("Meadow",
                 pa.get("grid_height"),
                 pa.get("grid_width"),
                 model_nm=MODEL_NM,
                 preact=True)

# Now we loop creating multiple agents with numbered names
# based on the number of agents of that type to create:
for i in range(pa.get("num_wolves")):
    env.add_agent(wsm.Wolf("wolf" + str(i), "Eating sheep",
                           pa.get("wolf_repro"),
                           pa.get("wolf_lforce")))
for i in range(pa.get("num_sheep")):
    env.add_agent(wsm.Sheep("sheep" + str(i), "Reproducing",
                            pa.get("sheep_repro"),
                            pa.get("sheep_lforce")))

utils.run_model(env, prog_file, results_file)
