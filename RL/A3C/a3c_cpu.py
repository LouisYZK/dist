import gym
import itertools
import numpy as np
import os
import random
import sys
import tensorflow as tf
import multiprocessing
import threading

GAME = ''
env = gym.make(GAME)
N_A = env.action_space.shape[0]
N_S = env.observation_space.shape[0]
A_BOUND = [env.observation_space.low, env.observation_space.high]
ENTROPY_BETA = 0.01

class ACNet():
    def __init__(self,scope, globalAC = None):
        if scope == 'global_net':
            with tf.variable_scope('global_net'):
                self.s = tf.placeholder(tf.float32, [None, N_S], name = 's')
                self.a_params ,self.c_params = self._build_network(scope)[-2:]
        else:
            with tf.variable_scope(scope):
                self.s = tf.placeholder(tf.float32, [None, N_S], name = 's')
                self.a_his = tf.placeholder(tf.float32, [None,N_A], name = 'a_his')
                self.v_target = tf.placeholder(tf.float32, [None, 1], name = 'v_target')
                mu, sigma ,v ,self.a_params, self.c_params = self._build_network(scope)
                td = tf.subtract(v, self.v_target)
                with tf.name_scope('c_loss'):
                    self.c_loss = tf.reduce_mean(tf.square(td))
                with tf.name_scope('wrap_a_out'):
                    mu, sigma = mu*A_BOUND[1] , sigma + 1e-4
                norm_dist = tf.distributions.Normal(mu,scale)
                with tf.name_scope('a_loss'):
                    logit = norm_dist.log_prob(self.a_his)
                    entropy = norm_dist.entropy()
                    self.exp_v = logit*tf.stop_gradient(td) + ENTROPY_BETA*entropy
                    self.a_loss = tf.reduce_mean(-self.exp_v)
                with tf.name_scope('choose_a'):
                    self.a_choose = tf.clip_by_value(tf.sqeeze(norm_dist.sample(1)),A_BOUND[0],A_BOUND[1])
                with tf.name_scope('local_grad'):
                    self.a_grad = tf.gradients(self.a_loss, self.a_params)
                    self.c_grad = tf.gradients(self.c_loss, self.c_params)
                with tf.name_scope('sync'):
                    with tf.name_scope('push'):
                        self.update_a_op = OPT_A.apply_gradients(self.a_grad,globalAC.a_params)
                        self.update_c_op = OPT_C.apply_gradients(self.c_grad,globalAC.c_params)
                    with tf.name_scope('pull'):
                        self.pull_a_op = [la.assign(ga) for la,ga in zip(self.a_params, globalAC.a_params)] 
                        self.pull_c_op = [lc.assign(gc) for lc,gc in zip(self.c_params, globalAC.c_params)]               

    def _build_network(scope):
        w_init = tf.random_normal_initializer(0.,.1)
        with tf.variable_scope('actor_net'):
            la = tf.layers.dense(self.s, 200,activation = tf.nn.relu, kernel_initializer= w_init. name = 'la' )
            mu = tf.layers.dense(la, N_A, activation=tf.tanh, kernel_initializer= w_init, name = 'mu')
            sigma = tf.layers.dense(la, N_A, activation= tf.sparse_softmax, kernel_initializer=w_init, name = 'sigma')
        with tf.variable_scope('criti_net'):
            lc = tf.layers.dense(self.s, 100, activation= tf.nn.relu, kernel_initializer= w_init, name = 'lc')
            v = tf.layers.dense(self, N_A, activation=tf.nn.softmax, kernel_initializer= w_init, name = 'v')
        a_params = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope = scope+'/actor_net')
        c_params = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope=scope+'/critic_net')
        return mu, sigma, v, a_params, c_params

        def update_global(self, feed_dict):
            SESS.run([self.update_a_op, self.update_c_op],feed_dict)
        
        def pull_global(self):
            SESS.run([self.pull_a_op, self.pull_c_op])
        
        def choose_action(self, s):
            return SESS.run(self.a_choose, {self.s:s})

MAX_GLOBAL_EP = 2000
MAX_EPISODE = 200
UPDATE_GLOBAL_ITER = 10
GLOBAL_RUNNING_R = []
GLOABL_EP = 0
GAMMA = 0.9
class Worker():
    def __init__(self,name, globalAC):
        self.env = env.make(GAME).unwraps
        self.name = name 
        self.AC = ACNet(name, globalAC=globalAC)
        
    def work():
        total_step = 1
        while not COORD.should_stop() and total_step <MAX_GLOBAL_EP:
            ep_r = 0
            for ep_t in range(MAX_EPISODE):
                buffer_s,buffer_a, buffer_r = [],[],[]
                s = self.env.reset()
                a = self.AC.choose_action(s[np.newaxis,:])
                s_, r, done, info = self.env.step(a)
                ep_r += r
                done = True if ep_t == MAX_EPISODE-1 else False
                buffer_s.append(s)
                buffer_a.append(a)
                buffer_r.append(r)
                if ep_t% UPDATE_GLOBAL_ITER ==0 or done:
                    buffer_v_target = []
                    if done:
                        v_s_ = 0
                    else:
                        v_s_ = SESS.run(self.AC.v, {self.AC.s:s_[np.newaxis,:]})[0,0]
                    for r in buffer_r[::-1]:
                        v_s_ = GAMMA *v_s_ + r 
                        buffer_v_target.append(v_s_)
                    buffer_v_target.reverse()
                    buffer_s, buffer_a,buffer_v_target = np.vstack(buffer_s), np.vstack(buffer_a), np.vstack(buffer_v_target)
                    self.AC.update_global({
                        self.AC.s:buffer_s,
                        self.AC.a_his:buffer_a,
                        self.AC.v_target:buffer_v_target
                    }) 
                    self.AC.pull_global()
                    buffer_s, buffer_a, buffer_r = [],[],[]
                total_step +=1
                s = s_
                if done:
                    if len(GLOBAL_RUNNING_R) ==0:
                        GLOBAL_RUNNING_R.append(ep_r)
                    else:
                        GLOBAL_RUNNING_R.append(GLOBAL_RUNNING_R[-1]*0.9 + 0.1*ep_r)
                    GLOABL_EP +=1
                    print(
                        name, 'EPISODE:',GLOABL_EP, 'REWARD',GLOBAL_RUNNING_R[-1]
                    )

if __name__ == '__main__':
    NUM_WORKERS  = multiprocessing.cpu_count()
    SESS = tf.Session()
    COORD = tf.train.Coordinator()
    with tf.device('/cpu:0'):
        OPT_A = tf.train.RMSPropOptimizer(LR_A)
        OPT_C = tf.train.RMSPropOptimizer(LR_C)
        global_net = ACNet('global_net')
        workers = []
        for i in range(NUM_WORKERS):
            workers.append(Worker('worker_{}'.format(i),globalAC = global_net))
    threads = []
    for worker in workers:
        job = lambda: worker.work()
        t = threading.Thread(target=job)
        t.start()
        threads.append(t)
    SESS.run(tf.global_variables_initializer())
    COORD.join(threads)
    
        




        