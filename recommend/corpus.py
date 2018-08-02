import osp
import codecs
import re
import jieba
import datetime
class Corpus():
    stopwords = []
    stopword_filepath="./stopwordList/stopword.txt"
    def __init__(self,dir):
        self.__readin_stop()
        self.dir = dir
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
            with open('./doc/'+doc_item,'r') as f:
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

def test():
    print("execute",datetime.datetime.now())
def time_run():
    while True:
        now = datetime.datetime.now()
        if now.second%5 == 0:
            test()
