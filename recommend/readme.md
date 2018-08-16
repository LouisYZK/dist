# 基于文本内容的推荐系统开发日记
这里将会涉及：
- 推荐模型逻辑
- 算法基本实现与测试（gensim等模块的调用）
- 内存溢出问题的解决
- 编写Python rest 服务接口
## 推荐模型逻辑
![模块逻辑类图](https://ws1.sinaimg.cn/large/6af92b9fgy1fu13zbjhwoj20t90hn40u.jpg)

基本思路是围绕一个json文件展开，将文本对应信息保存在json中，json定时根据更新过后的字典库、语料库进行更新。

## 算法基本实现与测试
### 文本预处理
中文文本的预处理包含去标点、去停用词、分词（单独编辑为预处理模块）
```python
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
        # 汉字的Unicode范围为4e00-9fa5
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
```
此模块输入未处理的文本字符串，输出的是分词后的数组。
### 字典与语料库的构建
字典就是输入目前所有文本分词结果 dict = [(w1,id),(w2,id),(w3,id),...,(wn,id)]
而语料的格式是对应文本在字典中生成：
```json
corpus = [
    [
        #doc1
        (w,id),(w,id),(w,id).....(w,id)
    ],[
        #doc2
        (w,id),(w,id),....(w,id)
    ],
    ......[
        #doc_n
    ]
]
```
以上是语料库的基本格式

```python
def __set_origin_corpus(self):
        if('dictionary.txt' in os.listdir()):
            print("----------语料库已经构建---------")
            self.dictionary = corpora.Dictionary.load_from_text('dictionary.txt')
            return             
        with open('doc.json','r',encoding = 'gbk') as f:
            doc = json.load(f)
        corpus = []
        text = []
        # 引入预处理模块
        pre = preprocess()
        for doc_item in doc:
            with open(self.dir + doc_item['name'],'r',encoding='gbk') as f:
                text.append(f.read())
        for item in text:
            pre_doc = pre.cut(pre.clean_doc(item))
            corpus.append(pre_doc)
        dictionary = corpora.Dictionary(corpus)
        # 将字典库保存为txt
        dictionary.save_as_text('dictionary.txt')
        corp = []
        print('----------词典构建完毕，目前共有词:%d 个---------' % len(dictionary.keys()))
        for item in text:
            corp.append(dictionary.doc2bow(pre.cut(pre.clean_doc(item))))
        # 将语料库存储为pkl序列
        with open('corpus.pkl','wb') as f:
            pickle.dump(corp,f)
        self.corp = corp
        print('----------语料库构建完毕---------')
```
可以看到这里将语料库保存为pickle， 用gensim的save_as_text方法将字典保存为txt
这是为了方便后续模块调用，如果简单存为变量对内存要求较大，所以只能增加io次数，这样保证数据安全。
### 语料库的更新模块
输入每天新增加的文件夹路径目录，提取文档后更新字典库和语料库
```python
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
```
### 向量化与相似度计算模块
向量化的方式有很多，有基于统计方法的Tf-idf模型，有矩阵计算方法的LDA、LSI模型，有基于神经网络的word2vec模型。根据使用摸底选择了前三个模型进行向量化，计算三个相似度后取平均。当然此模块应先加载前面完成的json文件和corp语料库。

- TF-IDF 向量 ： 

  $$TF-IDF(w,d) = TF(w,d) \cdot IDF(w,d)$$

  $$IDF(w,d) = log(\frac{n_d}{1 + DF(w,d)})$$

  其中$DF(w,d)$是词在所有文本中的概率，他的频率越高，越说明文本间差异度不大，区别意义就越小。

- LDA向量
  ![](https://ws1.sinaimg.cn/large/6af92b9fgy1fu7velzv1vj20fe06b3yp.jpg)

  LDA是一个为文章提取主题并计算该文本对该主题归属度的概率，是一个三成贝叶斯模型（预料层、文档层和单词层）

  1、为整篇doc选定一个主题分布$\theta$, 而他是在corpus层面上的分布： $\theta \sim Dir(\alpha)$

  2、根据$\theta$ 的分布，为该文档选取一个主题 $z_n \sim Multi(\theta)$ , n的值（也就是主题数）可以自己设定

  3、在单词层面上生成词的概率 $P(w_n|z_n,\beta)$  ($\beta$ 是一个矩阵，主题数×单词数，每一行代表这个主题在各个词的Dir分布)

  由此得出文档的向量：

  $$P(\theta,\vec z,\vec w| \alpha,\beta) = P(\theta |\alpha) \prod_{n=1}^{N}P(z_n|\theta)P(w_n|z_n,\beta)$$

- LSI 向量

  LSI向量是用降维的思想对TF-IDF矩阵进行降为，因为不是方阵pca的特征分解不起作用，故采用奇异值分解的方式：

  $$A_{m \times n} = U_{m \times m}\Sigma_{m\times n}V_{n\times n}$$

  根据奇异值矩阵$\Sigma$取特征向量

```python
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
            sim = np.array(sim)
            sim_vec = np.mean(sim,axis = 0)
            most_sim_doc_id = heapq.nlargest(11,range(len(sim_vec)),sim_vec.take)
            doc_item['sim'] = most_sim_doc_id
            print(doc_item['name'],'已计算',most_sim_doc_id)

        with open('doc.json','w',encoding = 'gbk') as f:
            f.truncate()
            json.dump(doc,f)
        print('----------计算相似文档结束！---------')
```
这里使用了heapq数据结构求数组中前N个最大值的index. heapq是最小堆结构，可以很好地解决TOP-K问题：
heapq.nlargest(n,iter,key)   key和sort一样是作用在iter上的函数
而要输出TOP-K的index
这里很巧妙的key使用了ndarray.take 作用是取出对应Index的值
如果是一般的list ,此方法仍然可以使用:
```python
h = [3,5,6,7,10]
heapq.nlargest(3,range(len(h)),h.__getitem__)
# 这个list的内建方法取出index的值，但是不能像ndarray对象一样传入数组
没有使用数据库，将推荐结果统一写入到了josn文件中。
```

## rest接口编写
为方便前端测试访问，先使用Flask框架编写出接口的测试版本：

```Python
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
```

接口主要功能是读取json文件，提取响应id文档的推荐文档id

## 计算过程与结果演示

![](https://ws1.sinaimg.cn/large/6af92b9fgy1ftzy0qjanxj20hl06e0tm.jpg)

语料库与字典库的构建与更新

![](https://ws1.sinaimg.cn/large/6af92b9fgy1fu7we9pl32j20p70erjyn.jpg)

推荐结果写入txt.

