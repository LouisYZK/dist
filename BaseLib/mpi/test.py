from mpi4py import MPI                                                            
import numpy as np                                                                
                                                                                  
comm = MPI.COMM_WORLD                                                             
rank = comm.Get_rank()                                                            
size = comm.Get_size()                                                            
                                                                                  
recv_data = None                                                                  
                                                                                  
if rank == 0:                                                                     
    # send_data = range(10)
    A = [i for i in range(10)]
    print("process {} scatter data {} to other processes".format(rank, A))
else:                                                                             
    A = None                                                              
recv_A = comm.bcast(A, root=0)
print(recv_A)
print("process {} recv data {}...".format(rank, recv_A))
if A: print("final A:", A)