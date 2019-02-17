## Indrocution of Parallel and Distributed
- Parallel computing is the simultaneous use of more than one **processor** to solve a problem.
    - two ways: multi-processing and multi-thread
    - shared memeory architechture
- Distributed computing is the simultaneous use of more than one **computer** to solve a problem.
    - CPU-GPU combination is also an example of distributed.
    - distributed memory achitetchture.
- Shared & Distributed Memory:
    - parallel application, all concurrent tasks can—in principle—access the same memory space.
    - distributed application, however, the various concurrent tasks cannot normally access the same memory space due to different physical computers;


## Parallel in Python
章末的总结写的挺好：

- We looked at a couple of technologies that we can exploit to make our Python code run faster and, in some cases, use multiple CPUs in our computers. One of these is the use of multiple threads, and the other is the use of multiple processes. Both are supported natively by the Python standard library.

- We looked at three modules: **threading**, for developing multithreaded applications, **multiprocessing**, for developing process-based parallelism, and **concurrent.futures**, which provides a high-level asynchronous interface to both.

- As far as parallelism goes, these three modules are not the only ones that exist in Python land. Other packages implement their own parallel strategies internally, freeing programmers from doing so themselves. Probably, the best known of these is **NumPy**, the de-facto standard Python package for array and matrix manipulations. Depending on the BLAS library that it is compiled against, NumPy is able to use multiple threads to speed up complex operations (for example, the matrix-matrix dot product).

- In the same vein, one interesting thing to note is that the multiprocessing module also has support for Python processes running on different machines and communicating over the network. In particular, it exports a couple of Manager classes (that is, BaseManager and SyncManager). These use a socket server to manage data and queues and share them over the network. The interested reader can explore this topic further by reading the online documentation in the multiprocessing module section available at [ibrary/multiprocessing.html#managers](https://docs.python.org/3/).

- Another piece of technology that might be worth investigating is **Cython**, a Python-like language to create C modules that is extremely popular and actively developed. Cython has excellent support for OpenMP, a directive-based API for C, C++, and Fortran, that allows programmers to easily multithread their code.