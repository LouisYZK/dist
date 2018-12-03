"""
	Time: Dec.3 ,2018
	Author: YZK
	Using:
		gym
		tensorflow
	describe:
		Deep Reinforcement Learning Method
"""

import numpy as np
import pandas as pd
import tensorflow as tf

class DeepQNetwork():
	def __init__(
			self,
			n_features,
			n_actions,
			learning_rate = 0.01,
			reward_decay = 0.9,
			e_greedy = 0.9,
			replace_target_iter = 300,
			memory_size = 300,
			batch_size = 32,
			e_greedy_increment = None,
			output_graph = False
		):
		self.n_features = n_features
		self.n_actions = n_actions
		self.lr = learning_rate
		self.gamma = reward_decay
		self.epsilon_max = e_greedy
		self.replace_target_iter = replace_target_iter
		self.memory_size = memory_size
		self.batch_size = batch_size
		self.epsilon = 0 if e_greedy_increment is not None else self.epsilon_max

		self.learn_step_counter = 0

		# size: [s, a,r,s_] ? n_fetures is States'dim ,but is here assuming that Action's dim is 1 ?
		self.memory = np.zeros((self.memory_size, 2*n_features +2 ))

		self._build_network()
		self.e_params = tf.get_collection('eval_net_params')
		self.t_params = tf.get_collection('target_net_params')

		self.replace_target_op = [tf.assign(t,e) for t,e in zip(self.t_params, self.e_params)]

		self.sess = tf.Session()
		if output_graph:
			tf.summary.FilerWriter('./logs/',self.sess.graph)

		self.sess.run(tf.global_variables_initializer())
		self.cost_his = []

	def _build_network(self):
		self.s = tf.placeholder(tf.float32, [None, self.n_features], name = 's')
		self.q_target = tf.placeholder(tf.float32, [None, self.n_actions], name = 'v_target')
		n_l1, w_init, b_init = 10, tf.random_normal_initializer(0., .3), tf.constant_initializer(0.1)
		with tf.variable_scope('eval_net'):
			c_names = ['eval_net_params', tf.GraphKeys.GLOBAL_VARIABLES]
			with tf.variable_scope('l1'):
				w1 = tf.get_variable('w1',[self.n_features,n_l1], initializer = w_init, collections = c_names)
				b1 = tf.get_variable('b1',[1, n_l1], initializer = b_init, collections = c_names)
				l1 = tf.nn.relu(tf.matmul(self.s, w1) + b1)
			with tf.variable_scope('l2'):
				w2 = tf.get_variable('w2',[n_l1, self.n_actions], initializer = w_init, collections = c_names)
				b2 = tf.get_variable('b2',[1, self.n_actions], initializer = b_init, collections = c_names)
				self.q_eval = tf.matmul(l1, w2) + b2

		with tf.variable_scope('loss'):
			self.loss = tf.reduce_mean(tf.squared_difference(self.q_target,self.q_eval))

		with tf.variable_scope('train'):
			self._tain_op = tf.train.RMSPropOptimizer(self.lr).minimize(self.loss)

		self.s_ = tf.placeholder(tf.float32, [None, self.n_features], name = 's_')
		with tf.variable_scope('target_net'):
			c_names = ['target_net_params', tf.GraphKeys.GLOBAL_VARIABLES]
			with tf.variable_scope('l1'):
				w1 = tf.get_variable('w1',[self.n_features, n_l1],initializer = w_init, collections = c_names)
				b1 = tf.get_variable('b1',[1, n_l1],initializer = b_init, collections = c_names)
				l1 = tf.nn.relu(tf.matmul(self.s_, w1) + b1)
			with tf.variable_scope('l2'):
				w2 = tf.get_variable('w2',[n_l1, self.n_actions],initializer = w_init, collections = c_names)
				b2 = tf.get_variable('b2',[1, self.n_actions],initializer = b_init, collections = c_names)
				self.q_next = tf.matmul(l1, w2) + b2

	def store_transitions(self, s, a, r, s_):
		if not hasattr(self, 'memory_counter'):
			self.memory_counter = 0
		transition = np.hstack((s,[a,r],s_))

		ind = self.memory_counter % self.memory_size
		self.memory[ind,:] = transition

		self.memory_counter +=1

	def choose_action(self, obseravtion):
		obseravtion = obseravtion[np.newaxis, :]
		if np.random.uniform() < self.epsilon:
			action_value = self.sess.run(self.q_eval, feed_dict = {self.s:obseravtion})
			action = np.argmax(action_value)
		else:
			action = np.random.randint(0,self.n_actions)
		return action

	def learn(self):
		if self.learn_step % self.replacte_target_iter == 0:
			self.sess.run(self.replace_target_op)
			print('\n target_net params were updated \n')

		if self.memory_counter > self.memory_size:
			sample_ind = np.random.choice(self.memory_size, size = self.batch_size)
		else:
			sample_ind = np.random.choice(self.memory_counter, size = self.bacth_size)
		batch_memory = self.memory[sample_ind,:]

		q_next ,q_eval = self.sess.run(
				[self.q_next, self.q_eval],
				feed_dict ={
					self.s:batch_memory[:,:self.n_features],
					self.s_:batch_memory[:,-self.n_features:]
				}
			)

		q_target = q_eval.copy()

		batch_ind = np.arange(self.batch_size)
		eval_action_ind = batch_memory[:, self.n_features].astype(int)
		reward = batch_memory[:,self.n_features +1]

		q_target[batch_ind, eval_action_ind] = reward + self.gamma* np.max(q_next,axis = 1)

		_, self.cost = self.sess.run([self._train_op, self.loss], feed_dict = {self.s:batch_memory[:,:self.n_features], self.q_target:q_target})

		self.cost_his.append(self.cost)

		self.epsilon = self.epsilon + self.epsilon_increment if self.epsilon < self.epsilon_max else self.epsilon_max
		self.learn_step_counter += 1

import gym

if __name__ == '__main__':
	env = gym.make('CartPole-v0')
	env = env.unwrapped

	RL = DeepQNetwork(env.observation_space.shape[0], env.action_space.n,learning_rate = 0.01, e_greedy = 0.9,replace_target_iter = 100, memory_size = 2000, e_greedy_increment = 0.001)
	total_steps = 0

	n_episode = 100
	for i in range(n_episode):
		while True:
			observation = env.reset()
			ep_r = 0

			action = RL.choose_action(observation)
			observation_, r , done, info = env.step(action)

			x, x_dot, theta, theta_dot = observation_
			r1 = (env.x_threshold - abs(x))/env.x_threshold - 0.8
			r2 = (env.theta_threshold_radians - abs(theta))/env.theta_threshold_radians - 0.5
			reward = r1 + r2

			RL.store_transitions(observation, action, reward, observation_)

			ep_r += r
		if total_steps > 1000:
			RL.learn()

			if done:
				print('episode: ', i_episode,
					'ep_r: ', round(ep_r, 2),
					' epsilon: ', round(RL.epsilon, 2))
				break
			observation = observation_

			total_steps += 1


