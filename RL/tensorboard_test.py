import numpy as np
import tensorflow as tf 

tf.set_random_seed(1)
np.random.seed(1)
# fake data
data_x = np.linspace(-1,1,100)[:,np.newaxis] # shape = [100,1] 其中100是指100个样本，1是指1个单元（维度）
noise = np.random.normal(0,0.1,size = data_x.shape)
data_y = np.power(data_x,2) + noise

# plt.scatter(data_x,data_y)
# plt.show()

# 定义网络参数
with tf.variable_scope('Inputs'):
    tf_xx = tf.placeholder(tf.float32,shape = data_x.shape,name = 'X')
    tf_yy = tf.placeholder(tf.float32,shape = data_y.shape,name = 'Y')

# 网络结构
with tf.variable_scope('Net'):
    ll = tf.layers.dense(tf_xx, 10, tf.nn.relu, name='hidden_layer') # 自定义隐藏层的单元数
    output = tf.layers.dense(ll,1,activation=None,name = 'output_layer') # 输出层的单元数必须是维度
    
#     统计
    tf.summary.histogram('hidden1',ll)
    tf.summary.histogram('output',output)

loss = tf.losses.mean_squared_error(tf_yy,output,scope='loss')
optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.5)
train_op = optimizer.minimize(loss)

tf.summary.scalar('loss',loss)

sess = tf.Session()                                 # control training and others
sess.run(tf.global_variables_initializer())

writer = tf.summary.FileWriter('./log/example',sess.graph)
merge_op = tf.summary.merge_all()

for step in range(300):
    _ , res = sess.run([train_op,merge_op],{tf_xx:data_x,tf_yy:data_y})
    writer.add_summary(res,step)

# tensorboard --logdir path/to/log