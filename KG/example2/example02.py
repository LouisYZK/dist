import requests
import json
import pickle
with open('test_doc.txt','r',encoding='utf8',errors='ignore') as f:
	test_doc = f.read()

def get_Entity(doc):
	url = 'http://shuyantech.com/api/entitylinking/cutsegment'
	doc = doc.split('。')
	entities = []
	for item in doc:
		params = {'q':item}
		r = requests.get(url,params = params)
		entity = json.loads(r.text)['entities']
		entities.append([item2[0] for item2 in entity])
	# with open('entity.pkl','w') as f:
	# 	pickle.dump(f,entities)
	return entities

def get_trip_tuple(entity):
	url = 'http://shuyantech.com/api/cndbpedia/avpair'
	know = []
	for item in entity:
		params = {'q':item}
		text = r.get(url,params = params).text
		knowledge = json.loads(text)['ret']
		know.append(knowledge)
	return know

def store_in_neo4j(triple):
	# 加载entity

	# 添加节点和属性

	# 构建节点间关系
	pass

if __name__ =='__main__':
	print(get_Entity(test_doc))