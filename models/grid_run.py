"""
A script to test our grid capabilities.
"""

import logging
import indra.utils as utils
import indra.prop_args as props
import indra.grid_env as ge
import grid_model as gm

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
    pa.set("num_agents", 4)
    pa.set("grid_width", 3)
    pa.set("grid_height", 3)

# Now we create a minimal environment for our agents to act within:
env = ge.GridEnv("Test grid env",
                 pa.get("grid_height"),
                 pa.get("grid_width"),
                 torus=False,
                 model_nm=MODEL_NM,
                 preact=True)

# Now we loop creating multiple agents with numbered names
# based on the loop variable:
for i in range(pa.get("num_agents")):
    env.add_agent(gm.TestGridAgent(name="agent" + str(i),
                  goal="taking up a grid space!"))

# Logging is automatically set up for the modeler:
logging.info("Starting program " + prog_file)

# let's test our iterator
for cell in env:
    (x, y) = cell.coords
    print("Contents of cell x = " + str(x)
          + " and y = " + str(y)
          + " is " + str(cell.contents))

# And now we set things running!
env.run()
env.record_results(results_file)
