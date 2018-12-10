"""
ASCII based features and impl.
"""

import numpy as np

import gym
from gym import error, spaces, utils, core
from gym.utils import seeding
from gym.envs.registration import register
from six import StringIO
import math
import sys

class RubiksCube(gym.Env):

    """
    # Set this in SOME subclasses
    metadata = {'render.modes': []}
    reward_range = (-np.inf, np.inf)
    spec = None


    # Set these in ALL subclasses
    action_space = None
    observation_space = None

    """

    metadata = {'render.modes': ["human", 'ansi']}
    action_list = ['left','right']#,'leftskip','rightskip']


    def __init__(self,dim=2):
        #empty function

    def _reset(self):
        #empty function

    def _render(self, mode='human',close=False):
        outfile = StringIO() if mode == 'ansi' else sys.stdout

        lstholder = self.to_liststring();
        outfile.write(''.join(lstholder));
        outfile.write("\n");

        # No need to return anything for human
        if mode != 'human':
            return outfile

        #TODO ansi mode is not working yet since StringIO is not used correctly

    def _seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def _close(self):
        del action_space;

    """Run one timestep of the environment's dynamics. When end of
    episode is reached, you are responsible for calling `reset()`
    to reset this environment's state.

    Accepts an action and returns a tuple (observation, reward, done, info).

    Args:
        action (object): an action provided by the environment

    Returns:
        observation (object): agent's observation of the current environment
        reward (float) : amount of reward returned after previous action
        done (boolean): whether the episode has ended, in which case further step() calls will return undefined results
        info (dict): contains auxiliary diagnostic information (helpful for debugging, and sometimes learning)
    """
    def _step(self, action_value):
        #empty function

class RubiksCube3x3(RubiksCube):

    def __init__(self):
        super(RubiksCube3x3, self).__init__(dim=3)
