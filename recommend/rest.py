from flask import Flask ,jsonify ,abort,request

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

@app.route('/get',methods = ['GET'])
def index():
	return jsonify({'task':task})

@app.route('/get/task/<string:task_id>',methods = ['GET'])
def get_task(task_id):
	task_o = list(filter(lambda t: t['id'] == task_id,task))
	if len(task_o) ==0:
		abort(404)
	return jsonify({'task':task_o[0]})

@app.route('/get/task',methods=['POST'])
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


if __name__ == '__main__':
	app.run(debug = True)