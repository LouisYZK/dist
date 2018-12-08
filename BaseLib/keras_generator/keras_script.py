import numpy as np

from keras.models import Sequential
from keras.layers import Dense, Activation
from utils import DataGenerator
from keras.layers import Dense,Dropout,Flatten,Conv2D,MaxPool2D
from keras.optimizers import RMSprop
# Parameters
params = {'dim': (4,9),
          'batch_size': 90,
          'n_classes': 6,
          'n_channels': 4,
          'shuffle': True}

# Datasets
# partition = # IDs
labels = ['1']*params['n_classes']

# Generators
training_generator = DataGenerator(labels, **params)
validation_generator = DataGenerator(labels, **params)

# print(training_generator[0])

# Design model
model = Sequential()
# 第一个卷积层，32个卷积核，大小５x5，卷积模式SAME,激活函数relu,输入张量的大小 
model.add(Conv2D(filters= 32, kernel_size=(5,5), padding='Same', activation='relu',input_shape=(4,9,4)))
model.add(Conv2D(filters= 32, kernel_size=(5,5), padding='Same', activation='relu'))
# 池化层,池化核大小２x2
model.add(MaxPool2D(pool_size=(2,2)))
# 随机丢弃四分之一的网络连接，防止过拟合
model.add(Dropout(0.25))  
model.add(Conv2D(filters= 64, kernel_size=(3,3), padding='Same', activation='relu'))
model.add(Conv2D(filters= 64, kernel_size=(3,3), padding='Same', activation='relu'))
model.add(MaxPool2D(pool_size=(2,2), strides=(2,2)))
model.add(Dropout(0.25))
# 全连接层,展开操作，
model.add(Flatten())
# 添加隐藏层神经元的数量和激活函数
model.add(Dense(256, activation='relu'))    
model.add(Dropout(0.25))
# 输出层
model.add(Dense(params['n_classes'], activation='softmax'))

optimizer = RMSprop(lr = 0.001, decay=0.0)
model.compile(optimizer=optimizer, loss = 'categorical_crossentropy',metrics=['accuracy'])

# Train model on dataset
model.fit_generator(generator=training_generator,
                    validation_data=validation_generator,
                    use_multiprocessing=True,
                    workers=6)

