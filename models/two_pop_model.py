"""
stance_model.py
Models two classes of agents: one tries to follow the other,
the other tries to avoid the first.
"""
# import logging
import indra.display_methods as disp
import indra.menu as menu
import indra.grid_env as ge
import indra.grid_agent as ga
import indra.prehension as pre


INIT_FLWR = pre.Prehension.X_PRE
INIT_LEDR = pre.Prehension.Y_PRE

STANCE_TRACKED = INIT_FLWR
STANCE_TINDEX = 0  # the index of the tracked stance in an array of stances


class TwoPopAgent(ga.GridAgent):
    """
    An agent taking a stance depending on others' stance.
    """
    def __init__(self, name, goal, max_move, self_import=1):
        super().__init__(name, goal, max_move, max_detect=max_move)
        self.stance = pre.Prehension()
        self.new_stance = pre.Prehension()
        self.other = None
        self.self_import = self_import

    def survey_env(self):
        """
        Look around and see what stances surround us.
        """
        def my_filter(n): return isinstance(n, self.other)

        super().survey_env()
        other_pre = pre.Prehension()
        for other in self.neighbor_iter(view=self.my_view,
                                        filt_func=my_filter):
            other_pre = other.public_stance().prehend(other_pre)
        return other_pre

    def respond_to_cond(self, env_vars=None):
        """
        Over-riding our parent method.
        """
        pass

    def postact(self):
        """
        After we are done acting, adopt our new stance.
        Then move to an empty cell.
        """
        print("With " + type(self).__name__)
        print("old stance = " + str(self.stance))
        print("public old stance = " + str(self.public_stance()))
        print("new stance = " + str(self.new_stance))
        self.new_stance = self.new_stance.normalize()
        self.new_stance = self.new_stance.intensify(self.self_import)
        print("new stance intensified = " + str(self.new_stance),
              "self importance = " + str(self.self_import))
        self.stance = self.new_stance
        print("stance = " + str(self.stance))
        print("")
        self.move_to_empty(grid_view=self.my_view)

    def public_stance(self):
        """
        My stance as seen from outside. Filters out internal conflict.
        """
        return self.stance.direction()


class Follower(TwoPopAgent):
    """
    A trend follower: tries to switch to leader's stance
    """
    def __init__(self, name, goal, max_move, self_import=1):
        super().__init__(name, goal, max_move, self_import)
        self.other = Leader
        self.stance = INIT_FLWR.intensify(self.self_import)

    def eval_env(self, other_pre):
        """
        See how we respond to the stance scene.
        """
        self.new_stance = self.stance.prehend(other_pre)


class Leader(TwoPopAgent):
    """
    A leader: avoids follower's stance.
    """
    def __init__(self, name, goal, max_move, self_import=1):
        super().__init__(name, goal, max_move, self_import)
        self.other = Follower
        self.stance = INIT_LEDR.intensify(self.self_import)

    def eval_env(self, other_pre):
        """
        See how we respond to the stance scene.
        For a leader, we reverse what the followers are doing.
        """
        self.new_stance = self.stance.prehend(other_pre.reverse())


class TwoPopEnv(ge.GridEnv):
    """
    A society of leaders and followers.
    """
    def __init__(self, name, length, height, model_nm=None, torus=False,
                 postact=True):
        super().__init__(name, length, height, model_nm=model_nm,
                         torus=False, postact=postact)
        # sub-models will override these vague names with something
        # meaningful in those models
        self.stances = ["yes", "no"]
        self.line_graph_title = "StanceAgents in %s adopting stance %s"
        self.menu.view.add_menu_item("v",
                                     menu.MenuLeaf("(v)iew populations",
                                                   self.view_pop))

    def census(self, disp=True):
        """
        Take a census of our pops.
        Return the total adopting STANCE_TRACKED.
        """
        total_w_stance = 0
        self.user.tell("Populations in period " + str(self.period) +
                       " adopting " +
                       self.stances[STANCE_TINDEX] + ":")
        for var in self.varieties_iter():
            pop = 0
            for agent in self.get_agents_of_var(var):
                if agent.public_stance().equals(STANCE_TRACKED):
                    pop += 1
            total_w_stance += pop
            self.user.tell(var + ": " + str(pop))
            self.append_pop_hist(var, pop)
        return total_w_stance

    def view_pop(self):
        """
        Draw a graph of our changing pops.
        """
        if self.period < 4:
            self.user.tell("Too little data to display")
            return

        (period, data) = self.line_data()
        self.line_graph = disp.LineGraph(self.line_graph_title
                                         % (self.name,
                                            self.stances[STANCE_TINDEX]),
                                         data, period)
