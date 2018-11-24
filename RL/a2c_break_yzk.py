import gym
from gym.wrappers import Monitor
import itertools
import numpy as np
import os
import random
import sys
import psutil
import tensorflow as tf

from collections import deque, namedtuple
from matplotlib import pyplot as plt

env = gym.make('Breakout-v0')
env.seed(1)  # reproducible
env = env.unwrapped

class StateProcessor():
    """
    Processes a raw Atari iamges. Resizes it and converts it to grayscale.
    图片的预处理。
    """
    def __init__(self):
        # Build the Tensorflow graph
        with tf.variable_scope("state_processor"):
            self.input_state = tf.placeholder(shape=[210, 160, 3], dtype=tf.uint8)
            self.output = tf.image.rgb_to_grayscale(self.input_state)
            self.output = tf.image.crop_to_bounding_box(self.output, 34, 0, 160, 160)
            self.output = tf.image.resize_images(
                self.output, [84, 84], method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
            self.output = tf.squeeze(self.output)

    def process(self, sess, state):
        """
        Args:
            sess: A Tensorflow session object
            state: A [210, 160, 3] Atari RGB State

        Returns:
            A processed [84, 84, 1] state representing grayscale values.
        """
        return sess.run(self.output, { self.input_state: state })

def build_convolutional_network(X,output_units):
	# two convolutional layers
	# X  shape [84,84,1]
	conv1 = tf.layers.conv2d(
		inputs = X, 
		filters = 64, 
		kernel_size = [4,4], 
		padding = "same",
		activation = tf.nn.relu, 
		name = "conv1"
	)
	pool1 = tf.layers.max_pooling2d(
		inputs = conv1, 
		pool_size = [2, 2], 
		strides = 2
	)
	conv2 = tf.layers.conv2d(
		pool1, 
		filters = 32, 
		kernel_size = [4,4], 
		padding = "same",
		activation = tf.nn.relu, 
		name = "conv2"
	)
	pool2 = tf.layers.max_pooling2d(
		inputs = conv2, 
		pool_size = [2, 2], 
		strides = 2
	)
  # Fully connected layer
	fc1 = tf.layers.dense(
		inputs = tf.layers.flatten(pool2),
		units = output_units, # action number
		activation = tf.nn.relu,
		name = "fc1")
	return fc1

class Actor(object):
    def __init__(self, sess, image_shape, lr=0.001):
        self.sess = sess

        self.s = tf.placeholder(tf.float32, image_shape, "state")
        self.a = tf.placeholder(tf.float32, [None,4], name="act")
        self.td_error = tf.placeholder(tf.float32, None, name="td_error")  # TD_error

        with tf.variable_scope('Actor'):
        	self.action_prob = build_convolutional_network(self.s,output_units = 4)

        with tf.variable_scope('exp_v'):
            log_prob = tf.log(self.action_prob)        #selecte the action prob value
            # advantage (TD_error) guided loss
            self.exp_v = tf.reduce_mean(log_prob * self.td_error)
        with tf.variable_scope('train'):
            self.train_op = tf.train.AdamOptimizer(lr).minimize(-self.exp_v)  # minimize(-exp_v) = maximize(exp_v)

    def learn(self, s, a, td):
        feed_dict = {self.s: s, self.a: a, self.td_error: td}  
        #td temproal difference 由 critic net产生
        _, exp_v = self.sess.run([self.train_op, self.exp_v], feed_dict)  #优化
        return exp_v  

    def choose_action(self, s):
        probs = self.sess.run(self.action_prob, {self.s: s})   
        # get probabilities for all actions
        return np.random.choice(np.arange(probs.shape[1]), p=probs.ravel())   
        # return a int 以某种概率选择动作

class Critic(object):
    def __init__(self, sess, image_shape, lr=0.01):
        self.sess = sess
        self.s = tf.placeholder(tf.float32,image_shape, "state")   
        #critic net input 当前状态
        self.v_ = tf.placeholder(tf.float32, [1, 1], "v_next")         #下一状态对应的value 值
        self.r = tf.placeholder(tf.float32, None, 'r')                  #当前状态执行动作后的奖励值

        with tf.variable_scope('Critic'):                           
        #构建critic 网络，注意输出一个值表示当前value
            self.v = build_convolutional_network(self.s,output_units = 1)

        with tf.variable_scope('squared_TD_error'):
            self.td_error = self.r + GAMMA * self.v_ - self.v   #贝尔慢迭代公式 求TD-error
            self.loss = tf.square(self.td_error)    # TD_error = (r+gamma*V_next) - V_eval
        
        with tf.variable_scope('train'):
            self.train_op = tf.train.AdamOptimizer(lr).minimize(self.loss)

    def learn(self, s, r, s_):      #critic net的学习算法
        v_ = self.sess.run(self.v, {self.s: s_})    #下一状态输入到网络获取下一状态的q值
        td_error, _ = self.sess.run([self.td_error, self.train_op],    
                                          {self.s: s, self.v_: v_, self.r: r})  #当前状态下输入获取当前状态q值
        return td_error

sess = tf.Session()

OUTPUT_GRAPH = False # 是否保存模型（网络结构）
MAX_EPISODE = 3000
DISPLAY_REWARD_THRESHOLD = 200  # renders environment if total episode reward is greater then this threshold
MAX_EP_STEPS = 100000   # maximum time step in one episode
RENDER = True  # rendering wastes time
GAMMA = 0.9     # reward discount in TD error
LR_A = 0.01    # learning rate for actor
LR_C = 0.1     # learning rate for critic

actor = Actor(sess, [None,84,84,1], lr=LR_A)
critic = Critic(sess, [None,84,84,1], lr=LR_C)  

sess.run(tf.global_variables_initializer())

state_proess = StateProcessor()

for i_episode in range(MAX_EPISODE):
    s = env.reset()
    s = state_proess.process(sess,s)
    t = 0
    track_r = []
    while True:
        if RENDER: env.render()

        a = actor.choose_action(s)

        s_, r, done, info = env.step(a)

        if done: r = -20

        track_r.append(r)

        td_error = critic.learn(s, r, s_)  # gradient = grad[r + gamma * V(s_) - V(s)]
        actor.learn(s, a, td_error)     # true_gradient = grad[logPi(s,a) * td_error]

        s = s_
        t += 1

        if done or t >= MAX_EP_STEPS:
            ep_rs_sum = sum(track_r)

            if 'running_reward' not in globals():
                running_reward = ep_rs_sum
            else:
                running_reward = running_reward * 0.95 + ep_rs_sum * 0.05
            if running_reward > DISPLAY_REWARD_THRESHOLD: RENDER = True  # rendering
            print("episode:", i_episode, "  reward:", int(running_reward))
            break