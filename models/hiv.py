
import random
import indra.markov_agent as ma
import indra.markov_env as menv

NSTATES = 4

avg_coupling_tendency = 5 # 0-10
avg_commitment = 20 # 0-200
avg_condom_use = 5 # 0-10
avg_test_frequency = 1 # 0-2

infection_chance = 50 # 0-100
symptoms_show = 200

class neg(ma.MarkovAgent):
    """
        An HIV-negative individual
    """
    def __init__(self, name, init_state, max_detect=1, coupling_tendency, commitment, condom_use, test_frequency, coupled, couple_length, partner):
        super().__init__(name, 4, init_state, max_detect=max_detect)
        
        self.coupling_tendency = avg_coupling_tendency
        self.commitment = avg_commitment
        self.condom_use = avg_condom_use
        self.test_frequency = avg_test_frequency

        self.coupled = False
        self.coupled_length = 0
        self.partner = None
    
    def preact(self):
        if self.coupled = True:
            self.coupled_length++

    def act(self):
        if self.coupled = False:
            super().act()
            self.state = self.next_state
            self.move(self.state)
        else:
            self.uncouple()

    def move(self, state):
        x = self.pos[0]
        y = self.pos[1]
        if state == 0:
            if self.env.is_cell_empty(x, y+1):
                self.env.move(self, x,y+1)
        elif state == 1:
            if self.env.is_cell_empty(x, y-1):
                self.env.move(self, x,y-1)
        elif state == 2:
            if self.env.is_cell_empty(x-1, y):
                self.env.move(self, x-1,y)
        else:
            if self.env.is_cell_empty(x+1, y):
                self.env.move(self, x+1,y)
            
    def uncouple(self):
        if (self.couple_length > self.commitment) || (self.couple_length > self.partner.commitment):
            self.coupled = False
            self.couple_length = 0
            self.partner.coupled = False
            self.partner.couple_length = 0
            self.partner.partner = None
            self.partner = None


class poz(neg):
    """
        An HIV-positive individual
    """
    def __init__(self, name, init_state, max_detect=1, coupling_tendency, commitment, condom_use, test_frequency, coupled, couple_length, partner, status_known, infection_length):
        super().__init__(name, init_state, max_detect=1, SPEED, coupling_tendency, commitment, condom_use, test_frequency, coupled, couple_length, partner)
        status_known = False
        infection_length = random.randint(0, symptoms_show - 1)

    def preact(self):
        self.infection_length++
        if self.infection_length > symptoms_show:
            self.status_known = True

    def postact(self):
        if self.coupled = Ture && self.status_known = False:
            self.infect()
        self.test()

    def infect(self):
        if (random.randint(0, 10) > self.condom_use) && (random.randint(0,10) > self.partner.condom_use && random.randint(0, 10) > infection_chance)
            self.partner.converse()

    def converse(self):
        pass

    def test(self):
        if (random.randint(0, 52) < self.test_frequency) && self.status_known == False:
            self.status_known = True


class People(menv.MarkovEnv):
    """
        Individuals wander around randomly when they are not in couples. Upon coming into contact with a suitable partner, there is a chance the two individuals will couple together. When this happens, the two individuals no longer move around, they stand next to each other holding hands as a representation of two people in a sexual relationship.
    """
    def get_pre(self, agent):
        pass

