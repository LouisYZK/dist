import os
import codecs
import re
import jieba
import json
import pickle
import numpy as np 
import heapq
from gensim import corpora,models,similarities

# doc 结构
# doc ={
#     'name':string,
#     'id': int,
#     'url': doc's position,
#     'recomm':[doc1,doc2,doc3,doc4,doc5]
# }
class preprocess():
    stopwords = []
    stopword_filepath="./stopwordList/stopword.txt"
    def __init__(self):
        self.__readin_stop()
    def __readin_stop(self):
        file_obj = codecs.open(self.stopword_filepath,'r','utf-8')
        while True:
            line = file_obj.readline()
            line=line.strip('\r\n')
            if not line:
                break
            self.stopwords.append(line)
        file_obj.close()
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

class Corpus():
    def __init__(self,dir):
        self.dir = dir
        self.__set_dir()
        self.__set_origin_corpus()
    def __set_dir(self):
        if 'doc.json' in os.listdir():
            print("----------文本库已经构建---------")
            return 
        doc_name = os.listdir(self.dir)
        doc = []
        id_num = 0
        for doc_item in doc_name:
            id_num +=1
            doc_item.replace('/','')
            doc.append({'id':id_num,'name':doc_item,'url':self.dir+doc_item})
        with open('doc.json','w',encoding = 'gbk') as f:
            json.dump(doc,f)
    def __set_origin_corpus(self):
        if('dictionary.txt' in os.listdir()):
            print("----------语料库已经构建---------")
            self.dictionary = corpora.Dictionary.load_from_text('dictionary.txt')
            return             
        with open('doc.json','r',encoding = 'gbk') as f:
            doc = json.load(f)
        corpus = []
        text = []
        pre = preprocess()
        for doc_item in doc:
            with open(self.dir + doc_item['name'],'r',encoding='gbk') as f:
                text.append(f.read())
        for item in text:
            pre_doc = pre.cut(pre.clean_doc(item))
            corpus.append(pre_doc)
        dictionary = corpora.Dictionary(corpus)
        dictionary.save_as_text('dictionary.txt')
        corp = []
        print('----------词典构建完毕，目前共有词:%d 个---------' % len(dictionary.keys()))
        for item in text:
            corp.append(dictionary.doc2bow(pre.cut(pre.clean_doc(item))))
        with open('corpus.pkl','wb') as f:
            pickle.dump(corp,f)
        self.corp = corp
        print('----------语料库构建完毕---------')

    def update(self,new_dir):
        if os.path.exists('dictionary.txt'):
            dictionary = corpora.Dictionary.load_from_text('dictionary.txt')
        else:
            print('----------词典库还未构建---------')
            return 
        new_doc_name = os.listdir(new_dir)
        with open('doc.json','r',encoding='gbk') as f:
            doc = json.load(f)
        num = doc[-1]['id']
        for doc_item in new_doc_name:
            num +=1
            doc_item.replace('/','')
            doc.append({'id':num,'name':doc_item,'url':new_dir+doc_item})
        with open('doc.json','w',encoding='gbk') as f:
            f.truncate()
            json.dump(doc,f)
            print('----------文本库已更新---------')
        add_corpus = []
        add_text = []
        pre = preprocess()
        for doc_item in new_doc_name:
            with open(new_dir + doc_item,'r') as f:
                add_text.append(f.read())
        print('----------新增添文章:%d 篇---------' % len(new_doc_name))
        for item in add_text:
            add_pre_doc = pre.cut(pre.clean_doc(item))
            add_corpus.append(add_pre_doc)
        dictionary.add_documents(add_corpus)
        if len(dictionary.keys()) >=10:
            os.remove('dictionary.txt')
            dictionary.save_as_text('dictionary.txt')
            print('----------字典库已更新完毕---------')
            print('----------更新后的字典库有词：%d 个---------' % len(dictionary.keys()))
        corp = []
        text = []
        for item in doc:
            try:
                with open(item['url'],'r',encoding='gbk') as f:
                    text.append(f.read())
            # 如果gbk方式不行则更换编码utf8进行读取
            except UnicodeDecodeError :
                with open(item['url'],'r') as f:
                    text.append(f.read())
                continue
        for item in text:
            corp.append(dictionary.doc2bow(pre.cut(pre.clean_doc(item))))
        with open('corpus.pkl','wb') as f:
            f.truncate()
            pickle.dump(corp,f)
        self.corp = corp
        print('----------语料库更新完毕---------')
      
# test
import time
t1 = time.time()
c = Corpus('./doc/weixin/')
t2 = time.time()
print('Bulid time:',t2-t1)
c.update('./doc/new_test/')
t3 = time.time()
print('Update tiem :',t3-t2)

class recommend:
    def __init__(self):
        self.__vectorize()
        self.get_sim()
    def __set_corpus(self):
        if not os.path.exists('corpus.pkl'):
            print('----------未发现语料库，不能计算相似度！---------')
            return
        with open('corpus.pkl','rb') as f:
            self.corp = pickle.load(f)
    def __vectorize(self):
        self.__set_corpus()
        tfidf = models.TfidfModel(self.corp)
        lda = models.LdaModel(self.corp,num_topics=5)
        lsi = models.LdaModel(self.corp)
        self.tfidf_vect = [tfidf[item] for item in self.corp]
        self.lda_vect = [lda[item] for item in self.corp]
        self.lsi_vect = [lsi[item] for item in self.corp]

    def get_sim(self):
        with open('doc.json','r',encoding='gbk') as f:
            doc = json.load(f)
        self.dictionary  = corpora.Dictionary.load_from_text('dictionary.txt')
        for doc_item in doc:
            sim = []
            for item in [self.tfidf_vect,self.lsi_vect,self.lda_vect]:
                index = similarities.SparseMatrixSimilarity(item, num_features=len(self.dictionary.keys()))
                sim.append(index[item[doc_item['id']-1]])
            # index = similarities.SparseMatrixSimilarity(self.lda_vect, num_features=len(self.dictionary.keys()))
            # index = index[self.lda_vect[doc_item['id']-1]]
            sim = np.array(sim)
            sim_vec = np.mean(sim,axis = 0)
            most_sim_doc_id = heapq.nlargest(11,range(len(sim_vec)),sim_vec.take)
            doc_item['sim'] = most_sim_doc_id
            print(doc_item['name'],'已计算',most_sim_doc_id)

        with open('doc.json','w',encoding = 'gbk') as f:
            f.truncate()
            json.dump(doc,f)
        print('----------计算相似文档结束！---------')

# test
rec = recommend()
t4 = time.time()
print('Get Sim Time:',t4-t3)

def get_res():
    with open('doc.json','r') as f:
        doc = json.load(f)
    with open('res.txt','w') as f:
        for item in doc:
            f.writelines('标题:'+item['name']+'的推荐文章为：\n')
            f.write("\n")
            for item2 in  item['sim']:
                f.writelines(doc[item2-1]['name'])
                f.write("\n")
            f.write('-------------------------------\n')
get_res()
print("结果已写入文档")
def draw():
    with open('doc.json','r') as f:
        doc = json.load(f)
    import networkx as nx
    G = nx.Graph()
    for i in range(1,len(doc)+1):
        G.add_node(str(i))
    for item in doc:
        G.add_edge(str(item['id']),str(item['sim'][0]))
    nx.draw(G,with_labels = True,font_size =11,node_size=10,alpha = 0.6,edge_color = 'k')
    import matplotlib.pyplot as plt
    plt.show()
