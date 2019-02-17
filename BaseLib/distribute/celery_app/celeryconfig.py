from datetime import  timedelta
from celery.schedules import crontab

BROKER_URL = 'redis://localhost:6379/1'

CELERY_RESULT_BACKEND = 'redis://localhost:6379/2'

CELERY_TIMEZONE = 'Asia/Shanghai'

CELERY_IMPORTS = (
    'celery_app.celery_tasks',
)

CELERYBEAT_SCHEDULE = {
    'task1': {
        'task': 'celery_app.celery_tasks.add',
        'schedule': timedelta(seconds=10),
        'args': (2, 8)
    },
    'task2':{
        'task': 'celery_app.celery_tasks.mul',
        'schedule': crontab(hour=16, minute=27),
        'args': (2, 8)
    }
}

# celert指令
# celery -B -A celery_app worker -l INFO
# celery flower --broker ...
