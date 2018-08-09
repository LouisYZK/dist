from flask import Flask ,jsonify ,abort,request
import json

app = Flask(__name__)

@app.route('/doc/<int:doc_id>/recommend_doc',methods = ['GET'])
def get_rec(doc_id):
	with open('doc.json','r') as f:
		doc = json.load(f)
	for item in doc:
		if item['id'] == doc_id:
			sim = set(item['sim'])
	rec = []
	for item in doc:
		rec_item = {}
		if item['id'] in sim:
			rec_item['name'] = item['name']
			rec_item['id'] = item['id']
			rec_item['url'] = item['url']
			rec.append(rec_item)
	return jsonify({'recommed':rec})

if __name__ == '__main__':
	app.run(debug = True)