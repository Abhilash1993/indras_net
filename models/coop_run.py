# -*- coding: utf-8 -*-
"""
Created on Tue Nov 11 21:13:15 2014

@author: Brandon
"""

import logging
import indra.utils as utils
import indra.prop_args as props
import coop_model as cm

MODEL_NM = "coop_model"
(prog_file, log_file, prop_file, results_file) = utils.gen_file_names(MODEL_NM)

read_props = False
if read_props:
    pa = props.PropArgs.read_props(MODEL_NM, prop_file)
else:
    pa = props.PropArgs(MODEL_NM, logfile=log_file, props=None)
    pa.set("model", MODEL_NM)
    pa.set("num_agents", 100)
    pa.set("min_holdings", 4.5)

env = cm.CoopEnv(model_nm=MODEL_NM)

for i in range(pa.get("num_agents")):
    env.add_agent(
        cm.CoopAgent('agent' + str(i), 5, 0))

logging.info("Starting program " + prog_file)

env.run()
