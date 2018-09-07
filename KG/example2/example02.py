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
		entities.append([item2[1] for item2 in entity])
	with open('entity.pkl','wb') as f:
		pickle.dump(entities,f)

def flatten(items):
    for x in items:
        if hasattr(x,'__iter__') and not isinstance(x, (str, bytes)):
            # for sub_x in flatten(x):
            #     yield sub_x
            yield from flatten(x)
        else:
            yield x

def get_trip_tuple():
	url = 'http://shuyantech.com/api/cndbpedia/avpair'
	know = {}
	with open('entity.pkl','rb') as f:
		entities = pickle.load(f)
	entities = list(flatten(entities))
	for item in entities:
		params = {'q':item}
		text = requests.get(url,params = params).text
		knowledge = json.loads(text)['ret']
		know[item] = knowledge
	with open('know.json','w') as f:
		json.dump(know,f)
	return know

def is_entity(en):
	with open('entity.pkl','rb') as f:
		entities = set(list(flatten(pickle.load(f))))
	return en in entities

def store_in_neo4j(triple):
	from py2neo import Graph, Node, Relationship ,NodeSelector
	graph = Graph('http://52.83.213.55:7474',user ='neo4j',password = 'yangzhikai668')
	# graph = Graph('http://localhost:7474',user = 'neo4j',password='yangzhikai668')
	select = NodeSelector(graph)
	# 加载entity
	with open('entity.pkl','rb') as f:
		entities = pickle.load(f)
	entities = list(flatten(entities))
	# 添加所有实体为结点
	for en in entities:
		node = Node('Entity',name= en)
		graph.create(node)
	# 遍历三元组，添加节点的属性，结点间关系等
	for en, kw in triple.items():
		node_1 = select.select('Entity').where(name = en).first()
		for item in kw:
			if item[1] in triple.keys():
				node_2 = select.select('Entity').where(name = item[1]).first()
				relate = Relationship(node_1,item[0],node_2)
				graph.create(relate)
			else:
				node_1[item[0]] = item[1]
				graph.push(node_1)
	print('数据存储完毕')
if __name__ =='__main__':
	# print(get_Entity(test_doc))
	# triple = get_trip_tuple()
	with open('know.json','r') as f:
		triple = json.load(f)
	store_in_neo4j(triple)
