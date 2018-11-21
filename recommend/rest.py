from flask import Flask ,jsonify ,abort,request
from flask.httpauth import HttpBasicAuth
app = Flask(__name__)

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

@auth.get_password
def get_password(username):
	if username =='yzk':
		return 'python'
	return None
@auth.error_handler
def unauhorized():
	return make_response(jsonify({'error':'unauhorized access'},401))

@app.route('/api/tasks',methods = ['GET'])
@auth.login_required
def index():
	return jsonify({'task':task})

@app.route('/api/tasks/<string:task_id>',methods = ['GET'])
def get_task(task_id):
	task_o = list(filter(lambda t: t['id'] == task_id,task))
	if len(task_o) ==0:
		abort(404)
	return jsonify({'task':task_o[0]})

@app.route('/api/tasks',methods=['POST'])
def create_task():
	if not request.json or not 'title' in request.json:
		abort(400)
	task_new = {
		'id':'3',
		'title':request.json['title'],
		'content':request.json.get('content','')
	}
	task.append(task_new)
	return jsonify({'task':task}),201 

@app.route('/api/tasks/<string:task_id>',methods=['PUT'])
def update(task_id):
	task_o = list(filter(lambda i:i['id'] == task_id,task))
	task_o[0]['content'] = request.json['content']
	task_o[0]['title'] = request.json['title']
	return jsonify({'task':task_o[0]})

if __name__ == '__main__':
	app.run(debug = True)

