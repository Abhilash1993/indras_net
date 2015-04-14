"""
A script to test our grid capabilities.
"""

import logging
import indra.utils as utils
import indra.prop_args as props
import indra.grid_env as ge
import bacterium_model as bm

# set up some file names:
MODEL_NM = "grid_model"
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
    pa.set("num_agents", 1)
    pa.set("grid_width", 4)
    pa.set("grid_height", 4)

# Now we create a minimal environment for our agents to act within:
env = ge.GridEnv("Test grid env",
                 pa.get("grid_height"),
                 pa.get("grid_width"),
                 torus=False,
                 model_nm=MODEL_NM,
                 postact=True)

# Now we loop creating multiple agents with numbered names
# based on the loop variable:
"""
for i in range(pa.get("num_agents")):
"""

# Add our bacterium and our food source to the env
env.add_agent(bm.Bacterium(name="Rick",goal="work"))

env.add_agent(bm.FoodSource(name="Runaway Food", goal="not get eaten"))

# Logging is automatically set up for the modeler:
logging.info("Starting program " + prog_file)

# let's test our iterator
for cell in env.coord_iter():
    print("Contents of cell x = "
          + str(cell[1])
          + " and y = "
          + str(cell[2])
          + " is "
          + str(cell[0]))

# And now we set things running!
env.run()
env.record_results(results_file)
