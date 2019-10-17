#  function that uses MPI and OpenMP hybrid programming
from cython import parallel
from mpi4py import MPI

def cal_k(comm, u, K):
    cdef unsigned int thread_id
    cdef int i
    cdef int j
    cdef int k
    cdef int length
    length = u.shape[0]
    k = K
    print(u.shape)
    # use 4 OpenMP threads to execute the following code
    with nogil, parallel.parallel(num_threads=10):
        # allocate np tasks to the 4 threads with a chunk size of 2
        # and a static schedule, so thread 0 will have task 0 and 1,
        for i in parallel.prange(2, length-2, schedule="dynamic"):
            with gil:
                for j in range(2, length-2):
                    u[i,j,k+1] = 2*u[i,j,k]-u[i,j,k-1]
                    u[i,j,k+1] = u[i,j,k+1]-u[i-2,j,k]/12-u[i+2,j,k]/12+u[i-1,j,k]*4/3+u[i+1,j,k]*4/3-u[i,j,k]*5/2
                    u[i,j,k+1] = u[i,j,k+1]-u[i,j-2,k]/12-u[i,j+2,k]/12+u[i,j-1,k]*4/3+u[i,j+1,k]*4/3-u[i,j,k]*5/2
                rank = comm.rank
                # get the processor name
                pname = MPI.Get_processor_name()
                # calculate
                print('MPI rank %d, OpenMP thread %d in %s calculating %sth layer' % (rank, thread_id, pname, k))
