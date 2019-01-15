import orm 
from models import User, Blog, Comment 

'''
test whether the ORM performs. 
'''
async def test(loop):
	await orm.create_pool(loop,
						user='root',
						password='yangzhikai668',
						db='awesome')
	u = User(name='test', email='test@example.com', passwd='123', image='about:blank')
	await u.save()

import asyncio 
# loop = asyncio.get_event_loop()
# loop.run_until_complete(test(loop))
# loop.close()

import inspect
def test_func(a,b=1,*c,**kw):
	pass 

params = inspect.signature(test_func).parameters
print(params)
for name, param in params.items():
	if param.kind == inspect.Parameter.KEYWORD_ONLY:
		print(name, param)
	elif param.kind == inspect.Parameter.VAR_KEYWORD:
		print('VAR_KEYWORD:', name, param)
	else:
		print('other params:', param)