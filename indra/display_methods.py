"""
Filename: display_methods.py
Author: Gene Callahan
A collection of convenience functions
for using matplotlib.
"""

from math import ceil
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import logging
plt.ion()


BLUE = 'b'
RED = 'r'
GREEN = 'g'
YELLOW = 'y'
MAGENTA = 'm'
CYAN = 'c'
BLACK = 'k'
colors = [BLUE, RED, GREEN, YELLOW, MAGENTA, CYAN, BLACK]
NUM_COLORS = len(colors)
X = 0
Y = 1


def get_color(var, i):
    color = None
    if "color" in var:
        color = var["color"]
    if color is None:
        color = colors[i % NUM_COLORS]
    return color


class LineGraph():
    """
    We create a class here to save state for animation.
    Display a simple matplotlib line graph.
    The data is a dictionary with the label
    as the key and a list of numbers as the
    thing to graph.
    data_points is the length of the x-axis.
    """

    def __init__(self, title, varieties, data_points,
                 anim=False, data_func=None):
        self.title = title
        self.anim = anim
        self.data_func = data_func
        self.draw_graph(data_points, varieties)
        if anim:
            animation.FuncAnimation(self.fig,
                                    self.update_plot,
                                    frames=1000,
                                    interval=500,
                                    blit=False)

    def draw_graph(self, data_points, varieties):
        """
        Draw all elements of the graph.
        """
        self.fig, self.ax = plt.subplots()
        x = np.arange(0, data_points)
        self.create_lines(x, self.ax, varieties)
        self.ax.legend()
        self.ax.set_title(self.title)

    def create_lines(self, x, ax, varieties):
        """
        Draw just the data portion.
        """
        self.lines = []
        i = 0
        for var in varieties:
            data = varieties[var]["data"]
            color = get_color(varieties[var], i)
            y = np.array(data)
            ax.plot(x, y, linewidth=2, label=var, alpha=1.0, c=color)
            i += 1

    def show(self):
        """
        Display the plot.
        """
        plt.show()

    def update_plot(self, i):
        """
        This is our animation function.
        For line graphs, redraw the whole thing.
        """
        plt.clf()
        (data_points, varieties) = self.data_func()
        self.draw_graph(data_points, varieties)
        self.show()


class ScatterPlot():
    """
    We are going to use a class here to save state for our animation
    """

    def __init__(self, title, varieties, width, height,
                 anim=True, data_func=None):
        """
        Setup a scatter plot.
        varieties contains the different types of
        entities to show in the plot, which
        will get assigned different colors
        """
        self.scats = None
        self.anim = anim
        self.data_func = data_func
        self.s = ceil(4096 / width)

        fig, ax = plt.subplots()
        ax.set_xlim(0, width)
        ax.set_ylim(0, height)
        self.create_scats(varieties)
        ax.legend()
        ax.set_title(title)
        plt.grid(True)

        if anim:
            animation.FuncAnimation(fig,
                                    self.update_plot,
                                    frames=1000,
                                    interval=500,
                                    blit=False)

    def show(self):
        """
        Display the plot.
        """
        plt.show()

    def update_plot(self, i):
        """
        This is our animation function.
        """
        if self.scats is not None:
            for scat in self.scats:
                if scat is not None:
                    scat.remove()
        varieties = self.data_func()
        self.create_scats(varieties)
        return self.scats

    def get_arrays(self, varieties, var):
        x_array = np.array(varieties[var][X])
        y_array = np.array(varieties[var][Y])
        return (x_array, y_array)

    def create_scats(self, varieties):
        self.scats = []
        i = 0
        for var in varieties:
            (x_array, y_array) = self.get_arrays(varieties, var)
            if len(x_array) <= 0:  # no data to graph!
                next
            elif len(x_array) != len(y_array):
                logging.debug("Array length mismatch in scatter plot")
                next
            color = get_color(varieties[var], i)
            scat = plt.scatter(x_array, y_array,
                               c=color, label=var,
                               alpha=1.0, marker="8",
                               edgecolors='none', s=self.s)
            self.scats.append(scat)
            i += 1
