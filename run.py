
import argparse
import indra.utils as utils
import models.basic_model as bm

from indra.prop_args_refactoring import PropArgs

def run(model_nm):
    (prog_file, log_file, prop_file, results_file) = utils.gen_file_names(model_nm)

    pa = PropArgs(model_nm)

    env = bm.BasicEnv(model_nm=model_nm, props=pa)
    utils.run_model(env, prog_file, results_file)


parser = argparse.ArgumentParser(description="parser for command-line savvy users")
parser.add_argument('model_nm',
                    metavar="model_nm",
                    type=str,
                    help="the name of the model you want to run")
args = parser.parse_args()


run(args.model_nm)

