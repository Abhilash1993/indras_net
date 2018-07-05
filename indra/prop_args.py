"""
prop_args.py
Set, read, and write program-wide properties in one location. Includes logging.
"""
import logging
import sys
import platform
import networkx as nx
import json
import os

SWITCH = '-'
PERIODS = 'periods'
DATAFILE = 'datafile'

# user types
TERMINAL = "terminal"
IPYTHON = "iPython"
IPYTHON_NB = "iPython Notebook"
WEB = "Web browser"

global user_type
user_type = TERMINAL

type_dict = {'INT': int, 'DBL': float, 'BOOL': bool, 'STR': str}

def get_prop_from_env(prop_nm):
    global user_type
    try:
        user_type = os.environ['user_type']
    except KeyError:
        logging.info("Environment variable user type not found")
        user_type = TERMINAL
    return user_type

class PropArgs():
    """
    This class holds named properties for program-wide values.
    It enables getting properties from a file, a database,
    or from the user, either via the command line or a prompt.
    """

    @staticmethod
    def create_props(model_nm, props=None):
        """
        Create a property object with values in 'props'.
        """
        global user_type

        if props is None:
            props = {}
            user_type = get_prop_from_env("user_type")
            props["user_type"] = user_type
        return PropArgs(model_nm, props=props)

    @staticmethod
    def read_props(model_nm, file_nm):
        """
        Create a new PropArgs object from a json file
        """
        props = json.load(open(file_nm))
        return PropArgs.create_props(model_nm, props=props)


    def __init__(self, model_nm, logfile=None, props=None,
                 loglevel=logging.INFO):
        self.model_nm = model_nm
        self.graph = nx.Graph()
        if props is None:
            self.props = {}
        else:
            self.props = props
            logfile = self.get("log_fname")
        self.logger = Logger(self, logfile=logfile)
        self.graph.add_edge(self, self.logger)
        self["OS"] = platform.system()
        self["model"] = model_nm
        # process command line args and set them as properties:
        prop_nm = None
        for arg in sys.argv:
            # the first arg (-prop) names the property
            if arg.startswith(SWITCH):
                prop_nm = arg.lstrip(SWITCH)
            # the second arg is the property value
            elif prop_nm is not None:
                self[prop_nm] = arg
                prop_nm = None

    def add_props(self, props):
        self.props.update(props)

    def display(self):
        """
        How to represent the properties on screen.
        """
        ret = "Properties for " + self.model_nm + "\n"
        for prop in self.props:
            ret += "\t" + prop + ": " + str(self.props[prop]) + "\n"

        return ret

    def __iter__(self):
        return iter(self.props)

    def __str__(self):
        return self.display()

    def __len__(self):
        return len(self.props)

    def __contains__(self, key):
        return key in self.props

    def __setitem__(self, key, value):
        """
        Set a property value.
        """
        self.props[key] = value

    def __getitem__(self, key):
        return self.props[key]

    def get(self, nm, default=None):
        """
        Get a property value, with a default
        that gets stored if the property is not there
        at the time of the call.
        """
        if nm not in self.props:
            self.props[nm] = default
        return self.props[nm]

    def __delitem__(self, key):
        del self.props[key]

    def items(self):
        return self.props.items()

    def get_logfile(self):
        """
        Special get function for logfile name
        """
        return self.props["log_fname"]

    def write(self, file_nm):
        """
        Write properties to json file.
        Useful for storing interesting parameter sets.
        """
        json.dump(self.props, open(file_nm, 'w'), indent=4)


class Logger():
    """
    A class to track how we are logging.
    """

    DEF_FORMAT = '%(asctime)s:%(levelname)s:%(message)s'
    DEF_LEVEL = logging.INFO
    DEF_FILEMODE = 'w'
    DEF_FILENAME = 'log.txt'

    def __init__(self, props, logfile=None,
                 loglevel=logging.INFO):
        if logfile is None:
            logfile = Logger.DEF_FILENAME
        fmt = props.get("log_format", Logger.DEF_FORMAT)
        lvl = props.get("log_level", Logger.DEF_LEVEL)
        fmd = props.get("log_fmode", Logger.DEF_FILEMODE)
        fnm = props.get("log_fname", logfile)
        logging.basicConfig(format=fmt,
                            level=lvl,
                            filemode=fmd,
                            filename=fnm)
        logging.info("Logging initialized.")
