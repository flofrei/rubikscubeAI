#import logging
from gym.envs.registration import register

#logger = logging.getLogger(__name__)

register(
    id='RubiksCube3x3-v0',
    entry_point='gym_3drubikscube.envs:RubiksCube3x3',
    timestep_limit=100,
)
