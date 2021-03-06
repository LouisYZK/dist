# -*- coding: utf-8 -*-
import os
import codecs
import numpy as np 
from gensim import corpora,models,similarities
from corpus import preprocess, Corpus
class recommend:
    def __init__(self):
        pass 
    def get_corpus(self,doc):
        corp = []
        for item in text:
            corp.append(dictionary.doc2bow(pre.cut(pre.clean_doc(item))))
        self.corp = corp
    def __vectorize(self):
        self.__set_corpus()
        tfidf = models.TfidfModel(self.corp)
        self.tfidf_vect = [tfidf[item] for item in self.corp]
        lsi = models.LsiModel(self.corp)
        self.lsi_vect= [lsi[item] for item in self.corp]
        lda = models.LdaModel(self.corp,num_topics=5)
        self.lda_vect= [lda[item] for item in self.corp]
    def gen_vec(self,corp):
        tfidf = models.TfidfModel(corp)
        vec = {}
        vec['tfidf'] = [tfidf[item] for item in corp]
        lsi = models.LsiModel(corp)
        vec['lsi'] = [lsi[item] for item in corp]
        lda = models.LdaModel(corp,num_topics=5)
        vec['lda'] = [lda[item] for item in corp]
        return vec
    # test string -->[['...'],['...'],...['...']]
    def get_sim(self,string):
        corp = self.get_corpus(string)
        vec = self.gen_vec(corp)
        sim = []
        for item,name in zip([self.tfidf_vect,self.lsi_vect,self.lda_vect],['tfidf','lsi','lda']):
            index = similarities.SparseMatrixSimilarity(self.lda_vect, num_features=len(self.dictionary.keys()))
            sim.append(index[vec[name]][0])
        sim = np.array(sim)
        index_com = np.argmax(np.mean(sim,axis=0))
        index_lda = np.argmax(sim[2,:],axis=0)
        index_lsi = np.argmax(sim[1,:],axis=0)
        return [index_com,index_lsi,index_lda]        
#test
p = recommend('./doc')

 
# for ind,item in  df.iterrows():
#     fname = item['标题']
#     try:
#         with open('./doc/weixin/'+fname+'.txt','w') as f:
#             if type(item['内容']) == 'str':
#                 f.write(item['内容'])
#     except FileNotFoundError:
#         continue
    

# def wrapper(func):
#     def inner(x,y):
#         a = func(x,y)
#         a +=1
#         return a
#     return inner
# @wrapper
# def func(a,b):
#     return a+b
# func(1,2)

# def log(func):
#     def inner(*args,**kwargs):
#         print("Arguments were %s %s" % (args,kwargs))
#         return func(*args,**kwargs)
#     return inner
# @log
# def fun1(a,x=1,y=2):
#     return a+x+y
# @log
# def fun2():
#     return 2
# fun1(1)
# fun1(1,10,10)
# fun2()
