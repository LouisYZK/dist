import cvxpy as cp 
import numpy as np 
def test01():
	x = Variable()
	y = Variable()
	constraint = [x+y == 1,x-y >= 1]
	obj = Minimize(square(x-y))
	prob = Problem(obj,constraint)
	prob.solve()
	print(prob.status)
	print(x.value,y.value)
	print(prob.value)
# test01()
# 向量
def test02():
	m = 20
	n = 10
	A = np.random.randn(m,n)
	b = np.random.randn(m)
	x = cp.Variable(n)
	obj = cp.Minimize(cp.sum_squares(A*x-b))
	constraint = [x>=0,x<=1]
	prob = cp.Problem(obj,constraint)
	prob.solve()
	print(prob.status)
	print(prob.value)
	print(x.value)
# test02()
# 二次规划
def test03():
	x1 = cp.Variable()
	x2 = cp.Variable()
	constraint = [x1+x2<=100,x1-2*x2<=0,x1>=0,x2>=0]
	obj = cp.Maximize(98*x1+277*x2-cp.power(x1,2)-0.3*x1*x2-2*cp.power(x2,2))
	prob = cp.Problem(obj,constraint)
	prob.solve()
	print(prob.status)
	print(prob.value)
	print(x1.value,x2.value)
	# 非凸，解不了...
# test03()
# 例2.1
def ex21():
	x = cp.Variable()
	y = cp.Variable()
	obj = cp.Maximize(2*x+3*y)
	constraint = [4*x+3*y<=10,3*x+5*y<=12,x>=0,y>=0]
	prob = cp.Problem(obj,constraint)
	prob.solve()
	print(prob.status)
	print(prob.value)
	print(x.value,y.value)
# ex21()
