import time
# from celery import Celery

# # 中间消息件
# broker = 'redis://localhost:6379/1'
# # 存储结果
# backend = 'redis://localhost:6379/2'

# app = Celery('my_task', broker=broker, backend=backend)

# @app.task

from celery_app import app

@app.task
def add(a, b):
    print('enter the func ..,')
    time.sleep(3)
    return a + b

@app.task
def mul(a, b):
    print('{}*{} is {}'.format(a, b, a*b))
    return a*b

# celery worker -A celery_tasks -l INFO

