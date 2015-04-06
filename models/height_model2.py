"""
Filename: height_agent.py
Author: Gene Callahan and Brandon Logan
"""

import indra.entity as ent
import indra.env as env
import random
import indra.display_methods as disp

REPRODUCE = "reproduce"
ENV_NM = "Schelling height model"
DEF_HEIGHT = 1.0


class HeightAgent(ent.Agent):

    def __init__(self, name, height):
        super().__init__(name, REPRODUCE)
        self.height = height
        self.alive = True
        self.mychild = None
        #print('adding agent with name ' + self.name)

    def act(self):
        #super().act()
        self.reproduce()
        self.alive = False

    def reproduce(self):
        self.mychild = HeightAgent(self.name + str(self.env.period), random.gauss(self.height, self.height/4))

        self.env.add_child(self.mychild)
        #print('adding to womb ')

class HeightAgentEng(HeightAgent):

    def __init__(self, name, height):
        super().__init__(name, height)
    #def gen_height(self):
        #new_height = random.uniform(self.height-self.height/4,self.height+self.height/4)


    def reproduce(self):
        self.mychild = HeightAgentEng(self.name + str(self.env.period), random.gauss(self.height, self.height/4))

        self.env.add_child(self.mychild)

        #print(self.env.step(self.total_height))
        runt_height = .67 * self.env.cur_avg_height
        if self.mychild.height < runt_height:
            #print('changing agent ' + self.mychild.name + ' height from ' + str(self.mychild.height) + ' to ' + str(runt_height))
            self.mychild.height = runt_height

class HeightEnv(env.Environment):

    """ This class creates an environment for Schelling height agents """


    def __init__(self, model_nm = None):
        super().__init__( "Height Environment", model_nm=model_nm, preact=True)
        self.cur_avg_height = 0
        
    def census(self, disp=True):                                                        
        """                                                                             
        Take a census of our pops.                                                      
        """                                                                             
        self.user.tell("Average heights in period " + str(self.period))                        
        for var in self.agents.varieties_iter():                                        
            total_height = 0                                                              
            i = 0                                                                       
        for agent in self.agents.variety_iter(var):                                 
            total_height += agent.height                                               
            i += 1                                                                  
        avg_height = total_height / i                                                 
        self.agents.append_pop_hist(var, avg_height)                                
        self.user.tell(var + ": " + str(avg_height))                                
                                                                                    
    def view_pop(self):                                                                 
        """                                                                             
        Draw a graph of our changing pops.                                              
        """                                                                             
        if self.period < 4:                                                             
            self.user.tell("Too little data to display")                                
            return                                                                      
                                                                                    
        (period, data) = self.line_data()                                               
        self.line_graph = disp.LineGraph("Schelling's height model",                    
                                     data, period, anim=False)                          
    def preact_loop(self):
        total_height = 0
        for agent in reversed(self.agents):
            if agent.alive:
                total_height += agent.height
            else:
#                print ( agent.name + ' with a height of ' + str(agent.height))
                self.agents.remove(agent)
        self.cur_avg_height = total_height / len(self.agents)
<<<<<<< HEAD
      
=======
        self.height_hist.append(self.cur_avg_height)
        print ('Average height period ' + str(self.period) + ' is: ' + str(self.cur_avg_height))
        print(self.height_hist)
#    def display(self):
#
#        if self.period < 4:
#            self.user.tell("Too little data to display")
#            return
#
#
#
#        disp.display_line_graph("Carl Menger's money model: "
#                                + "Trades per good ",
#                                self.height_hist,
#                                self.period)


>>>>>>> origin/master





