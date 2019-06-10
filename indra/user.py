"""
This file defines User, which represents a user in our system.
"""
import json
from indra.agent import Agent  # , DEBUG2  # DEBUG,
from IPython import embed

TERMINAL = "terminal"
TEST = "test"
WEB = "web"
GUI = "gui"
NOT_IMPL = "Choice not yet implemented."
CANT_ASK_TEST = "Can't ask anything of a scripted test"
DEF_STEPS = 1
USER_EXIT = -999


def not_impl(user):
    return user.tell(NOT_IMPL)


def run(user, test_run=False):
    steps = 0
    acts = 0
    try:
        if not test_run:
            steps = user.ask("How many periods?")
            if steps is None or steps == "" or steps.isspace():
                steps = DEF_STEPS
            else:
                steps = int(steps)
            user.tell("Steps = " + str(steps))
        else:
            steps = DEF_STEPS

        acts = user.env.runN(periods=steps)
    except (ValueError, TypeError) as e:
        user.tell("You must enter an integer value for # of steps: "
                  + str(e))
    return acts


def leave(user):
    user.tell("Goodbye, " + user.name + ", I will miss you!")
    return USER_EXIT


def scatter_plot(user):
    user.tell("Drawing a scatter plot.")
    return user.env.scatter_graph()


def line_graph(user):
    user.tell("Drawing a line graph.")
    return user.env.line_graph()


def ipython(user):
    embed()


MSG = 0
FUNC = 1

QUIT = 0
RUN = 1


class TermUser(Agent):
    """
    A representation of the user in the system.
    """
    def __init__(self, name, env, **kwargs):
        super().__init__(name, **kwargs)
        self.env = env  # this class needs this all the time, we think

    def tell(self, msg, end='\n'):
        """
        How to tell the user something.
        """
        print(msg, end=end)
        return msg

    def ask(self, msg, default=None):
        """
        How to ask the user something.
        """
        self.tell(msg, end=' ')
        choice = input()
        if not choice:
            return default
        else:
            return choice

    def log(self, msg, end='\n'):
        """
        How to log something for this type of user.
        Our default is going to be the same as tell, for now!
        """
        return self.user.tell(msg, end)

    def __call__(self):
        DEFAULT_CHOICE = '0'
        menu_item = None
        menu_list = None
        with open("/indras_net/indra/menu.props.json",
                  'r') as f:
            menu_item = json.load(f)
        menu_list = menu_item["menu_database"]
        menu_display = "Displaying the menu"
        stars = "*" * len(menu_display)
        self.tell("What would you like to do?")
        print("\n",
              stars, "\n",
              menu_display, "\n",
              stars)
        for choice, menuId in enumerate(menu_list):
            print(str(choice) + ". ", menuId["question"])
        c = input()
        if not c or c.isspace():
            c = DEFAULT_CHOICE
        choice = int(c)
        if choice >= 0 and choice < len(menu_list):
            ret = 0
            exec(menu_list[choice]["run"])
            return ret
        else:
            self.user.tell("Invalid Option")


class TestUser(TermUser):
    """
        This is our test user, who has some characteristics different from the
        terminal user, such as overriding ask() and __call__().
    """
    def ask(self, msg, default=None):
        """
            Can't ask anything of a scripted test!
        """
        return self.tell(CANT_ASK_TEST, end=' ')

    def __call__(self):
        """
            Can't present menu to a scripted test!
        """
        run(self)  # noqa: W391


class WebUser(TermUser):
    """
    This is our web user, who is expected to communicate with a web page
    frontend.
    """
    def tell(self, msg, end='\n'):
        """
        Tell the user something by showing it on the web page
        """
        # Some json thing
        pass

    def ask(self, msg, default=None):
        """
        Ask the user something and present it to the web page
        """
        # Some json thing
        pass
