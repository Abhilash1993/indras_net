"""
A predator-prey model with wolves and sheep.
"""

import logging
import indra.utils as utils
import indra.prop_args as props
import wolfsheep_model as wsm

# set up some file names:
MODEL_NM = "wolfsheep_model"
(prog_file, log_file, prop_file, results_file) = utils.gen_file_names(MODEL_NM)

# We store basic parameters in a "property" file; this allows us to save
#  multiple parameter sets, which is important in simulation work.
#  We can read these in from file or set them here.
read_props = False
if read_props:
    pa = props.PropArgs.read_props(MODEL_NM, prop_file)
else:
    pa = props.PropArgs(MODEL_NM, logfile=log_file, props=None)
    pa.set("model", MODEL_NM)
    pa.set("num_wolves", 4)
    pa.set("num_sheep", 16)
    pa.set("grid_width", 16)
    pa.set("grid_height", 16)

# Now we create a minimal environment for our agents to act within:
env = wsm.Meadow("Meadow",
                 pa.get("grid_height"),
                 pa.get("grid_width"),
                 torus=False,
                 model_nm=MODEL_NM,
                 preact=True)

# Now we loop creating multiple agents with numbered names
# based on the loop variable:
for i in range(pa.get("num_wolves")):
    env.add_agent(wsm.Wolf("wolf" + str(i), "Eating sheep"))
for i in range(pa.get("num_sheep")):
    env.add_agent(wsm.Sheep("sheep" + str(i), "Reproducing"))

# Logging is automatically set up for the modeler:
logging.info("Starting program " + prog_file)

# And now we set things running!
env.run()
env.record_results(results_file)
