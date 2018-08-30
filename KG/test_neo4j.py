from py2neo import Graph, Node, Relationship ,NodeSelector

a = Node('Person',name='yzk')
b = Node('Person',name= 'whf')
r = Relationship(a,'konws',b,since = 1999)
s = a|b|r 
graph = Graph('http://52.83.213.55:7474',user ='neo4j',password = 'yangzhikai668')
# graph.create(s)
select = NodeSelector(graph)
per = select.select('Person').where(name = 'yzk').first()
# print(per)

