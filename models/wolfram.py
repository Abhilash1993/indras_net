"""
Wolfram's cellular automata model
"""
import ast

from propargs.propargs import PropArgs

from indra.agent import Agent, switch
from indra.env import Env
from indra.space import DEF_WIDTH
from indra.composite import Composite
from indra.display_methods import BLACK, WHITE, SQUARE

DEBUG = False  # Turns debugging code on or off
DEF_RULE = 30

# Group codes:
W = 0
B = 1

groups = None
rule_dict = None
wolfram_env = None


def create_agent(x, y):
    """
    Create an agent with the passed x, y value as its name.
    """
    name = "(" + str(x) + "," + str(y) + ")"
    return Agent(name=name, action=None)


def turn_black(wolfram_env, groups, agent):
    """
    Automatically change color from one to the other.
    """
    if agent.primary_group() == groups[W]:
        switch(agent, groups[W], groups[B])


def get_color(group):
    """
    Returns W or B, W for white and B for black
    when passed in a group.
    """
    if group == groups[W]:
        return W
    else:
        return B


def get_rule(rule_num):
    """
    Takes in an int for the rule_num
    and returns a dictionary that contains those rules
    read from a master text file that contains all 256 rules.
    """
    rule_str = ""
    with open("wolfram_rules.txt") as rule_line:
        for i, line in enumerate(rule_line):
            if i == rule_num:
                rule_str = line
                break
    return ast.literal_eval(rule_str)


def next_color(rule_dict, left, middle, right):
    """
    Takes in a trio of colors
    and returns the color that the current agent needs to be
    in the next row based on the rule picked by the user.
    """
    return rule_dict[str((left, middle, right))]


def wolfram_action(wolfram_env):
    """
    The action that will be taken every period.
    """
    active_row_y = wolfram_env.height - wolfram_env.get_periods() - 1
    if active_row_y < 1:
        wolfram_env.user.tell_warn("You have exceeded the maximum height"
                                   + " and cannot run the model"
                                   + " for more periods."
                                   + "\nYou can still ask for a scatter plot.")
        wolfram_env.user.exclude_choices(["run", "line_graph"])
        return False
    wolfram_env.user.tell("\nChecking agents in row " + str(active_row_y)
                          + " against the rule...")
    active_row = wolfram_env.get_row_hood(active_row_y)
    next_row = wolfram_env.get_row_hood(active_row_y - 1)
    first_agent_key = "(0," + str(active_row_y) + ")"
    left_color = get_color(active_row[first_agent_key].primary_group())
    x = 0
    for agent in active_row:
        if (x > 0) and (x < wolfram_env.width - 1):
            middle_color = get_color(active_row[agent].primary_group())
            right_color = get_color(active_row["(" + str(x + 1) + ","
                                               + str(active_row_y)
                                               + ")"].primary_group())
            if next_color(rule_dict, left_color, middle_color, right_color):
                next_row_agent_key = ("(" + str(x) + ","
                                      + str(active_row_y - 1) + ")")
                turn_black(wolfram_env, groups, next_row[next_row_agent_key])
            left_color = middle_color
        x += 1
    return True


def set_up(props=None):
    """
    A func to set up run that can also be used by test code.
    """
    global groups
    if props is None:
        pa = PropArgs.create_props('wolfram_props',
                                   ds_file='props/wolfram.props.json')
    else:
        pa = PropArgs.create_props('wolfram_props',
                                   prop_dict=props)
    width = pa.get('grid_width', DEF_WIDTH)
    rule_dict = get_rule(pa.get('rule_number', DEF_RULE))
    height = 0
    height = (width // 2) + (width % 2)
    black = Composite("black", {"color": BLACK, "marker": SQUARE})
    white = Composite("white", {"color": WHITE})
    groups = []
    groups.append(white)
    groups.append(black)
    for y in range(height):
        for x in range(width):
            groups[W] += create_agent(x, y)
    wolfram_env = Env("Wolfram env",
                      action=wolfram_action,
                      random_placing=False,
                      props=pa,
                      height=height,
                      width=width,
                      members=groups)
    wolfram_env.user.exclude_choices(["line_graph"])
    first_agent = wolfram_env.get_agent_at(width // 2, height - 1)
    turn_black(wolfram_env, groups, first_agent)
    return (wolfram_env, groups, rule_dict)


def main():
    global groups
    global wolfram_env
    global rule_dict
    (wolfram_env, groups, rule_dict) = set_up()
    wolfram_env()
    return 0


if __name__ == "__main__":
    main()
