# -*- coding: utf-8 -*-
import os
import codecs
import re
import jieba
import numpy as np 
from gensim import corpora,models,similarities
from gensim.test.utils import get_tmpfile 
class recommend:
    stopwords = []
    stopword_filepath="./stopwordList/stopword.txt"
    def __init__(self,dir):
        self.__readin_stop()
        self.dir = dir
        self.__set_corpus()
    def __readin_stop(self):
        file_obj = codecs.open(self.stopword_filepath,'r','utf-8')
        while True:
            line = file_obj.readline()
            line=line.strip('\r\n')
            if not line:
                break
            self.stopwords.append(line)
        file_obj.close()
    def get_dir(self):
        doc_dir = os.listdir(self.dir)
        doc_name = [item for item in doc_dir if item[-4:] =='.txt']
        return doc_name
    def clean_doc(self,doc):
        pattern = re.compile(r'[\u4e00-\u9fa5]+')
        filter_data = re.findall(pattern,doc)
        cleaned_doc = ''.join(filter_data)
        return cleaned_doc
    def cut(self,doc):
        seg = jieba.cut(doc)
        results = []
        for item in seg:
            if item in self.stopwords:
                continue
            results.append(item)
        return results
    def __set_corpus(self):
        doc_name = self.get_dir()
        corpus = []
        text = []
        for doc_item in doc_name:
            with open('./doc/weixin/'+doc_item,'r') as f:
                text.append(f.read())
        for item in text:
            pre_doc = self.cut(self.clean_doc(item))
            corpus.append(pre_doc)
        dictionary = corpora.Dictionary(corpus)
        self.dictionary = dictionary
        corp = []
        for item in text:
            corp.append(dictionary.doc2bow(self.cut(self.clean_doc(item))))
        self.corp = corp
    def get_corpus(self,doc):
        corp = []
        for item in doc:
            corp.append(dictionary.doc2bow(self.cut(self.clean_doc(item))))
        return corp
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
p = recommend('./doc/weixin')