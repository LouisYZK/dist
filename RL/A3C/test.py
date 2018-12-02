class A():
	def __init__(self, a):
		self.a = a 
	def print_a(self):
		print(self.a)
	def run(self):
		print("I am runnig A!")

class B(A):
	# def __init__(self):
	def run(self):
		print("B is running!")

b = B(1)
b.run()
b.print_a()
