from aiohttp import web
from aiohttp_swagger import *
from tortoise.models import Model
from tortoise import fields, Tortoise
from tortoise.transactions import atomic, in_transaction
import asyncio
import logging
import time
import datetime

logging.basicConfig(level=logging.DEBUG)
routes = web.RouteTableDef()


@routes.get('/task')
@swagger_path("tasks.yaml")
async def get_task(request):
    task_id = request.match_info.get('task_id', '')
    task_id = request.query.get('task_id', '')
    await init_db()
    res = list()
    if task_id:
        task_info = await Task.filter(id=task_id).all()
    else:
        task_info = await Task.all()
    for task in task_info:
        info = {
            'task_id': task.id,
            'task_name': task.task_name,
            'task_status': task.status,
            'start_time': task.start_time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        if task.end_time is not None:
            info['end_time'] = task.end_time.strftime("%Y-%m-%d %H:%M:%S")
        else: info['end_time'] = ''
        res.append(info)
    return web.json_response({"status": "ok", "message": res})

@routes.post('/task')
@swagger_path("tasks.yaml")
async def create_task(request):
    data = await request.json()
    task_name = data.get('task_name', '')
    timestamp = datetime.datetime.now()
    await init_db()
    async with in_transaction() as conn:
        task = Task(task_name=task_name, start_time=timestamp)
        await task.save()
        task_id = task.id
    asyncio.create_task(perform_task(task_id))
    return web.json_response({"status": "ok", "task_id": task_id})



async def perform_task(task_id):
    """simple task
    """
    await asyncio.sleep(3)
    await update_status(task_id, "30%")
    await asyncio.sleep(3)
    await update_status(task_id, "60%")
    await asyncio.sleep(10)
    await update_status(task_id, "100%")
    await init_db()
    async with in_transaction() as conn:
        end_time = datetime.datetime.now()
        await Task.filter(id=task_id).using_db(conn).update(end_time=end_time)
    print(f'Task {task_id} ended!')

async def update_status(task_id, status):
    await init_db()
    await Task.filter(id=task_id).update(status=status)

DB_URL = 'mysql://root:750750750@localhost:3306/test?charset=utf8'
class Task(Model):
    id = fields.IntField(pk=True)
    task_name = fields.CharField(max_length=100)
    status = fields.CharField(max_length=50, null=True)
    start_time = fields.DatetimeField()
    end_time = fields.DatetimeField(null=True)
    
async def init_db(create_db=False):
    await Tortoise.init(
        db_url=DB_URL,
        modules={'apps': ['__main__']},
        _create_db=create_db
    )
    # await Tortoise.generate_schemas()

app = web.Application()
app.add_routes(routes)
setup_swagger(app, swagger_url="/apidocs")
if __name__ ==  '__main__':
    # asyncio.run(init_db())
    asyncio.run([web.run_app(app)], debug=True)