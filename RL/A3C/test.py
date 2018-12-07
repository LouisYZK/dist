import tensorflow as tf
import numpy as np 
with tf.variable_scope('global'):
    s = tf.placeholder(tf.float32, [None, 10], name = 's')
    l1 = tf.layers.dense(s, 100, name = 'l1')
    out = tf.layers.dense(l1, 1, name = 'out')

with tf.variable_scope('local'):
    # g_params = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope = 'global')
    lo1 = tf.placeholder(tf.float32, [None, 10], name = 'lo1')
    with tf.name_scope('local_net'):
        local_const = tf.constant(0.)

with tf.Session() as sess:
    S = np.random.rand(50,10)
    g_params = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope = 'global')
    sess.run(tf.global_variables_initializer())
    # print(sess.run(out, {s:S}))
    res = sess.run(g_params)
    # print(res[3])
    # l_params = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope ='local') 
    # res = sess.run(l_params,{lo1:np.random.rand(1,10)})
    print(res)
    # print('')
