"""
env.py
Our base environment class for hosting agents.
Other specialized environments inherit from this.
"""

from collections import deque
import sys
import time
import pdb
import getpass
import IPython
import networkx as nx
import indra.display_methods as disp
import indra.node as node
import indra.menu as menu
import indra.prop_args as pa
import indra.agent_pop as ap
import indra.user as user


class Environment(node.Node):
    """
    A basic environment allowing starting, stopping,
    stepping, inspection and editing of key objects,  etc.
    """

    prev_period = 0  # in case we need to restore state

    def __init__(self, name, preact=False,
                 postact=False, model_nm=None):
        super().__init__(name)
        self.graph = nx.Graph()
        pop_name = ""
        if model_nm:
            pop_name += model_nm + " "
        pop_name += "Agents"
        self.agents = ap.AgentPop(pop_name)
        self.graph.add_edge(self, self.agents)
        self.womb = []
        self.period = 0
        self.preact = preact
        self.postact = postact
        self.disp_census = False
        self.model_nm = model_nm
        if model_nm is not None:
            self.props = pa.PropArgs.get_props(model_nm)
        else:
            self.props = None

        user_nm = getpass.getuser()
        self.props.set("user_name", user_nm)
        user_type = self.props.get("user_type", user.User.TERMINAL)
        self.user = user.User(user_nm, user_type)
        self.graph.add_edge(self, self.user)
        self.menu = menu.MainMenu("Main Menu", self)
        self.graph.add_edge(self, self.menu)
        self.graph.add_edge(self, self.props)
        self.graph.add_edge(self, node.universals)

    def add_agent(self, agent):
        """
        Add an agent to pop.
        """
        self.agents.append(agent)
        agent.add_env(self)

    def join_agents(self, a1, a2):
        """
        Relate two agents.
        """
        self.agents.join_agents(a1, a2)

    def add_child(self, agent):
        """
        Put a child agent in the womb.
        """
        self.womb.append(agent)
        agent.add_env(self)

    def find_agent(self, name):
        """
        Find an agent by name.
        """
        for agent in self.agents:
            if agent.name == name:
                return agent
        return None

    def get_agents_of_var(self, var):
        """
        Return all agents of type 'var'.
        """
        return self.agents.get_agents_of_var(var)

    def run(self, resume=False, loops=0):
        """
        This is the main menu loop for all models.

        resume: starts up from a previous period.
        loops: run x loops, perhaps for timing purposes.
        """

        if resume:
            self.period = Environment.prev_period
        else:
            self.period = 0

        if loops > 0:
            while self.period < loops:
                self.step()
            self.user.tell("Ran for " + str(self.period) + " periods.")
        else:
            self.user.tell("Welcome, " + self.user.name)
            self.user.tell("Running in " + self.name)
            msg = self.menu.display()
            while msg is None:
                msg = self.menu.display()
                self.user.tell("\nMain Menu; Period: " + str(self.period))

            Environment.prev_period = self.period

            self.user.tell(msg)

    def add_menu_item(self, submenu, letter, text, func):
        """
        This func exists to screen the menu class from outside objects:
        no need for them to know more than the env
        """
        self.menu.add_menu_item(submenu, letter, text, func)

    def debug(self):
        """
        Invoke the python debugger.
        """
        pdb.set_trace()

    def ipython(self):
        """
        Kick off iPython.
        """
        IPython.start_ipython(argv=[])

    def eval_code(self):
        """
        Evaluate a line of code.
        """
        eval(self.user.ask("Type a line of code to run: "))

    def list_agents(self):
        """
        List all agents in env.
        """
        self.user.tell("Active agents in environment:")
        for agent in self.agents:
            self.user.tell(agent.name
                           + " with a goal of "
                           + agent.goal)

    def add(self):
        """
        Add a new agent to the env.
        """
        exec("import " + self.props.get("model")
             + " as m")
        constr = self.user.ask("Enter constructor for agent to add: ")
        new_agent = eval("m." + constr)
        self.add_agent(new_agent)

    def agnt_inspect(self):
        """
        View (and possibly alter) an agent's data.
        """
        name = self.user.ask(
            "Type the name of the agent to inspect: ")
        agent = self.find_agent(name.strip())
        if agent is None:
            self.user.tell("No such agent")
        else:
            agent.pprint()
        self.edit_field(agent)

    def env_inspect(self):
        """
        Have a look at (and possibly alter) the environment.
        """
        self.pprint()
        self.edit_field(self)

    def edit_field(self, entity):
        """
        Edit a field in an entity.
        """
        while True:
            y_n = self.user.ask("Change a field's value in "
                                + entity.name
                                + "? (y/n) "
                                + "(Only str, float, and int supported.)")
            if y_n in ["Y", "y"]:
                field = self.user.ask("Which field? ")
                nval = self.user.ask("Enter new value for "
                                     + field + ": ")
                fld_type = type(entity.__dict__[field])
                if fld_type is int:
                    entity.__dict__[field] = int(nval)
                elif fld_type is float:
                    entity.__dict__[field] = float(nval)
                else:
                    entity.__dict__[field] = nval
            else:
                break

    def cont_run(self):
        """
        Run continuously.
        """
        self.user.tell(
            "Running continously; press Ctrl-c to halt!")
        time.sleep(3)
        try:
            while self.keep_running():
                step_msg = self.step()
                if step_msg is not None:
                    self.user.tell(step_msg)
                    break
        except KeyboardInterrupt:
            pass

    def pwrite(self):
        """
        Write out the properties to a file.
        """
        file_nm = self.user.ask("Choose file name: ")
        if self.props is not None:
            self.props.write(file_nm)

    def disp_props(self):
        """
        Display current system properties.
        """
        self.user.tell(self.props.display())

    def disp_log(self):
        """
        Display last 16 lines of log file.
        """

        MAX_LINES = 16

        logfile = self.props.get_logfile()

        if logfile is None:
            self.user.tell("No log file to examine!")

        last_n_lines = deque(maxlen=MAX_LINES)  # for now hard-coded

        with open(logfile, 'rt') as log:
            for line in log:
                last_n_lines.append(line)

        self.user.tell("Displaying the last " + str(MAX_LINES)
                       + " lines of logfile " + logfile)
        for line in last_n_lines:
            self.user.tell(line.strip())

    def step(self):
        """
        Step period-by-period through agent actions.
        """
        self.census(disp=self.disp_census)

        self.period += 1

# agents might be waiting to be born
        if self.womb is not None:
            for agent in self.womb:
                self.add_agent(agent)
            del self.womb[:]

# there might be state-setting to do before acting
        if self.preact:
            self.preact_loop()

# now have everyone act in random order
        self.act_loop()

# there might be cleanup to do after acting
        if self.postact:
            self.postact_loop()

    def act_loop(self):
        """
        Loop through randomly through agents calling their act() func.
        """
        for agent in self.agents.agent_random_iter():
            agent.act()

    def preact_loop(self):
        """
        Loop through agents calling their preact() func.
        """
        for agent in self.agents:
            agent.preact()

    def postact_loop(self):
        """
        Loop through agents calling their postact() func.
        """
        for agent in self.agents:
            agent.postact()

    def draw_graph(self):
        """
        Draw a graph!
        """
        choice = self.user.ask_for_ltr("Draw graph for "
                                       + "(a)gents; (e)nvironment; "
                                       + "(u)niversals?")
        if choice == "a":
            self.agents.draw()
        elif choice == "u":
            node.universals.draw()
        else:
            self.draw()

    def graph_agents(self):
        """
        Draw a graph of the agent relationships.
        """
        self.agents.draw()

    def graph_env(self):
        """
        Draw a graph of the env's relationships.
        """
        self.draw()

    def graph_unv(self):
        """
        Draw a graph of the universal relationships.
        """
        node.universals.draw()

    def keep_running(self):
        """
        Placeholder
        """
        return True

    def view_pop(self):
        """
        Graph our population levels.
        """
        if self.period < 4:
            self.user.tell("Too little data to display")
            return

        pop_hist = self.agents.get_pop_hist()

        disp.display_line_graph('Populations in '
                                + self.name,
                                pop_hist,
                                self.period)

    def plot(self):
        """
        Placeholder
        """
        self.user.tell("Plot not implemented in this model")

    def quit(self):
        """
        Leave this run.
        """
        self.user.tell("Returning to runtime environment.")
        sys.exit(0)

    def contains(self, agent_type):
        """
        Do we have this sort of thing in our env?
        """
        return self.agents.contains(agent_type)

    def census(self, disp=True):
        """
        Take a census of what is in the env.
        """
        results = self.agents.census()
        if disp:
            self.user.tell("Populations in period "
                           + str(self.period) + ":")
            self.user.tell(results)

    def get_pop(self, var):
        """
        Return the population of variety 'var'
        """
        return self.agents.get_pop(var)

    def get_my_pop(self, agent):
        """
        Return the population of agent's type
        """
        return self.agents.get_my_pop(agent)
