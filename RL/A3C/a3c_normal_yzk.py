import gym
import itertools
import numpy as np
import os
import random
import sys
import tensorflow as tf
import multiprocessing
import threading
# Learning from Movan

GAME = 'Pendulum-v0'
# env = gym.make(GAME).unwrapped
env = gym.make(GAME)
N_S = env.observation_space.shape[0]
N_A = env.action_space.shape[0]
A_BOUND = [env.action_space.low, env.action_space.high]
ENTROPY_BETA = 0.01

class  ACNet():
	def __init__(self,scope,globalAC = None):
		if scope == 'global_net':
			with tf.variable_scope(scope):
				self.s = tf.placeholder(tf.float32, [None,N_S], name = 's')
				self.a_params, self.c_params = self._build_network(scope)[-2:]
		else:
			with tf.variable_scope(scope):
				self.s = tf.placeholder(tf.float32, [None,N_S], name = 's')
				self.a_his = tf.placeholder(tf.float32, [None,N_A], name = 'a_his')
				self.v_target = tf.placeholder(tf.float32, [None,1],name = 'v_target')
				mu, sigma ,self.v , self.a_params, self.c_params = self._build_network(scope)
				td = tf.subtract(self.v_target, self.v,name = 'TD_error')
				with tf.name_scope('c_loss'):
					self.c_loss = tf.reduce_mean(tf.square(td))
				with tf.name_scope('wrap_a_out'):
					mu, sigma = mu*A_BOUND[1], sigma + 1e-4

				norm_dist = tf.distributions.Normal(mu,sigma)
				with tf.name_scope('a_loss'):
					entropy = norm_dist.entropy()
					a_prob = norm_dist.log_prob(self.a_his)
					self.exp_v = a_prob*tf.stop_gradient(td) + entropy*ENTROPY_BETA
					self.a_loss = tf.reduce_mean(-self.exp_v)
				with tf.name_scope('local_grad'):
					self.a_grad = tf.gradients(self.a_loss, self.a_params)
					self.c_grad = tf.gradients(self.c_loss, self.c_params)
				with tf.name_scope('choose_a'):
					self.a_choose = tf.clip_by_value(tf.squeeze(norm_dist.sample(1), axis=[0, 1]), A_BOUND[0], A_BOUND[1])
				with tf.name_scope('sync'):
					with tf.name_scope('push'):
						self.update_a_op = OPT_A.apply_gradients(zip(self.a_grad, globalAC.a_params))
						self.update_c_op = OPT_C.apply_gradients(zip(self.c_grad, globalAC.c_params))
					with tf.name_scope('pull'):
						self.pull_a_op = [ l_a.assign(g_a) for l_a, g_a in zip(self.a_params, globalAC.a_params)]
						self.pull_c_op = [l_c.assign(g_c) for l_c, g_c in zip(self.c_params, globalAC.c_params)]

	def _build_network(self,scope):
		"""
			Continous Envirnment
		"""
		w_init = tf.random_normal_initializer(0., .1)
		with tf.variable_scope('actor_net'):
			l_a = tf.layers.dense(self.s,200,tf.nn.relu6, kernel_initializer = w_init, name = 'la')
			mu = tf.layers.dense(l_a,N_A,tf.nn.tanh, kernel_initializer = w_init, name = 'mu')
			sigma = tf.layers.dense(l_a,N_A,tf.nn.softplus, kernel_initializer = w_init, name = 'sigma')
		with tf.variable_scope('critic_net'):
			l_c = tf.layers.dense(self.s, 100,tf.nn.relu6, kernel_initializer = w_init, name = 'lc')
			v = tf.layers.dense(l_c,1,kernel_initializer = w_init,name = 'v')
		a_params = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope = scope +'/actor_net')
		c_params = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope = scope + '/critic_net')
		return mu, sigma, v ,a_params, c_params

	def update_global(self,feed_dict):
		SESS.run([self.update_a_op,self.update_c_op], feed_dict)

	def pull_global(self):
		SESS.run([self.pull_a_op, self.pull_c_op])

	def choose_action(self,s):
		s = s[np.newaxis,:]
		return SESS.run(self.a_choose,{self.s:s})

MAX_GLOBAL_STEP = 2000
MAX_EPISODE_STEP = 200
UPDATE_GLOBAL_ITER = 10
GLOABL_REWARD_R = []
GLOBAL_EP = 0
GAMMA = 0.9

class Worker():
	def __init__(self,name,globalAC):
		self.env = gym.make(GAME).unwrapped
		self.name = name 
		self.ACNet = ACNet(self.name, globalAC)
	def work(self):
		total_step = 1
		buffer_s, buffer_a, buffer_r = [], [], []
		global GLOBAL_EP, GLOABL_REWARD_R
		while not COORD.should_stop() and GLOBAL_EP < MAX_GLOBAL_STEP:
			ep_r = 0
			s = self.env.reset()
			for ep_t in range(MAX_EPISODE_STEP):
				if self.name == 'W_0':
					self.env.render()
				a = self.ACNet.choose_action(s)
				s_ , r, done, info = self.env.step(a)
				ep_r += r
				done = True if ep_t == MAX_EPISODE_STEP -1 else False
				buffer_s.append(s)
				buffer_a.append(a)
				buffer_r.append((r+8)/8)
				if total_step % UPDATE_GLOBAL_ITER ==0 or done:
					if done:
						v_s_ = 0
					else:
						v_s_ = SESS.run(self.ACNet.v, {self.ACNet.s:s_[np.newaxis,:]})[0,0]
					buffer_v_target = []
					for item in buffer_r[::-1]:
						v_s_  = v_s_*GAMMA + item
						buffer_v_target.append(v_s_)
					buffer_v_target.reverse()
					buffer_s, buffer_a, buffer_v_target = np.vstack(buffer_s), np.vstack(buffer_a),np.vstack(buffer_v_target)
					feed_dict = {
						self.ACNet.s:buffer_s,
						self.ACNet.a_his:buffer_a,
						self.ACNet.v_target:buffer_v_target
					}
					self.ACNet.update_global(feed_dict)
					buffer_a,buffer_s,buffer_r = [],[],[]
					self.ACNet.pull_global()
	
				total_step += 1
				s = s_
				if done:
					if len(GLOABL_REWARD_R) == 0:
						GLOABL_REWARD_R.append(ep_r)
					else:
						GLOABL_REWARD_R.append(GLOABL_REWARD_R[-1]*0.9 + 0.1*ep_r)
					print(self.name, "EP:",GLOBAL_EP, "Reward:", GLOABL_REWARD_R[-1])
					GLOBAL_EP +=1    
					break

if __name__ == '__main__':
	LR_A = 0.0001
	LR_C = 0.001
	# SESS = tf.Session()
	SESS  = tf.Session(config=tf.ConfigProto(log_device_placement=True))
	N_WORKERS = multiprocessing.cpu_count()
	with tf.device("/gpu:0"):
		OPT_A = tf.train.RMSPropOptimizer(LR_A, name='RMSPropA')
		OPT_C = tf.train.RMSPropOptimizer(LR_C, name='RMSPropC')
		GLOBAL_AC = ACNet('global_net')  # we only need its params
		workers = []
        # Create worker
		for i in range(N_WORKERS):
			i_name = 'W_%i' % i   # worker name
			workers.append(Worker(i_name, GLOBAL_AC))
	COORD = tf.train.Coordinator()
	SESS.run(tf.global_variables_initializer())

	worker_threads = []
	for worker in workers:
		job = lambda: worker.work()
		t = threading.Thread(target=job)
		t.start()
		worker_threads.append(t)
	COORD.join(worker_threads)

	import matplotlib.pyplot as plt
	plt.plot(np.arange(len(GLOABL_REWARD_R)), GLOABL_REWARD_R)
	plt.xlabel('step')
	plt.ylabel('Total moving reward')
	plt.show()




