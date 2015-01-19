"""
spatial_model.py
You can clone this file and its companion spatial_run.py
to easily get started on a new spatial model.
It also is a handy tool to have around for testing
new features added to the base system.
"""
import spatial_agent as sa


class TestSpatialAgent(sa.MobileAgent):
    """
    An agent that just prints where it is when asked to act
    """

    def act(self):
        print(sa.pos_msg(self, self.pos))


