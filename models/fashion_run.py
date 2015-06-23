#!/usr/bin/env python3
"""
fashion_run.py: A script to run fashion_model.py,
which implements Adam Smith's fashion model.
"""

import indra.utils as utils
import indra.node as node
import indra.prop_args as props
import predprey_model as ppm
import fashion_model as fm

MODEL_NM = "fashion_model"
(prog_file, log_file, prop_file, results_file) = utils.gen_file_names(MODEL_NM)

pa = utils.read_props(MODEL_NM)
if pa is None:
    pa = props.PropArgs(MODEL_NM, logfile=log_file, props=None)

    pa.set("model", MODEL_NM)

    pa.set("num_trndstr", 20)
    pa.set("num_flwr", 80)

    pa.set("fshn_f_ratio", 1.3)
    pa.set("fshn_t_ratio", 1.5)

    pa.set("flwr_others", 3)
    pa.set("trnd_others", 5)

    pa.set("flwr_max_detect", 20.0)
    pa.set("trnd_max_detect", 20.0)

    pa.set("min_adv_periods", 8)

env = fm.SocietyEnv("society", 50.0, 50.0, model_nm=MODEL_NM)

for i in range(pa.get("num_flwr")):
    env.add_agent(fm.Follower(name="prole" + str(i),
                  max_detect=pa.get("flwr_max_detect")))

for i in range(pa.get("num_trndstr")):
    env.add_agent(fm.TrendSetter(name="hipster" + str(i),
                  max_detect=pa.get("trnd_max_detect")))

node.add_prehension(fm.Follower, ppm.EAT, fm.TrendSetter)
node.add_prehension(fm.TrendSetter, ppm.AVOID, fm.Follower)

utils.run_model(env, prog_file, results_file)
