import gym
import itertools
import numpy as np
import os
import random
import sys
import tensorflow as tf
import multiprocessing
# Learning from Movan

GAME = 'Pendulum-v0'
env = gym.make(GAME)

N_S = env.obeservation_space.shape()[0]
N_A = env.action_space.shape()[0]
A_BOUND = [env.action_scpace.low, env.action_space.high]
ENTROPY_BETA = 0.9

class  ACNect():
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
				mu, sigma ,v , self.a_params, self.c_params = self._build_network(scope)
				td = tf.substract(self.v_target, v)
				with tf.name_scope('c_loss'):
					self.c_loss = tf.reduce_mean(tf.square(td))
				with tf.name_scope('wrap_a_out'):
					mu, sigma = mu*A_BOUND[1], sigma + 1e-8

				norm_dist = tf.distributions.Normal(mu,sigma)
				with tf.name_scope('a_loss'):
					td = tf.stop_gradients(td)
					entropy = norm_dist.entropy()
					a_prob = norm_dist.log_prob(self.a_his)
					exp_v = a_prob*td + entropy*ENTROPY_BETA
					self.a_loss = tf.reduce_mean(exp_v)
				with tf.name_scope('local_grad'):
					self.a_grad = tf.gradients(self.a_loss, self.a_params)
					self.c_grad = tf.gradients(self.c_loss, self.c_params)
				with tf.name_scope('choose_a'):
					self.a_choose = tf.clip_by_value(tf.squeeze(norm_dist.sample(1)),A_BOUND[0],A_BOUND[1])
				with tf.name_scope('sync'):
					with tf.name_scope('push'):
						self.update_a_op = OPT_A.apply_gradients(self.a_grad, globalAC.a_params)
						self.update_c_op = OPT_C.apply_gradients(self.c_grad, globalAC.c_params)
					with tf.name_scope('pull'):
						self.pull_a_op = [ l_a.assign(g_a) for l_a, g_a in zip(self.a_params, globalAC.a_params)]
						self.pull_c_op = [l_c.assign(g_c) for l_c, g_c in zip(self.c_params, globalAC.c_params)]

	def _build_network(self,scope):
		"""
			Continous Envirnment
		"""
		w_init = tf.random_normal_initializer(0.,0.1)
		with tf.variable_scope('actor_net'):
			l_a = tf.layers.dense(self.s,10,kernal_initializer = w_init, name = 'la')
			mu = tf.layers.dense(l_a,N_A,kernal_initializer = w_init, name = 'mu')
			sigma = tf.layers.dense(l_a,N_A,kernal_initializer = w_init, name = 'sigma')
		with tf.variable_scope('critic_net'):
			l_c = tf.layers.dense(self.s, 10,kernal_initializer = w_init, name = 'lc')
			v = tf.layers.dense(l_c,1,kernal_initializer = w_init,name = 'v')
		a_params = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope = scope +'/actor_net')
		c_params = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope = scope + '/critic_net')
		return mu, sigma, v ,a_params, c_params

	def update_global(self,feed_dict):
		SESS.run([self.update_a_op,self.update_c_op], feed_dict)

	def pull_global(self):
		SESS.run([self.pull_a_op, self.pull_c_op])

	def choose_action(self,s):
		SESS.run(self.a_choose,{self.s:s})

MAX_GLOBAL_STEP = 2000
MAX_EPISODE_STEP = 200
UPDATE_GLOBAL_ITER = 10
GLOABL_REWARD_R = []
GLOBAL_EP = 0
GAMMA = 0.9

class Worker():
	def __init__(self,name,globalAC):
		self.env = env # initiate globally
		self.name = name 
		self.ACNet = ACNect(self.name, globalAC)
	def work():
		total_step = 0
		buffer_s, buffer_a, buffer_r = [], [], []
		global GLOBAL_EP, GLOABL_REWARD_R
		while not COORD.should_stop() and total_step < MAX_GLOBAL_STEP:
			ep_r = 0
			s = self.env.reset()
			for ep_t in range(MAX_EPISODE_STEP):
				a = slice.ACNet.choose_action(s)
				s_ , r, done, info = self.env.step(a)
				ep_r += r
				done = True if ep_t == MAX_EPISODE_STEP -1 else False
				buffer_s.append(s_)
				buffer_a.append(a)
				buffer_r.append(r)
				if total_step % UPDATE_GLOBAL_ITER ==0 :
					if done:
						v_s_ = 0
					else:
						v_s = SESS.run(self.ACNet.v, {self.ACNet.s:s_})
					buffer_v_target = []
					for item in r[::-1]:
						v_s += item*GAMMA
						buffer_v_target.append(v_s)
					buffer_v_target.reverse()
					buffer_s, buffer_a, buffer_v_target = np.vstack(buffer_s), np.vstack(buffer_a),np.stack(buffer_v_target)
					feed_dict = {
						self.ACNet.s:buffer_s,
						self.ACNet.a_his:buffer_a,
						self.ACNet.v_target:buffer_v_target
					}
					self.ACNet.update_global(feed_dict)
					self.ACNet.pull_global()
					buffer_a,buffer_s,buffer_r = [],[],[]
				total_step += 1
				s = s_
				if done:
					if len(GLOABL_REWARD_R) == 0:
						GLOABL_REWARD_R.append(ep_r)
					else:
						GLOABL_REWARD_R.append(GLOABL_REWARD_R[-1]*0.9 + 0.1*ep_r)
					print(self.name, "EP:",GLOBAL_EP, "Reward:", GLOABL_REWARD_R[-1])
					GLOBAL_EP +=1 

if __name__ == '__main__':
	SESS = tf.Session()
	NUM_WORKERS = multiprocessing.cpu_count()
	workers = []
	globalAC = ACNect('global_net')
	for i in range(NUM_WORKERS):
		worker = Worker('worker_{}'.format(i), globalAC)
		workers.append(worker)
	COORD = tf.coordinator()
	threads = []
	for worker in workers:
		job = lambda: worker.work()
		t = thread.Threading(target = job)
		threads.append(t)
	COORD.join(threads)

	# plot
	plt.plot(np.arange(len(GLOBAL_EP)),GLOABL_REWARD_R)
	plt.show()



