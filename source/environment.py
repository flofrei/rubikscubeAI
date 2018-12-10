# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np

class Environment(object):
  # cached action size
  action_size = -1
  feature_size_1 = -1;
  feature_size_2 = -1;  
  
  @staticmethod
  def create_environment(env_type, env_name):
    if env_type == 'gym':
      from gym_environment import GymEnvironment
      return GymEnvironment(env_name)
    else:
        print("Something terribly gone wrong with env_type in creating env");
  
  @staticmethod
  def get_action_size(env_type, env_name):
    #if Environment.action_size >= 0:
     #print("Why are you falling into action_size>=0 branch??")
      #return Environment.action_size

    if env_type == "gym":
      from gym_environment import GymEnvironment 
      Environment.action_size, Environment.feature_size_1,Environment.feature_size_2  = \
        GymEnvironment.get_action_size(env_name)
    else:
        print("Something terribly gone wrong with env_type in getting action_size");
    return Environment.action_size,Environment.feature_size_1,Environment.feature_size_2 

  def __init__(self):
    pass

  def process(self, action):
    pass

  def reset(self):
    pass

  def stop(self):
    pass  

  def render(self):
    pass
