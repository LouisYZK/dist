- 编译

python setup.py build_ext --inplace

- 执行任务

mpiexec -np 16 python mpi_openmp.py

calculate.pyx是python风格的C语言，实现Open MP的多线程并行

mpi_openmp文件实现了python语言调用MPI
