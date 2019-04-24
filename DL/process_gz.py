import sys
import gzip
import shutil
import os

# if (sys.version_info > (3, 0)):
#     writemode = 'wb'
# else:
#     writemode = 'w'

# zipped_mnist = [f for f in os.listdir('./') if f.endswith('ubyte.gz')]
# for z in zipped_mnist:
#     with gzip.GzipFile(z, mode='rb') as decompressed, open(z[:-3], writemode) as outfile:
#         outfile.write(decompressed.read())

import os
import struct
import numpy as np
 
def load_mnist(path, kind='train'):
    """Load MNIST data from `path`"""
    labels_path = os.path.join(path, 
                               '%s-labels-idx1-ubyte' % kind)
    images_path = os.path.join(path, 
                               '%s-images-idx3-ubyte' % kind)
        
    with open(labels_path, 'rb') as lbpath:
        magic, n = struct.unpack('>II', 
                                 lbpath.read(8))
        labels = np.fromfile(lbpath, 
                             dtype=np.uint8)

    with open(images_path, 'rb') as imgpath:
        magic, num, rows, cols = struct.unpack(">IIII", 
                                               imgpath.read(16))
        images = np.fromfile(imgpath, 
                             dtype=np.uint8).reshape(len(labels), 784)
        images = ((images / 255.) - .5) * 2
 
    return images, labels

import os
import struct
import numpy as np
 
def load_mnist(path, kind='train'):
    """Load MNIST data from `path`"""
    labels_path = os.path.join(path, 
                               '%s-labels-idx1-ubyte' % kind)
    images_path = os.path.join(path, 
                               '%s-images-idx3-ubyte' % kind)
        
    with open(labels_path, 'rb') as lbpath:
        magic, n = struct.unpack('>II', 
                                 lbpath.read(8))
        labels = np.fromfile(lbpath, 
                             dtype=np.uint8)

    with open(images_path, 'rb') as imgpath:
        magic, num, rows, cols = struct.unpack(">IIII", 
                                               imgpath.read(16))
        images = np.fromfile(imgpath, 
                             dtype=np.uint8).reshape(len(labels), 784)
        images = ((images / 255.) - .5) * 2
 
    return images, labels


# X_train, y_train = load_mnist('', kind='train')
# X_test, y_test = load_mnist('', kind='t10k')


# import numpy as np

# np.savez_compressed('mnist_scaled.npz', 
#                     X_train=X_train,
#                     y_train=y_train,
#                     X_test=X_test,
#                     y_test=y_test)

def fn(A):
    print(A, '...')
    return A**2
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor() as e:
    fn_pool = e.map(fn, [1, 2, 3, 4])
    for future in fn_pool:
        print('res:', future)


    