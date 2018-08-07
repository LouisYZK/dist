# 基于文本内容的推荐系统开发日记
这里将会涉及：
- 推荐模型逻辑
- 算法基本实现与测试（gensim等模块的调用）
- 内存溢出问题的解决
- 编写Python rest 服务接口
## 推荐模型逻辑
![模块逻辑类图](https://ws1.sinaimg.cn/large/6af92b9fgy1fu13zbjhwoj20t90hn40u.jpg)

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
字典就是输入目前所有文本分词结果
