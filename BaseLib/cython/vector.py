import reprlib
from array import array 
import math 
import functools
import operator
class Vector:
	typecode = 'd'

	def __init__(self, components):
		self._components = array(self.typecode, components)

	def __iter__(self):
		return iter(self._components)

	def __repr__(self):
		com = reprlib.repr(self._components)
		com = com[com.find('['):-1]
		return 'Vector({})'.format(com)

	def __str__(self):
		return str(tuple(self._components))

	def __len__(self):
		return len(self._components)

	def __eq__(self, other):
		# return tupe(self) == tuple(other)
		# if len(self) !=len(other):
		# 	return False
		# for a,b in zip(self,other):
		# 	if a!=b:
		# 		return False
		# return True
		return len(self) == len(other) and all(a==b for a, b in zip(self,other))

	def __abs__(self):
		return math.sqrt(sum([x for x in self]))

	def __getitem__(self, index):
		return self._components[index]

	def __hash__(self):
		hashes = (hash(x) for x in self._components)
		return functools.reduce(operator.xor, hashes, 0)

	@classmethod
	def frombytes(cls, octets):
		typecode = chr(octets[0])
		memv = memoryview(octets[1:]).cast(typecode)
		return cls(memv)
