import gym
import itertools
import numpy as np
import os
import random
import sys
import psutil
import tensorflow as tf

# Learning from Movan

GAME = 'Pendulum-v0'
env = gym.make(GAME)

N_S = env.obeservation_space.shape()[0]
N_A = env.action_space.shape()[0]
A_BOUND = [env.action_scpace.low, env.action_space.high]

class  