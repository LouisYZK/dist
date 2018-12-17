cimport cython 

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef clip(double[:] a, double min, double max, double[:] out):
	for i in range(len(a)):
		if a[i]<min:
			out[i] = min
		elif a[i]>max:
			out[i] = max
		else:
			out[i] = a[i]