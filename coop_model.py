# -*- coding: utf-8 -*-
"""
Created on Tue Nov 11 21:13:15 2014

@author: Brandon
"""

import sitter_agent
num_agents = 10


env = sitter_agent.CoopEnv()


for i in range(num_agents):
    env.add_agent(sitter_agent.Member('Steve' + str(i), i+1))

env.run()
