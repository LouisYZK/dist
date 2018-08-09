from flask import Flask,jsonify
from flask.ext.restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)
task = [
	{
		'id':'1',
		'title':'python',
		'content':'Life is short, use it!'
	},
	{
		'id':'2',
		'title':'php',
		'content':'The most beautiful language in the world!'
	}
]
class TaskListAPI(Resource):
	def __init__(self):
		self.parse = reqparse.RequestParser()
		self.parse.add_argument('title',type = str,required = True, help = 'You need title',location = 'json')
		self.parse.add_argument('content',type = str,default = '',location = 'json')
		super(TaskListAPI,self).__init__()
	def get(self):
		return jsonify({'task':task})

class TaskAPI(Resource):
	def __init__(self):
		self.parse = reqparse.RequestParser()
		self.parse.add_argument('title',type = str,location = 'json')
		self.parse.add_argument('content',type = str,location = 'json')
		super(TaskAPI,self).__init__()

	def put(self,task_id):
		task_o = list(filter(lambda i:i['id'] == task_id),task)
		if len(task_o) ==0:
			abort(404)
		task_o = task_o[0]
		args = self.reqparse.parse_args()
		for k ,v in args.iteritems():
			if v!=None:
				task_o[k] = v
		return jsonify({'task':task_o})

api.add_resource(TaskListAPI,'/task')
api.add_resource(TaskAPI,'/task/<int:task_id>')
