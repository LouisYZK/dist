import numpy as np

# def data_generator(batch_size):
#     for i in range(batch_size):
#         yield np.random.randn(4,4,9)
def data_generator():
    while True:
        yield np.random.randn(4,4,9)
x = data_generator()
y = next(x)

dim = [4,9]
n_channels = 9
def gen_X(size):
    yield np.random.rand(size,*dim,n_channels)
x = gen_X(1)
x = next(x)
x.shape
