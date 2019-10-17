
"""
Demonstrates how to use mpi4py and OpenMP hybrid programming.
使用MPI+ Open计算三维矩阵
tun this with 2 processes like:
$ mpiexec -n 2 python mpi_openmp.py
"""


from mpi4py import MPI
import numpy as np
import argparse
import calculate
import matplotlib.pyplot as plt
# import calculate

parser = argparse.ArgumentParser()
# 矩阵[d, d, k]维度中的d, 建议d为偶数
parser.add_argument('-d', type=int)
# 采用的空间分割策略是简单的按照进程数量进行网格划分。
# 例如采用16个进程的话，就可以将平面分为4*4的网格，共16个网格，每个网格分别独立计算

#initate value
args = parser.parse_args()


comm = MPI.COMM_WORLD                                                             
rank = comm.Get_rank()                                                            
size = comm.Get_size()

# 计算步长
step = round(args.d / 4) 
nt = 100
step = step -1
if comm.rank == 0:
    ni = nj = args.d
    # 网格划分
    index = []
    for i in range(4):
        for j in range(4):
            index.append((i * step, j*step))
    u  = np.zeros((ni,nj,nt))
    for i in range(0,101): #k+1
        for j in range(0,101):  #k+1
            u[49:52,49:52,0]=np.ones((3,3)) # u[k/2-1:k/2+2,k/2-1:k/2+2,0]=np.ones((3,3)) 
            u[48:53,48:53,1]=np.ones((5,5)) # u[k/2-2:k/2+3,k/2-2:k/2+3,0]=np.ones((5,5)) 
            u[50,50,1]=np.zeros((1,1))      # u[k/2,k/2,1]=np.zeros((1,1))for i in range(0,101): #k+1
else:
    u = None
    index = None

recv_u = comm.bcast(u, root=0)
recv_ind = comm.scatter(index, root=0)
x, y = recv_ind[0], recv_ind[1]
pre_u = recv_u[x: x + step, y: y + step, :]
print(x, y, pre_u.shape)
for k in range(nt-1):
    calculate.cal_k(comm, pre_u, k)

u_tup = (recv_ind, pre_u)


def draw(A, k=89):
    x, y = A.shape[0], A.shape[1]
    X, Y = np.meshgrid(np.arange(x), np.arange(y))
    plt.contourf(X, Y, A[:, :, k])
    name = str(x) + '-' + str(k)
    name += '.png'
    plt.savefig(name)
    plt.show()

gather_A = comm.gather(u_tup, root=0)  
if comm.rank == 0:
    A = np.zeros((args.d, args.d, 100))
    for ind, mat in gather_A:
        x, y = ind
        A[x: x + step, y: y + step, :] = mat
    print(A.shape)
    draw(A, k=99)
    

