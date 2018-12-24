import reprlib
from array import array 
import math 
import functools
import itertools
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

	# def __add__(self)
		try :
			pairs = itertools.zip_longest(self, other, fillvalue = 0.0)
			return Vector(a + b for a, b in pairs)
		except TypeError:
			return NotImplemented 
	def __radd__(self,other):
		return self + other

	@classmethod
	def frombytes(cls, octets):
		typecode = chr(octets[0])
		memv = memoryview(octets[1:]).cast(typecode)
		return cls(memv)

# Can be accepted any sequence object!
# print(Vector([1,2,3]))
# import numpy as np 
# print(Vector(np.array([4,5,6])))
# from array import array
# print(Vector(array('i',[7,8,9])))
# print(Vector(range(10)))

from collections import namedtuple

Result = namedtuple("Result", "count average")

# subgenerator
def average():
	count = 0
	total = 0
	average = None
	while True:
		item = yield
		if item is None:
			break
		count +=1
		total += item
		average = total/count
	return Result(count, average) 

# deligate generator
def grouper(results, key):
	while True :
		results[key] = yield from average()

def main(data):
	res = {}
	for key, values in data.items():
		group = grouper(res, key)
		next(group)
		for val in values:
			group.send(val)
		group.send(None)
	report(res)

def report(res):
	for key, item in res.items():
		print(key, item) 

data = {
	'girls;kg':[40.9, 38.5, 44.3, 42.2, 45.2, 41.7, 44.5, 38.0, 40.6, 44.5],
	'girls;m':[1.6, 1.51, 1.4, 1.3, 1.41, 1.39, 1.33, 1.46, 1.45, 1.43],
	'boys;kg':[39.0, 40.8, 43.2, 40.8, 43.1, 38.6, 41.4, 40.6, 36.3],
	'boys;m':[1.38, 1.5, 1.32, 1.25, 1.37, 1.48, 1.25, 1.49, 1.46],
}

main(data)
