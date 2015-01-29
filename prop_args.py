"""
prop_args.py
Set, read, and write program-wide properties in one
location. Includes logging.
"""

import logging
import networkx as nx
import json
import node


class PropArgs(node.Node):

    """
    This class holds sets of named properties for program-wide values.
    """

    prop_sets = {}


    @staticmethod
    def get_props(model_nm):
        """
        Get properties for model 'model_nm'.
        """
        if model_nm in PropArgs.prop_sets:
            return PropArgs.prop_sets[model_nm]


    @staticmethod
    def create_props(model_nm, props={}):
        """
        Create a property object with values in 'props'.
        """
        return PropArgs(model_nm, props)


    @staticmethod
    def read_props(model_nm, file_nm):
        """
        Create a new PropArgs object from a json file
        """
        props = json.load(open(file_nm))
        return PropArgs.create_props(model_nm, props)

    
    def __init__(self, model_nm, logfile=None, props=None):
        super().__init__("Properties")
        self.model_nm = model_nm
# store this instance as the value in the dict for 'model_nm'
        PropArgs.prop_sets[model_nm] = self
        self.graph = nx.Graph()
        if props is None:
            self.props = {}
        else:
            self.props = props
        self.logger = Logger(self, logfile=logfile)
        self.graph.add_edge(self, self.logger)


    def display(self):
        """
        How to represent the properties on screen.
        """
        ret = "Properties for " + self.model_nm + "\n"
        for prop in self.props:
            ret += "\t" + prop + ": " + str(self.props[prop]) + "\n"

        return ret


    def set(self, nm, val):
        """
        Set a property value.
        """
        self.props[nm] = val


    def get(self, nm, default=None):
        """
        Get a property value, with a default
        that gets stored if the property is not there
        at the time of the call.
        """
        if nm not in self.props:
            self.props[nm] = default
        return self.props[nm]


    def get_logfile(self):
        """
        Special get function for logfile name
        """
        return self.props.get("log_fname")


    def write(self, file_nm):
        """
        Write properties to json file.
        Useful for storing interesting parameter sets.
        """
        json.dump(self.props, open(file_nm, 'w'), indent=4)


class Logger(node.Node):
    """
    A class to track how we are logging.
    """

    DEF_FORMAT = '%(asctime)s:%(levelname)s:%(message)s'
    DEF_LEVEL = logging.INFO
    DEF_FILEMODE = 'w'
    DEF_FILENAME = 'log.txt'

    def __init__(self, props, logfile=None):
        super().__init__("Logger")
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


