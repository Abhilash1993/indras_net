"""
node.py
A very basic class implementing some thing at the bottom of our
net of objects
"""

import logging
import inspect
import matplotlib.pyplot as plt
import networkx as nx

UNIVERSAL = "universal"

indras_net = nx.Graph()


def get_class_name(genera):
    return genera.__name__


def get_prehensions(prehender, universal):
    """
    Find prehensions for a prehender.
    """
    return universals.get_prehensions(prehender, universal)


def add_prehension(prehender, universal, prehended):
    """
    Add a prehension between classes
    """
    logging.info("Prehender = %s for universal %s" % (prehender, universal))
    prnr_type = get_class_name(prehender)
    prnd_type = get_class_name(prehended)
    universals.add_prehension(prnr_type, universal, prnd_type)


def add_ent_prehension(prehender, universal, prehended):
    """
    Add a prehension between entities.
    """
    universals.add_prehension(prehender, universal, prehended)


class Node():
    """
    Contains a name and a graph.
    """

    class_graph = nx.Graph()  # we are going to graph our class hierarchy
    node_added = False

    @classmethod
    def class_draw(cls):
        """
        This draws our class hierarchy.
        """
        if cls.class_graph is not None:
            plt.title("Class Hierarchy")
            nx.draw_networkx(cls.class_graph)
            plt.show()

    @classmethod
    def connect_to_class_tree(cls):
        for c in inspect.getmro(cls):
            if c != cls:
                if c.__name__ not in Node.class_graph:
                    c.connect_to_class_tree()
                    break
                else:
                    Node.class_graph.add_edge(get_class_name(c),
                                              get_class_name(cls))
                    return
        cls.connect_to_class_tree()  # call until all upper classes are in

    def __init__(self, name):
        self.name = name
# every node is potentially a graph itself
        self.graph = None
        self.ntype = self.__class__.__name__
        if not Node.node_added:
            Node.class_graph.add_node(Node.__name__)
        if self.ntype not in Node.class_graph:
            self.__class__.connect_to_class_tree()

    def __str__(self):
        return self.name

    def draw(self):
        """
        Every node should have some way to draw itself.
        """
        if self.graph is not None:
            nx.draw_networkx(self.graph)
            plt.show()

    def display(self):
        """
        Every node should have some way to display itself.
        The difference between draw and display:
        Display makes the object show up on screen.
        Draw reveals the object's structure (such
        as graphing its components).
        """
        pass

    def get_type(self):
        """
        Returns node's type.
        By default, this is its class name.
        """
        return self.ntype

    def set_type(self, new_type):
        """
        Change node's type.
        Use caution: A lot depends on this field!
        In particular, AgentPop uses it to sort agents.
        """
        self.ntype = new_type

    def to_json(self):
        return {"name": self.name}


class Universals(Node):
    """
    Our universals, the things which relate instances
    or classes.
    """

    universals_graphed = False

    def __init__(self):
        super().__init__("Universals")
        self.unis = {}
        self.graph = nx.MultiDiGraph()
        if not Universals.universals_graphed:
            pass

    def add_universal(self, uni):
        """
        We want to be able to view all
        univeral relationships at a glance,
        so we will store them here
        """
        self.unis[uni] = []  # a list of prehensions

    def add_prehension(self, prehender, uni, prehended):
        """
        Adds a universal relationship between two classes
        """
        if uni not in self.unis:
            self.add_universal(uni)
        self.unis[uni].append([prehender, prehended])
        self.graph.add_edge(prehender, prehended,
                            universal=uni)

    def get_prehensions(self, prehender, uni):
        """
        Find all prehensions for some prehender.
        """
        prehensions = []
        logging.debug("edges = " + str(self.graph.edges()))
        for etuple in self.graph.edges_iter(data=True):
            hender = etuple[0]
            hended = etuple[1]
            edge_data = etuple[2]
            prehension = edge_data[UNIVERSAL]
            logging.debug("Comparing hender = "
                          + hender
                          + " with prehender = "
                          + prehender)
            if uni == prehension and hender == prehender:
                logging.debug("Found our universal: " + uni)
                prehensions.append(hended)
        logging.debug("prehensions = " + str(prehensions))
        return prehensions

universals = Universals()
