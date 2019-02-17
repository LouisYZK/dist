# from celery_tasks import add

from celery_app import celery_tasks

if __name__ == '__main__':
    print('start task....')
    res = celery_tasks.add.delay(3, 5)
    print('end task..')

    print(res)