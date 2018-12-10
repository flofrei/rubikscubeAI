# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from multiprocessing import Process, Pipe
import numpy as np
import cv2
import gym
import gym_1dmaze
from copy import copy

from environment import Environment

COMMAND_RESET     = 0
COMMAND_ACTION    = 1
COMMAND_TERMINATE = 2
COMMAND_RENDER    = 3

def worker_with_instance(conn, env_name,env_instance):
  #env = gym.make(env_name)
  #env.reset()
  conn.send(0)
  
  while True:
    command, arg = conn.recv()

    if command == COMMAND_RESET:
      obs = env_instance.reset()
      #state = preprocess_frame(obs)
      conn.send(obs)
    elif command == COMMAND_ACTION:
      reward = 0
      timer = 0
      for i in range(4):
        obs, r, terminal, lst = env_instance.step(arg)
        reward += r
        timer += lst.pop()
        if terminal:
          break
      #state = preprocess_frame(obs)
      conn.send([obs, reward, terminal,timer])
    elif command == COMMAND_RENDER:
      env_instance.render()
      continue
    elif command == COMMAND_TERMINATE:
      break
    else:
      print("bad command: {}".format(command))
  env_instance.close()
  conn.send(0)
  conn.close()

def worker_without_instance(conn, env_name):
  env = gym.make(env_name)
  env.reset()
  conn.send(0)
  
  while True:
    command, arg = conn.recv()

    if command == COMMAND_RESET:
      obs = env.reset()
      #state = preprocess_frame(obs)
      conn.send(obs)
    elif command == COMMAND_ACTION:
      #reward = 0
      #timer = 0
      obs, r, terminal, lst = env.step(arg)
      #timer = lst.pop()
      conn.send([obs, r, terminal,lst])
      #for i in range(4):
      #  obs, r, terminal, lst = env.step(arg)
      #  reward += r
      #  timer += lst.pop()
      #  if terminal:
      #    break
      #state = preprocess_frame(obs)
      #conn.send([obs, reward, terminal,timer])
    elif command == COMMAND_RENDER:
      env.render()
      continue
    elif command == COMMAND_TERMINATE:
      break
    else:
      print("bad command: {}".format(command))
  env.close()
  conn.send(0)
  conn.close()


class GymEnvironment(Environment):
  @staticmethod
  def get_action_size(env_name):
    env = gym.make(env_name)
    action_size = env.action_space.n
    feature_size_1= env.observation_space.shape[0]
    feature_size_2= env.observation_space.shape[1]
    env.close()
    return action_size,feature_size_1,feature_size_2
  
  def __init__(self, env_name):
    Environment.__init__(self)
    self.right_decision = None
    #self.env_instance = gym.make(env_name)
    #self.last_state=self.env_instance.reset()
    self.conn, child_conn = Pipe() ##create a 2way pipe with self.conn=parent and child_conn=child
    self.proc = Process(target=worker_without_instance, args=(child_conn, env_name))
    #self.proc = Process(target=worker_with_instance, args=(child_conn, env_name,self.env_instance))

    #self.last_action = 0
    #self.last_reward = 0

    self.proc.start()
    self.conn.recv()
    self.reset()

  def reset(self):
    self.conn.send([COMMAND_RESET, 0])
    [temp_state,right_decision] = self.conn.recv()
    self.right_decision = np.copy(right_decision)
    self.last_state = np.copy(temp_state) 
    self.last_action = None
    self.last_reward = None

  def stop(self):
    self.conn.send([COMMAND_TERMINATE, 0])
    ret = self.conn.recv()
    self.conn.close()
    self.proc.join()
    print("gym environment stopped")

  def process(self, action):
    self.conn.send([COMMAND_ACTION, action])
    [state, reward, terminal, add_data] = self.conn.recv()
    
    self.last_state = np.copy(state)
    self.last_action = np.copy(action)
    self.last_reward = np.copy(reward)
    return np.copy(state), np.copy(reward), np.copy(terminal), copy(add_data)

  def render(self):
    self.conn.send([COMMAND_RENDER,0])
