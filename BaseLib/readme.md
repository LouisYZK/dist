

```python
# 数据导出
import sqlite3
conn = sqlite3.connect('OTAcatch_tuniu_20180316.db')
cur = conn.cursor()
# 获取sqlite数据库中的表名称，无需下载navicate
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
table = cur.fetchall()
table
```




    [('tuniuItem',)]




```python
# 查询表结构
cur.execute("select * from sqlite_master WHERE type = 'table'")
table = cur.fetchall()
table
```




    [('table',
      'tuniuItem',
      'tuniuItem',
      2,
      'CREATE TABLE "tuniuItem" (\r\n"startCity"  TEXT,\r\n"destination"  TEXT,\r\n"addTime"  TEXT,\r\n"id"  INTEGER,\r\n"url"  TEXT,\r\n"type"  TEXT,\r\n"holiday"  TEXT,\r\n"line"  TEXT,\r\n"title"  TEXT,\r\n"label"  TEXT,\r\n"subtitle"  TEXT,\r\n"overview"  TEXT,\r\n"brand"  TEXT,\r\n"start"  TEXT,\r\n"price"  INTEGER,\r\n"commentSatNum"  INTEGER,\r\n"personNum"  INTEGER,\r\n"personComment"  INTEGER,\r\n"star"  INTEGER,\r\n"shoufuchufa"  INTEGER,\r\n"lijianyouhui"  INTEGER\r\n)')]


# SQL语句从数据提取数据，加载入pandas数据框中
sql = 'select startCity,destination,holiday,line,title,subtitle,overview,brand,start,price,commentSatNum, personNum,personComment ,star,shoufuchufa,lijianyouhui from tuniuItem'
# sql = 'select * from tuniuItem'
cur.execute(sql)
data = cur.fetchall()
import pandas as pd
df = pd.DataFrame(data = data,columns = ['startCity','destination','holiday','line','title','subtitle','overview','brand','start','price','commentSatNum', 'personNum','personComment' ,'star','shoufuchufa','lijianyouhui'])
df.head()

```python
# 去除二进制编码与中文转换
def trans(x):
    if len(x) == 0 :
        return x
    elif type(x) == bytes:
        return x.decode()
    elif x[0] == 'b':
        return eval(x).decode()
    else:
        return x
# df['holiday'].apply(trans).head()
col = ['holiday','line','title','subtitle','overview','brand','start']
for item in col:
    df[item] = df[item].apply(trans)
df.head(2)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>startCity</th>
      <th>destination</th>
      <th>holiday</th>
      <th>line</th>
      <th>title</th>
      <th>subtitle</th>
      <th>overview</th>
      <th>brand</th>
      <th>start</th>
      <th>price</th>
      <th>commentSatNum</th>
      <th>personNum</th>
      <th>personComment</th>
      <th>star</th>
      <th>shoufuchufa</th>
      <th>lijianyouhui</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>北京</td>
      <td>欧洲</td>
      <td>五一</td>
      <td>法国意大利瑞士13日游</td>
      <td>自营欧洲，万人出游，林志颖同款，意深四五星，5处世遗，庄园酒店，少女峰，金色快车，双宫双游船...</td>
      <td>北京出发 | 北京成团 | 庄园酒店 少女峰 五渔村 意深 一价全含</td>
      <td>琉森（卢塞恩），叹息桥，协和广场，比萨大教堂，圣马可教堂，罗马斗兽场，米开朗基罗广场，佛罗伦...</td>
      <td>牛人专线</td>
      <td>4月12日，4月19日，4月26日，5月2日，5月10日，5月17日</td>
      <td>16399</td>
      <td>97</td>
      <td>13642</td>
      <td>3472</td>
      <td>4</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>北京</td>
      <td>欧洲</td>
      <td>五一</td>
      <td>法国意大利瑞士12日游</td>
      <td>自营欧洲，5千人出游，全含，瑞士深度，少女峰，冰川3000，山顶特色餐，双宫双船，金色山口，...</td>
      <td>北京出发 | 北京成团 | 瑞深 楚格 少女峰 TGV+金色山口 一价全含</td>
      <td>琉森（卢塞恩），叹息桥，协和广场，卡佩尔桥和水塔，巴黎塞纳河游船，圣马可教堂，圣莫里茨，琉森...</td>
      <td>牛人专线</td>
      <td>4月4日，5月21日，5月30日，6月15日，6月27日，7月24日</td>
      <td>13583</td>
      <td>96</td>
      <td>5288</td>
      <td>1341</td>
      <td>3</td>
      <td>1</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>




```python
df['destination'].value_counts()
```




    泰国       73010
    欧洲       66337
    日本       41936
    中东非洲     32424
    香港       25433
    印度尼西亚    24770
    越南       23056
    马来西亚     15248
    新加坡      12007
    美国       11871
    台湾       11729
    澳新       11313
    柬埔寨       8760
    加拿大       3035
    马尔代夫       106
    Name: destination, dtype: int64




```python
df['startCity'].value_counts()
```




    南京    23955
    杭州    23945
    长沙    23444
    成都    23416
    厦门    23394
    昆明    23144
    北京    23087
    深圳    23066
    沈阳    22958
    广州    22905
    青岛    22836
    上海    22311
    天津    21859
    重庆    21176
    武汉    19898
    西安    19641
    Name: startCity, dtype: int64




```python
import matplotlib.pyplot as plt
import seaborn as sns

table = df.groupby(['startCity'])['personNum'].sum()
# sns.set_style("whitegrid")

# ax = sns.barplot(x = table.index,y = table.values,ci =0)
# ax.set_ylabel('出游人数总和')
from pyecharts import Bar
attr = table.index
value = table.values
bar = Bar('出游人数综合')
bar.add('出游人数',attr,value)
bar
```




<script>
    require.config({
        paths: {
            'echarts': '/nbextensions/echarts/echarts.min'
        }
    });
</script>
    <div id="82fa848b077342b4a1ba5b4031a0bdb1" style="width:800px;height:400px;"></div>


<script>
    require(['echarts'], function(echarts) {
        
var myChart_82fa848b077342b4a1ba5b4031a0bdb1 = echarts.init(document.getElementById('82fa848b077342b4a1ba5b4031a0bdb1'), 'light', {renderer: 'canvas'});

var option_82fa848b077342b4a1ba5b4031a0bdb1 = {
    "title": [
        {
            "text": "\u51fa\u6e38\u4eba\u6570\u7efc\u5408",
            "left": "auto",
            "top": "auto",
            "textStyle": {
                "fontSize": 18
            },
            "subtextStyle": {
                "fontSize": 12
            }
        }
    ],
    "toolbox": {
        "show": true,
        "orient": "vertical",
        "left": "95%",
        "top": "center",
        "feature": {
            "saveAsImage": {
                "show": true,
                "title": "save as image"
            },
            "restore": {
                "show": true,
                "title": "restore"
            },
            "dataView": {
                "show": true,
                "title": "data view"
            }
        }
    },
    "series_id": 572383,
    "tooltip": {
        "trigger": "item",
        "triggerOn": "mousemove|click",
        "axisPointer": {
            "type": "line"
        },
        "textStyle": {
            "fontSize": 14
        },
        "backgroundColor": "rgba(50,50,50,0.7)",
        "borderColor": "#333",
        "borderWidth": 0
    },
    "series": [
        {
            "type": "bar",
            "name": "\u51fa\u6e38\u4eba\u6570",
            "data": [
                1074625.0,
                965930.0,
                1082165.0,
                906434.0,
                929632.0,
                849924.0,
                921568.0,
                898995.0,
                1076638.0,
                938489.0,
                858816.0,
                848434.0,
                923962.0,
                931526.0,
                936738.0,
                936479.0
            ],
            "barCategoryGap": "20%",
            "label": {
                "normal": {
                    "show": false,
                    "position": "top",
                    "textStyle": {
                        "fontSize": 12
                    }
                },
                "emphasis": {
                    "show": true,
                    "textStyle": {
                        "fontSize": 12
                    }
                }
            },
            "markPoint": {
                "data": []
            },
            "markLine": {
                "data": []
            },
            "seriesId": 572383
        }
    ],
    "legend": [
        {
            "data": [
                "\u51fa\u6e38\u4eba\u6570"
            ],
            "selectedMode": "multiple",
            "show": true,
            "left": "center",
            "top": "top",
            "orient": "horizontal",
            "textStyle": {
                "fontSize": 12
            }
        }
    ],
    "animation": true,
    "xAxis": [
        {
            "show": true,
            "nameLocation": "middle",
            "nameGap": 25,
            "nameTextStyle": {
                "fontSize": 14
            },
            "axisTick": {
                "alignWithLabel": false
            },
            "inverse": false,
            "boundaryGap": true,
            "type": "category",
            "splitLine": {
                "show": false
            },
            "axisLine": {
                "lineStyle": {
                    "width": 1
                }
            },
            "axisLabel": {
                "interval": "auto",
                "rotate": 0,
                "margin": 8,
                "textStyle": {
                    "fontSize": 12
                }
            },
            "data": [
                "\u4e0a\u6d77",
                "\u5317\u4eac",
                "\u5357\u4eac",
                "\u53a6\u95e8",
                "\u5929\u6d25",
                "\u5e7f\u5dde",
                "\u6210\u90fd",
                "\u6606\u660e",
                "\u676d\u5dde",
                "\u6b66\u6c49",
                "\u6c88\u9633",
                "\u6df1\u5733",
                "\u897f\u5b89",
                "\u91cd\u5e86",
                "\u957f\u6c99",
                "\u9752\u5c9b"
            ]
        }
    ],
    "yAxis": [
        {
            "show": true,
            "nameLocation": "middle",
            "nameGap": 25,
            "nameTextStyle": {
                "fontSize": 14
            },
            "axisTick": {
                "alignWithLabel": false
            },
            "inverse": false,
            "boundaryGap": true,
            "type": "value",
            "splitLine": {
                "show": true
            },
            "axisLine": {
                "lineStyle": {
                    "width": 1
                }
            },
            "axisLabel": {
                "interval": "auto",
                "formatter": "{value} ",
                "rotate": 0,
                "margin": 8,
                "textStyle": {
                    "fontSize": 12
                }
            }
        }
    ],
    "color": [
        "#c23531",
        "#2f4554",
        "#61a0a8",
        "#d48265",
        "#749f83",
        "#ca8622",
        "#bda29a",
        "#6e7074",
        "#546570",
        "#c4ccd3",
        "#f05b72",
        "#ef5b9c",
        "#f47920",
        "#905a3d",
        "#fab27b",
        "#2a5caa",
        "#444693",
        "#726930",
        "#b2d235",
        "#6d8346",
        "#ac6767",
        "#1d953f",
        "#6950a1",
        "#918597",
        "#f6f5ec"
    ]
};
myChart_82fa848b077342b4a1ba5b4031a0bdb1.setOption(option_82fa848b077342b4a1ba5b4031a0bdb1);

    });
</script>





```python
table = df['startCity'].value_counts()
from pyecharts import Pie

attr = table.index
v1 = table.values
pie = Pie("出游城市产品数比例", title_pos='center')
pie.add("", attr, v1, radius=[40, 75], label_text_color=None, is_label_show=True,
        legend_orient='vertical', legend_pos='left')
pie
```




<script>
    require.config({
        paths: {
            'echarts': '/nbextensions/echarts/echarts.min'
        }
    });
</script>
    <div id="d6b63e5e75674947920309434920b954" style="width:800px;height:400px;"></div>


<script>
    require(['echarts'], function(echarts) {
        
var myChart_d6b63e5e75674947920309434920b954 = echarts.init(document.getElementById('d6b63e5e75674947920309434920b954'), 'light', {renderer: 'canvas'});

var option_d6b63e5e75674947920309434920b954 = {
    "title": [
        {
            "text": "\u51fa\u6e38\u57ce\u5e02\u4ea7\u54c1\u6570\u6bd4\u4f8b",
            "left": "center",
            "top": "auto",
            "textStyle": {
                "fontSize": 18
            },
            "subtextStyle": {
                "fontSize": 12
            }
        }
    ],
    "toolbox": {
        "show": true,
        "orient": "vertical",
        "left": "95%",
        "top": "center",
        "feature": {
            "saveAsImage": {
                "show": true,
                "title": "save as image"
            },
            "restore": {
                "show": true,
                "title": "restore"
            },
            "dataView": {
                "show": true,
                "title": "data view"
            }
        }
    },
    "series_id": 4436279,
    "tooltip": {
        "trigger": "item",
        "triggerOn": "mousemove|click",
        "axisPointer": {
            "type": "line"
        },
        "textStyle": {
            "fontSize": 14
        },
        "backgroundColor": "rgba(50,50,50,0.7)",
        "borderColor": "#333",
        "borderWidth": 0
    },
    "series": [
        {
            "type": "pie",
            "data": [
                {
                    "name": "\u5357\u4eac",
                    "value": 23955.0
                },
                {
                    "name": "\u676d\u5dde",
                    "value": 23945.0
                },
                {
                    "name": "\u957f\u6c99",
                    "value": 23444.0
                },
                {
                    "name": "\u6210\u90fd",
                    "value": 23416.0
                },
                {
                    "name": "\u53a6\u95e8",
                    "value": 23394.0
                },
                {
                    "name": "\u6606\u660e",
                    "value": 23144.0
                },
                {
                    "name": "\u5317\u4eac",
                    "value": 23087.0
                },
                {
                    "name": "\u6df1\u5733",
                    "value": 23066.0
                },
                {
                    "name": "\u6c88\u9633",
                    "value": 22958.0
                },
                {
                    "name": "\u5e7f\u5dde",
                    "value": 22905.0
                },
                {
                    "name": "\u9752\u5c9b",
                    "value": 22836.0
                },
                {
                    "name": "\u4e0a\u6d77",
                    "value": 22311.0
                },
                {
                    "name": "\u5929\u6d25",
                    "value": 21859.0
                },
                {
                    "name": "\u91cd\u5e86",
                    "value": 21176.0
                },
                {
                    "name": "\u6b66\u6c49",
                    "value": 19898.0
                },
                {
                    "name": "\u897f\u5b89",
                    "value": 19641.0
                }
            ],
            "radius": [
                "40%",
                "75%"
            ],
            "center": [
                "50%",
                "50%"
            ],
            "label": {
                "normal": {
                    "show": true,
                    "position": "outside",
                    "textStyle": {
                        "fontSize": 12
                    },
                    "formatter": "{b}: {d}%"
                },
                "emphasis": {
                    "show": true,
                    "textStyle": {
                        "fontSize": 12
                    },
                    "formatter": "{b}: {d}%"
                }
            },
            "seriesId": 4436279
        }
    ],
    "legend": [
        {
            "data": [
                "\u5357\u4eac",
                "\u676d\u5dde",
                "\u957f\u6c99",
                "\u6210\u90fd",
                "\u53a6\u95e8",
                "\u6606\u660e",
                "\u5317\u4eac",
                "\u6df1\u5733",
                "\u6c88\u9633",
                "\u5e7f\u5dde",
                "\u9752\u5c9b",
                "\u4e0a\u6d77",
                "\u5929\u6d25",
                "\u91cd\u5e86",
                "\u6b66\u6c49",
                "\u897f\u5b89"
            ],
            "selectedMode": "multiple",
            "show": true,
            "left": "left",
            "top": "top",
            "orient": "vertical",
            "textStyle": {
                "fontSize": 12
            }
        }
    ],
    "animation": true,
    "color": [
        "#c23531",
        "#2f4554",
        "#61a0a8",
        "#d48265",
        "#749f83",
        "#ca8622",
        "#bda29a",
        "#6e7074",
        "#546570",
        "#c4ccd3",
        "#f05b72",
        "#ef5b9c",
        "#f47920",
        "#905a3d",
        "#fab27b",
        "#2a5caa",
        "#444693",
        "#726930",
        "#b2d235",
        "#6d8346",
        "#ac6767",
        "#1d953f",
        "#6950a1",
        "#918597",
        "#f6f5ec"
    ]
};
myChart_d6b63e5e75674947920309434920b954.setOption(option_d6b63e5e75674947920309434920b954);

    });
</script>





```python
# sankey图
from pyecharts import Sankey
start = df['startCity'].unique().tolist()
desti = df['destination'].unique().tolist()
nodes = start + desti
# 定义出发城市和目的地地区为结点
Nodes = [{'name':item} for item in nodes]
# 制作以值为人数的数据透视表
piv_table = pd.pivot_table(df, index= 'startCity',columns = 'destination',values = 'personNum',aggfunc = 'sum')
piv_table = piv_table.fillna(0)
Links = [{'source':chufa,'target':daoda,'value':piv_table.loc[chufa,daoda]} for chufa in start for daoda in desti]
sankey = Sankey("出游地点热度", width=1200, height=600)
sankey.add(
    "sankey",
    Nodes,
    Links,
    line_opacity=0.6,
    line_curve=0.5,
    line_color="source",
    is_label_show=True,
    label_pos="right",
)
sankey
# sankey.render('sankey.html')
```




<script>
    require.config({
        paths: {
            'echarts': '/nbextensions/echarts/echarts.min'
        }
    });
</script>
    <div id="d74d02db7dad47d0a0dd71cde5f6158b" style="width:1200px;height:600px;"></div>


<script>
    require(['echarts'], function(echarts) {
        
var myChart_d74d02db7dad47d0a0dd71cde5f6158b = echarts.init(document.getElementById('d74d02db7dad47d0a0dd71cde5f6158b'), 'light', {renderer: 'canvas'});

var option_d74d02db7dad47d0a0dd71cde5f6158b = {
    "title": [
        {
            "text": "\u51fa\u6e38\u5730\u70b9\u70ed\u5ea6",
            "left": "auto",
            "top": "auto",
            "textStyle": {
                "fontSize": 18
            },
            "subtextStyle": {
                "fontSize": 12
            }
        }
    ],
    "toolbox": {
        "show": true,
        "orient": "vertical",
        "left": "95%",
        "top": "center",
        "feature": {
            "saveAsImage": {
                "show": true,
                "title": "save as image"
            },
            "restore": {
                "show": true,
                "title": "restore"
            },
            "dataView": {
                "show": true,
                "title": "data view"
            }
        }
    },
    "series_id": 3545398,
    "tooltip": {
        "trigger": "item",
        "triggerOn": "mousemove|click",
        "axisPointer": {
            "type": "line"
        },
        "textStyle": {
            "fontSize": 14
        },
        "backgroundColor": "rgba(50,50,50,0.7)",
        "borderColor": "#333",
        "borderWidth": 0
    },
    "series": [
        {
            "type": "sankey",
            "name": "sankey",
            "data": [
                {
                    "name": "\u5317\u4eac"
                },
                {
                    "name": "\u4e0a\u6d77"
                },
                {
                    "name": "\u5929\u6d25"
                },
                {
                    "name": "\u91cd\u5e86"
                },
                {
                    "name": "\u9752\u5c9b"
                },
                {
                    "name": "\u897f\u5b89"
                },
                {
                    "name": "\u5357\u4eac"
                },
                {
                    "name": "\u676d\u5dde"
                },
                {
                    "name": "\u53a6\u95e8"
                },
                {
                    "name": "\u6210\u90fd"
                },
                {
                    "name": "\u6df1\u5733"
                },
                {
                    "name": "\u5e7f\u5dde"
                },
                {
                    "name": "\u6606\u660e"
                },
                {
                    "name": "\u957f\u6c99"
                },
                {
                    "name": "\u6c88\u9633"
                },
                {
                    "name": "\u6b66\u6c49"
                },
                {
                    "name": "\u6b27\u6d32"
                },
                {
                    "name": "\u65e5\u672c"
                },
                {
                    "name": "\u9999\u6e2f"
                },
                {
                    "name": "\u53f0\u6e7e"
                },
                {
                    "name": "\u65b0\u52a0\u5761"
                },
                {
                    "name": "\u67ec\u57d4\u5be8"
                },
                {
                    "name": "\u6cf0\u56fd"
                },
                {
                    "name": "\u9a6c\u5c14\u4ee3\u592b"
                },
                {
                    "name": "\u8d8a\u5357"
                },
                {
                    "name": "\u7f8e\u56fd"
                },
                {
                    "name": "\u52a0\u62ff\u5927"
                },
                {
                    "name": "\u6fb3\u65b0"
                },
                {
                    "name": "\u4e2d\u4e1c\u975e\u6d32"
                },
                {
                    "name": "\u5370\u5ea6\u5c3c\u897f\u4e9a"
                },
                {
                    "name": "\u9a6c\u6765\u897f\u4e9a"
                }
            ],
            "links": [
                {
                    "source": "\u5317\u4eac",
                    "target": "\u6b27\u6d32",
                    "value": 267812.0
                },
                {
                    "source": "\u5317\u4eac",
                    "target": "\u65e5\u672c",
                    "value": 67193.0
                },
                {
                    "source": "\u5317\u4eac",
                    "target": "\u9999\u6e2f",
                    "value": 52847.0
                },
                {
                    "source": "\u5317\u4eac",
                    "target": "\u53f0\u6e7e",
                    "value": 29157.0
                },
                {
                    "source": "\u5317\u4eac",
                    "target": "\u65b0\u52a0\u5761",
                    "value": 23978.0
                },
                {
                    "source": "\u5317\u4eac",
                    "target": "\u67ec\u57d4\u5be8",
                    "value": 18161.0
                },
                {
                    "source": "\u5317\u4eac",
                    "target": "\u6cf0\u56fd",
                    "value": 250249.0
                },
                {
                    "source": "\u5317\u4eac",
                    "target": "\u9a6c\u5c14\u4ee3\u592b",
                    "value": 628.0
                },
                {
                    "source": "\u5317\u4eac",
                    "target": "\u8d8a\u5357",
                    "value": 29988.0
                },
                {
                    "source": "\u5317\u4eac",
                    "target": "\u7f8e\u56fd",
                    "value": 32641.0
                },
                {
                    "source": "\u5317\u4eac",
                    "target": "\u52a0\u62ff\u5927",
                    "value": 5889.0
                },
                {
                    "source": "\u5317\u4eac",
                    "target": "\u6fb3\u65b0",
                    "value": 17277.0
                },
                {
                    "source": "\u5317\u4eac",
                    "target": "\u4e2d\u4e1c\u975e\u6d32",
                    "value": 45416.0
                },
                {
                    "source": "\u5317\u4eac",
                    "target": "\u5370\u5ea6\u5c3c\u897f\u4e9a",
                    "value": 104374.0
                },
                {
                    "source": "\u5317\u4eac",
                    "target": "\u9a6c\u6765\u897f\u4e9a",
                    "value": 20320.0
                },
                {
                    "source": "\u4e0a\u6d77",
                    "target": "\u6b27\u6d32",
                    "value": 255778.0
                },
                {
                    "source": "\u4e0a\u6d77",
                    "target": "\u65e5\u672c",
                    "value": 105917.0
                },
                {
                    "source": "\u4e0a\u6d77",
                    "target": "\u9999\u6e2f",
                    "value": 54788.0
                },
                {
                    "source": "\u4e0a\u6d77",
                    "target": "\u53f0\u6e7e",
                    "value": 27892.0
                },
                {
                    "source": "\u4e0a\u6d77",
                    "target": "\u65b0\u52a0\u5761",
                    "value": 31218.0
                },
                {
                    "source": "\u4e0a\u6d77",
                    "target": "\u67ec\u57d4\u5be8",
                    "value": 17464.0
                },
                {
                    "source": "\u4e0a\u6d77",
                    "target": "\u6cf0\u56fd",
                    "value": 300073.0
                },
                {
                    "source": "\u4e0a\u6d77",
                    "target": "\u9a6c\u5c14\u4ee3\u592b",
                    "value": 208.0
                },
                {
                    "source": "\u4e0a\u6d77",
                    "target": "\u8d8a\u5357",
                    "value": 41752.0
                },
                {
                    "source": "\u4e0a\u6d77",
                    "target": "\u7f8e\u56fd",
                    "value": 32636.0
                },
                {
                    "source": "\u4e0a\u6d77",
                    "target": "\u52a0\u62ff\u5927",
                    "value": 5889.0
                },
                {
                    "source": "\u4e0a\u6d77",
                    "target": "\u6fb3\u65b0",
                    "value": 17976.0
                },
                {
                    "source": "\u4e0a\u6d77",
                    "target": "\u4e2d\u4e1c\u975e\u6d32",
                    "value": 58782.0
                },
                {
                    "source": "\u4e0a\u6d77",
                    "target": "\u5370\u5ea6\u5c3c\u897f\u4e9a",
                    "value": 95545.0
                },
                {
                    "source": "\u4e0a\u6d77",
                    "target": "\u9a6c\u6765\u897f\u4e9a",
                    "value": 28707.0
                },
                {
                    "source": "\u5929\u6d25",
                    "target": "\u6b27\u6d32",
                    "value": 254039.0
                },
                {
                    "source": "\u5929\u6d25",
                    "target": "\u65e5\u672c",
                    "value": 68581.0
                },
                {
                    "source": "\u5929\u6d25",
                    "target": "\u9999\u6e2f",
                    "value": 52642.0
                },
                {
                    "source": "\u5929\u6d25",
                    "target": "\u53f0\u6e7e",
                    "value": 29157.0
                },
                {
                    "source": "\u5929\u6d25",
                    "target": "\u65b0\u52a0\u5761",
                    "value": 23114.0
                },
                {
                    "source": "\u5929\u6d25",
                    "target": "\u67ec\u57d4\u5be8",
                    "value": 18143.0
                },
                {
                    "source": "\u5929\u6d25",
                    "target": "\u6cf0\u56fd",
                    "value": 250053.0
                },
                {
                    "source": "\u5929\u6d25",
                    "target": "\u9a6c\u5c14\u4ee3\u592b",
                    "value": 628.0
                },
                {
                    "source": "\u5929\u6d25",
                    "target": "\u8d8a\u5357",
                    "value": 29314.0
                },
                {
                    "source": "\u5929\u6d25",
                    "target": "\u7f8e\u56fd",
                    "value": 32576.0
                },
                {
                    "source": "\u5929\u6d25",
                    "target": "\u52a0\u62ff\u5927",
                    "value": 5889.0
                },
                {
                    "source": "\u5929\u6d25",
                    "target": "\u6fb3\u65b0",
                    "value": 17267.0
                },
                {
                    "source": "\u5929\u6d25",
                    "target": "\u4e2d\u4e1c\u975e\u6d32",
                    "value": 44776.0
                },
                {
                    "source": "\u5929\u6d25",
                    "target": "\u5370\u5ea6\u5c3c\u897f\u4e9a",
                    "value": 103453.0
                },
                {
                    "source": "\u5929\u6d25",
                    "target": "\u9a6c\u6765\u897f\u4e9a",
                    "value": 0.0
                },
                {
                    "source": "\u91cd\u5e86",
                    "target": "\u6b27\u6d32",
                    "value": 255904.0
                },
                {
                    "source": "\u91cd\u5e86",
                    "target": "\u65e5\u672c",
                    "value": 15868.0
                },
                {
                    "source": "\u91cd\u5e86",
                    "target": "\u9999\u6e2f",
                    "value": 52573.0
                },
                {
                    "source": "\u91cd\u5e86",
                    "target": "\u53f0\u6e7e",
                    "value": 27892.0
                },
                {
                    "source": "\u91cd\u5e86",
                    "target": "\u65b0\u52a0\u5761",
                    "value": 29633.0
                },
                {
                    "source": "\u91cd\u5e86",
                    "target": "\u67ec\u57d4\u5be8",
                    "value": 12647.0
                },
                {
                    "source": "\u91cd\u5e86",
                    "target": "\u6cf0\u56fd",
                    "value": 287125.0
                },
                {
                    "source": "\u91cd\u5e86",
                    "target": "\u9a6c\u5c14\u4ee3\u592b",
                    "value": 208.0
                },
                {
                    "source": "\u91cd\u5e86",
                    "target": "\u8d8a\u5357",
                    "value": 23309.0
                },
                {
                    "source": "\u91cd\u5e86",
                    "target": "\u7f8e\u56fd",
                    "value": 32573.0
                },
                {
                    "source": "\u91cd\u5e86",
                    "target": "\u52a0\u62ff\u5927",
                    "value": 5889.0
                },
                {
                    "source": "\u91cd\u5e86",
                    "target": "\u6fb3\u65b0",
                    "value": 17233.0
                },
                {
                    "source": "\u91cd\u5e86",
                    "target": "\u4e2d\u4e1c\u975e\u6d32",
                    "value": 55293.0
                },
                {
                    "source": "\u91cd\u5e86",
                    "target": "\u5370\u5ea6\u5c3c\u897f\u4e9a",
                    "value": 87573.0
                },
                {
                    "source": "\u91cd\u5e86",
                    "target": "\u9a6c\u6765\u897f\u4e9a",
                    "value": 27806.0
                },
                {
                    "source": "\u9752\u5c9b",
                    "target": "\u6b27\u6d32",
                    "value": 254333.0
                },
                {
                    "source": "\u9752\u5c9b",
                    "target": "\u65e5\u672c",
                    "value": 7857.0
                },
                {
                    "source": "\u9752\u5c9b",
                    "target": "\u9999\u6e2f",
                    "value": 52849.0
                },
                {
                    "source": "\u9752\u5c9b",
                    "target": "\u53f0\u6e7e",
                    "value": 27892.0
                },
                {
                    "source": "\u9752\u5c9b",
                    "target": "\u65b0\u52a0\u5761",
                    "value": 31105.0
                },
                {
                    "source": "\u9752\u5c9b",
                    "target": "\u67ec\u57d4\u5be8",
                    "value": 17513.0
                },
                {
                    "source": "\u9752\u5c9b",
                    "target": "\u6cf0\u56fd",
                    "value": 290434.0
                },
                {
                    "source": "\u9752\u5c9b",
                    "target": "\u9a6c\u5c14\u4ee3\u592b",
                    "value": 628.0
                },
                {
                    "source": "\u9752\u5c9b",
                    "target": "\u8d8a\u5357",
                    "value": 30118.0
                },
                {
                    "source": "\u9752\u5c9b",
                    "target": "\u7f8e\u56fd",
                    "value": 32525.0
                },
                {
                    "source": "\u9752\u5c9b",
                    "target": "\u52a0\u62ff\u5927",
                    "value": 5889.0
                },
                {
                    "source": "\u9752\u5c9b",
                    "target": "\u6fb3\u65b0",
                    "value": 17261.0
                },
                {
                    "source": "\u9752\u5c9b",
                    "target": "\u4e2d\u4e1c\u975e\u6d32",
                    "value": 45127.0
                },
                {
                    "source": "\u9752\u5c9b",
                    "target": "\u5370\u5ea6\u5c3c\u897f\u4e9a",
                    "value": 95479.0
                },
                {
                    "source": "\u9752\u5c9b",
                    "target": "\u9a6c\u6765\u897f\u4e9a",
                    "value": 27469.0
                },
                {
                    "source": "\u897f\u5b89",
                    "target": "\u6b27\u6d32",
                    "value": 251255.0
                },
                {
                    "source": "\u897f\u5b89",
                    "target": "\u65e5\u672c",
                    "value": 46903.0
                },
                {
                    "source": "\u897f\u5b89",
                    "target": "\u9999\u6e2f",
                    "value": 52566.0
                },
                {
                    "source": "\u897f\u5b89",
                    "target": "\u53f0\u6e7e",
                    "value": 591.0
                },
                {
                    "source": "\u897f\u5b89",
                    "target": "\u65b0\u52a0\u5761",
                    "value": 25868.0
                },
                {
                    "source": "\u897f\u5b89",
                    "target": "\u67ec\u57d4\u5be8",
                    "value": 18397.0
                },
                {
                    "source": "\u897f\u5b89",
                    "target": "\u6cf0\u56fd",
                    "value": 282543.0
                },
                {
                    "source": "\u897f\u5b89",
                    "target": "\u9a6c\u5c14\u4ee3\u592b",
                    "value": 628.0
                },
                {
                    "source": "\u897f\u5b89",
                    "target": "\u8d8a\u5357",
                    "value": 29381.0
                },
                {
                    "source": "\u897f\u5b89",
                    "target": "\u7f8e\u56fd",
                    "value": 32606.0
                },
                {
                    "source": "\u897f\u5b89",
                    "target": "\u52a0\u62ff\u5927",
                    "value": 5889.0
                },
                {
                    "source": "\u897f\u5b89",
                    "target": "\u6fb3\u65b0",
                    "value": 17236.0
                },
                {
                    "source": "\u897f\u5b89",
                    "target": "\u4e2d\u4e1c\u975e\u6d32",
                    "value": 48436.0
                },
                {
                    "source": "\u897f\u5b89",
                    "target": "\u5370\u5ea6\u5c3c\u897f\u4e9a",
                    "value": 86131.0
                },
                {
                    "source": "\u897f\u5b89",
                    "target": "\u9a6c\u6765\u897f\u4e9a",
                    "value": 25532.0
                },
                {
                    "source": "\u5357\u4eac",
                    "target": "\u6b27\u6d32",
                    "value": 254106.0
                },
                {
                    "source": "\u5357\u4eac",
                    "target": "\u65e5\u672c",
                    "value": 106249.0
                },
                {
                    "source": "\u5357\u4eac",
                    "target": "\u9999\u6e2f",
                    "value": 54872.0
                },
                {
                    "source": "\u5357\u4eac",
                    "target": "\u53f0\u6e7e",
                    "value": 28053.0
                },
                {
                    "source": "\u5357\u4eac",
                    "target": "\u65b0\u52a0\u5761",
                    "value": 31058.0
                },
                {
                    "source": "\u5357\u4eac",
                    "target": "\u67ec\u57d4\u5be8",
                    "value": 16605.0
                },
                {
                    "source": "\u5357\u4eac",
                    "target": "\u6cf0\u56fd",
                    "value": 303542.0
                },
                {
                    "source": "\u5357\u4eac",
                    "target": "\u9a6c\u5c14\u4ee3\u592b",
                    "value": 208.0
                },
                {
                    "source": "\u5357\u4eac",
                    "target": "\u8d8a\u5357",
                    "value": 43687.0
                },
                {
                    "source": "\u5357\u4eac",
                    "target": "\u7f8e\u56fd",
                    "value": 32669.0
                },
                {
                    "source": "\u5357\u4eac",
                    "target": "\u52a0\u62ff\u5927",
                    "value": 5889.0
                },
                {
                    "source": "\u5357\u4eac",
                    "target": "\u6fb3\u65b0",
                    "value": 17966.0
                },
                {
                    "source": "\u5357\u4eac",
                    "target": "\u4e2d\u4e1c\u975e\u6d32",
                    "value": 63182.0
                },
                {
                    "source": "\u5357\u4eac",
                    "target": "\u5370\u5ea6\u5c3c\u897f\u4e9a",
                    "value": 95659.0
                },
                {
                    "source": "\u5357\u4eac",
                    "target": "\u9a6c\u6765\u897f\u4e9a",
                    "value": 28420.0
                },
                {
                    "source": "\u676d\u5dde",
                    "target": "\u6b27\u6d32",
                    "value": 254106.0
                },
                {
                    "source": "\u676d\u5dde",
                    "target": "\u65e5\u672c",
                    "value": 106241.0
                },
                {
                    "source": "\u676d\u5dde",
                    "target": "\u9999\u6e2f",
                    "value": 54768.0
                },
                {
                    "source": "\u676d\u5dde",
                    "target": "\u53f0\u6e7e",
                    "value": 28053.0
                },
                {
                    "source": "\u676d\u5dde",
                    "target": "\u65b0\u52a0\u5761",
                    "value": 30741.0
                },
                {
                    "source": "\u676d\u5dde",
                    "target": "\u67ec\u57d4\u5be8",
                    "value": 16613.0
                },
                {
                    "source": "\u676d\u5dde",
                    "target": "\u6cf0\u56fd",
                    "value": 305023.0
                },
                {
                    "source": "\u676d\u5dde",
                    "target": "\u9a6c\u5c14\u4ee3\u592b",
                    "value": 208.0
                },
                {
                    "source": "\u676d\u5dde",
                    "target": "\u8d8a\u5357",
                    "value": 40969.0
                },
                {
                    "source": "\u676d\u5dde",
                    "target": "\u7f8e\u56fd",
                    "value": 32654.0
                },
                {
                    "source": "\u676d\u5dde",
                    "target": "\u52a0\u62ff\u5927",
                    "value": 5889.0
                },
                {
                    "source": "\u676d\u5dde",
                    "target": "\u6fb3\u65b0",
                    "value": 17979.0
                },
                {
                    "source": "\u676d\u5dde",
                    "target": "\u4e2d\u4e1c\u975e\u6d32",
                    "value": 59645.0
                },
                {
                    "source": "\u676d\u5dde",
                    "target": "\u5370\u5ea6\u5c3c\u897f\u4e9a",
                    "value": 95045.0
                },
                {
                    "source": "\u676d\u5dde",
                    "target": "\u9a6c\u6765\u897f\u4e9a",
                    "value": 28704.0
                },
                {
                    "source": "\u53a6\u95e8",
                    "target": "\u6b27\u6d32",
                    "value": 254295.0
                },
                {
                    "source": "\u53a6\u95e8",
                    "target": "\u65e5\u672c",
                    "value": 19306.0
                },
                {
                    "source": "\u53a6\u95e8",
                    "target": "\u9999\u6e2f",
                    "value": 52569.0
                },
                {
                    "source": "\u53a6\u95e8",
                    "target": "\u53f0\u6e7e",
                    "value": 28053.0
                },
                {
                    "source": "\u53a6\u95e8",
                    "target": "\u65b0\u52a0\u5761",
                    "value": 28633.0
                },
                {
                    "source": "\u53a6\u95e8",
                    "target": "\u67ec\u57d4\u5be8",
                    "value": 13114.0
                },
                {
                    "source": "\u53a6\u95e8",
                    "target": "\u6cf0\u56fd",
                    "value": 275993.0
                },
                {
                    "source": "\u53a6\u95e8",
                    "target": "\u9a6c\u5c14\u4ee3\u592b",
                    "value": 208.0
                },
                {
                    "source": "\u53a6\u95e8",
                    "target": "\u8d8a\u5357",
                    "value": 24304.0
                },
                {
                    "source": "\u53a6\u95e8",
                    "target": "\u7f8e\u56fd",
                    "value": 32600.0
                },
                {
                    "source": "\u53a6\u95e8",
                    "target": "\u52a0\u62ff\u5927",
                    "value": 5889.0
                },
                {
                    "source": "\u53a6\u95e8",
                    "target": "\u6fb3\u65b0",
                    "value": 17422.0
                },
                {
                    "source": "\u53a6\u95e8",
                    "target": "\u4e2d\u4e1c\u975e\u6d32",
                    "value": 34238.0
                },
                {
                    "source": "\u53a6\u95e8",
                    "target": "\u5370\u5ea6\u5c3c\u897f\u4e9a",
                    "value": 94488.0
                },
                {
                    "source": "\u53a6\u95e8",
                    "target": "\u9a6c\u6765\u897f\u4e9a",
                    "value": 25322.0
                },
                {
                    "source": "\u6210\u90fd",
                    "target": "\u6b27\u6d32",
                    "value": 255043.0
                },
                {
                    "source": "\u6210\u90fd",
                    "target": "\u65e5\u672c",
                    "value": 13158.0
                },
                {
                    "source": "\u6210\u90fd",
                    "target": "\u9999\u6e2f",
                    "value": 52559.0
                },
                {
                    "source": "\u6210\u90fd",
                    "target": "\u53f0\u6e7e",
                    "value": 28053.0
                },
                {
                    "source": "\u6210\u90fd",
                    "target": "\u65b0\u52a0\u5761",
                    "value": 27543.0
                },
                {
                    "source": "\u6210\u90fd",
                    "target": "\u67ec\u57d4\u5be8",
                    "value": 12704.0
                },
                {
                    "source": "\u6210\u90fd",
                    "target": "\u6cf0\u56fd",
                    "value": 283914.0
                },
                {
                    "source": "\u6210\u90fd",
                    "target": "\u9a6c\u5c14\u4ee3\u592b",
                    "value": 208.0
                },
                {
                    "source": "\u6210\u90fd",
                    "target": "\u8d8a\u5357",
                    "value": 23391.0
                },
                {
                    "source": "\u6210\u90fd",
                    "target": "\u7f8e\u56fd",
                    "value": 32657.0
                },
                {
                    "source": "\u6210\u90fd",
                    "target": "\u52a0\u62ff\u5927",
                    "value": 5889.0
                },
                {
                    "source": "\u6210\u90fd",
                    "target": "\u6fb3\u65b0",
                    "value": 17248.0
                },
                {
                    "source": "\u6210\u90fd",
                    "target": "\u4e2d\u4e1c\u975e\u6d32",
                    "value": 54332.0
                },
                {
                    "source": "\u6210\u90fd",
                    "target": "\u5370\u5ea6\u5c3c\u897f\u4e9a",
                    "value": 89119.0
                },
                {
                    "source": "\u6210\u90fd",
                    "target": "\u9a6c\u6765\u897f\u4e9a",
                    "value": 25750.0
                },
                {
                    "source": "\u6df1\u5733",
                    "target": "\u6b27\u6d32",
                    "value": 254431.0
                },
                {
                    "source": "\u6df1\u5733",
                    "target": "\u65e5\u672c",
                    "value": 20750.0
                },
                {
                    "source": "\u6df1\u5733",
                    "target": "\u9999\u6e2f",
                    "value": 48709.0
                },
                {
                    "source": "\u6df1\u5733",
                    "target": "\u53f0\u6e7e",
                    "value": 28053.0
                },
                {
                    "source": "\u6df1\u5733",
                    "target": "\u65b0\u52a0\u5761",
                    "value": 21768.0
                },
                {
                    "source": "\u6df1\u5733",
                    "target": "\u67ec\u57d4\u5be8",
                    "value": 12205.0
                },
                {
                    "source": "\u6df1\u5733",
                    "target": "\u6cf0\u56fd",
                    "value": 235748.0
                },
                {
                    "source": "\u6df1\u5733",
                    "target": "\u9a6c\u5c14\u4ee3\u592b",
                    "value": 208.0
                },
                {
                    "source": "\u6df1\u5733",
                    "target": "\u8d8a\u5357",
                    "value": 28577.0
                },
                {
                    "source": "\u6df1\u5733",
                    "target": "\u7f8e\u56fd",
                    "value": 32605.0
                },
                {
                    "source": "\u6df1\u5733",
                    "target": "\u52a0\u62ff\u5927",
                    "value": 5889.0
                },
                {
                    "source": "\u6df1\u5733",
                    "target": "\u6fb3\u65b0",
                    "value": 17218.0
                },
                {
                    "source": "\u6df1\u5733",
                    "target": "\u4e2d\u4e1c\u975e\u6d32",
                    "value": 29248.0
                },
                {
                    "source": "\u6df1\u5733",
                    "target": "\u5370\u5ea6\u5c3c\u897f\u4e9a",
                    "value": 92146.0
                },
                {
                    "source": "\u6df1\u5733",
                    "target": "\u9a6c\u6765\u897f\u4e9a",
                    "value": 20879.0
                },
                {
                    "source": "\u5e7f\u5dde",
                    "target": "\u6b27\u6d32",
                    "value": 254016.0
                },
                {
                    "source": "\u5e7f\u5dde",
                    "target": "\u65e5\u672c",
                    "value": 21556.0
                },
                {
                    "source": "\u5e7f\u5dde",
                    "target": "\u9999\u6e2f",
                    "value": 50678.0
                },
                {
                    "source": "\u5e7f\u5dde",
                    "target": "\u53f0\u6e7e",
                    "value": 27940.0
                },
                {
                    "source": "\u5e7f\u5dde",
                    "target": "\u65b0\u52a0\u5761",
                    "value": 21950.0
                },
                {
                    "source": "\u5e7f\u5dde",
                    "target": "\u67ec\u57d4\u5be8",
                    "value": 12205.0
                },
                {
                    "source": "\u5e7f\u5dde",
                    "target": "\u6cf0\u56fd",
                    "value": 236174.0
                },
                {
                    "source": "\u5e7f\u5dde",
                    "target": "\u9a6c\u5c14\u4ee3\u592b",
                    "value": 208.0
                },
                {
                    "source": "\u5e7f\u5dde",
                    "target": "\u8d8a\u5357",
                    "value": 26911.0
                },
                {
                    "source": "\u5e7f\u5dde",
                    "target": "\u7f8e\u56fd",
                    "value": 32685.0
                },
                {
                    "source": "\u5e7f\u5dde",
                    "target": "\u52a0\u62ff\u5927",
                    "value": 5892.0
                },
                {
                    "source": "\u5e7f\u5dde",
                    "target": "\u6fb3\u65b0",
                    "value": 17212.0
                },
                {
                    "source": "\u5e7f\u5dde",
                    "target": "\u4e2d\u4e1c\u975e\u6d32",
                    "value": 29291.0
                },
                {
                    "source": "\u5e7f\u5dde",
                    "target": "\u5370\u5ea6\u5c3c\u897f\u4e9a",
                    "value": 92169.0
                },
                {
                    "source": "\u5e7f\u5dde",
                    "target": "\u9a6c\u6765\u897f\u4e9a",
                    "value": 21037.0
                },
                {
                    "source": "\u6606\u660e",
                    "target": "\u6b27\u6d32",
                    "value": 254853.0
                },
                {
                    "source": "\u6606\u660e",
                    "target": "\u65e5\u672c",
                    "value": 12555.0
                },
                {
                    "source": "\u6606\u660e",
                    "target": "\u9999\u6e2f",
                    "value": 52573.0
                },
                {
                    "source": "\u6606\u660e",
                    "target": "\u53f0\u6e7e",
                    "value": 27940.0
                },
                {
                    "source": "\u6606\u660e",
                    "target": "\u65b0\u52a0\u5761",
                    "value": 27361.0
                },
                {
                    "source": "\u6606\u660e",
                    "target": "\u67ec\u57d4\u5be8",
                    "value": 12661.0
                },
                {
                    "source": "\u6606\u660e",
                    "target": "\u6cf0\u56fd",
                    "value": 278322.0
                },
                {
                    "source": "\u6606\u660e",
                    "target": "\u9a6c\u5c14\u4ee3\u592b",
                    "value": 208.0
                },
                {
                    "source": "\u6606\u660e",
                    "target": "\u8d8a\u5357",
                    "value": 22876.0
                },
                {
                    "source": "\u6606\u660e",
                    "target": "\u7f8e\u56fd",
                    "value": 32395.0
                },
                {
                    "source": "\u6606\u660e",
                    "target": "\u52a0\u62ff\u5927",
                    "value": 5892.0
                },
                {
                    "source": "\u6606\u660e",
                    "target": "\u6fb3\u65b0",
                    "value": 17163.0
                },
                {
                    "source": "\u6606\u660e",
                    "target": "\u4e2d\u4e1c\u975e\u6d32",
                    "value": 64454.0
                },
                {
                    "source": "\u6606\u660e",
                    "target": "\u5370\u5ea6\u5c3c\u897f\u4e9a",
                    "value": 64198.0
                },
                {
                    "source": "\u6606\u660e",
                    "target": "\u9a6c\u6765\u897f\u4e9a",
                    "value": 25544.0
                },
                {
                    "source": "\u957f\u6c99",
                    "target": "\u6b27\u6d32",
                    "value": 255560.0
                },
                {
                    "source": "\u957f\u6c99",
                    "target": "\u65e5\u672c",
                    "value": 47337.0
                },
                {
                    "source": "\u957f\u6c99",
                    "target": "\u9999\u6e2f",
                    "value": 52489.0
                },
                {
                    "source": "\u957f\u6c99",
                    "target": "\u53f0\u6e7e",
                    "value": 27940.0
                },
                {
                    "source": "\u957f\u6c99",
                    "target": "\u65b0\u52a0\u5761",
                    "value": 29603.0
                },
                {
                    "source": "\u957f\u6c99",
                    "target": "\u67ec\u57d4\u5be8",
                    "value": 14430.0
                },
                {
                    "source": "\u957f\u6c99",
                    "target": "\u6cf0\u56fd",
                    "value": 242772.0
                },
                {
                    "source": "\u957f\u6c99",
                    "target": "\u9a6c\u5c14\u4ee3\u592b",
                    "value": 208.0
                },
                {
                    "source": "\u957f\u6c99",
                    "target": "\u8d8a\u5357",
                    "value": 24590.0
                },
                {
                    "source": "\u957f\u6c99",
                    "target": "\u7f8e\u56fd",
                    "value": 32626.0
                },
                {
                    "source": "\u957f\u6c99",
                    "target": "\u52a0\u62ff\u5927",
                    "value": 5892.0
                },
                {
                    "source": "\u957f\u6c99",
                    "target": "\u6fb3\u65b0",
                    "value": 17348.0
                },
                {
                    "source": "\u957f\u6c99",
                    "target": "\u4e2d\u4e1c\u975e\u6d32",
                    "value": 80421.0
                },
                {
                    "source": "\u957f\u6c99",
                    "target": "\u5370\u5ea6\u5c3c\u897f\u4e9a",
                    "value": 79348.0
                },
                {
                    "source": "\u957f\u6c99",
                    "target": "\u9a6c\u6765\u897f\u4e9a",
                    "value": 26174.0
                },
                {
                    "source": "\u6c88\u9633",
                    "target": "\u6b27\u6d32",
                    "value": 211403.0
                },
                {
                    "source": "\u6c88\u9633",
                    "target": "\u65e5\u672c",
                    "value": 8321.0
                },
                {
                    "source": "\u6c88\u9633",
                    "target": "\u9999\u6e2f",
                    "value": 52686.0
                },
                {
                    "source": "\u6c88\u9633",
                    "target": "\u53f0\u6e7e",
                    "value": 27975.0
                },
                {
                    "source": "\u6c88\u9633",
                    "target": "\u65b0\u52a0\u5761",
                    "value": 26288.0
                },
                {
                    "source": "\u6c88\u9633",
                    "target": "\u67ec\u57d4\u5be8",
                    "value": 18407.0
                },
                {
                    "source": "\u6c88\u9633",
                    "target": "\u6cf0\u56fd",
                    "value": 277143.0
                },
                {
                    "source": "\u6c88\u9633",
                    "target": "\u9a6c\u5c14\u4ee3\u592b",
                    "value": 628.0
                },
                {
                    "source": "\u6c88\u9633",
                    "target": "\u8d8a\u5357",
                    "value": 28185.0
                },
                {
                    "source": "\u6c88\u9633",
                    "target": "\u7f8e\u56fd",
                    "value": 32670.0
                },
                {
                    "source": "\u6c88\u9633",
                    "target": "\u52a0\u62ff\u5927",
                    "value": 5892.0
                },
                {
                    "source": "\u6c88\u9633",
                    "target": "\u6fb3\u65b0",
                    "value": 17255.0
                },
                {
                    "source": "\u6c88\u9633",
                    "target": "\u4e2d\u4e1c\u975e\u6d32",
                    "value": 45604.0
                },
                {
                    "source": "\u6c88\u9633",
                    "target": "\u5370\u5ea6\u5c3c\u897f\u4e9a",
                    "value": 81574.0
                },
                {
                    "source": "\u6c88\u9633",
                    "target": "\u9a6c\u6765\u897f\u4e9a",
                    "value": 24785.0
                },
                {
                    "source": "\u6b66\u6c49",
                    "target": "\u6b27\u6d32",
                    "value": 256982.0
                },
                {
                    "source": "\u6b66\u6c49",
                    "target": "\u65e5\u672c",
                    "value": 52029.0
                },
                {
                    "source": "\u6b66\u6c49",
                    "target": "\u9999\u6e2f",
                    "value": 52802.0
                },
                {
                    "source": "\u6b66\u6c49",
                    "target": "\u53f0\u6e7e",
                    "value": 626.0
                },
                {
                    "source": "\u6b66\u6c49",
                    "target": "\u65b0\u52a0\u5761",
                    "value": 29339.0
                },
                {
                    "source": "\u6b66\u6c49",
                    "target": "\u67ec\u57d4\u5be8",
                    "value": 16169.0
                },
                {
                    "source": "\u6b66\u6c49",
                    "target": "\u6cf0\u56fd",
                    "value": 244699.0
                },
                {
                    "source": "\u6b66\u6c49",
                    "target": "\u9a6c\u5c14\u4ee3\u592b",
                    "value": 208.0
                },
                {
                    "source": "\u6b66\u6c49",
                    "target": "\u8d8a\u5357",
                    "value": 27434.0
                },
                {
                    "source": "\u6b66\u6c49",
                    "target": "\u7f8e\u56fd",
                    "value": 32722.0
                },
                {
                    "source": "\u6b66\u6c49",
                    "target": "\u52a0\u62ff\u5927",
                    "value": 5902.0
                },
                {
                    "source": "\u6b66\u6c49",
                    "target": "\u6fb3\u65b0",
                    "value": 17383.0
                },
                {
                    "source": "\u6b66\u6c49",
                    "target": "\u4e2d\u4e1c\u975e\u6d32",
                    "value": 81236.0
                },
                {
                    "source": "\u6b66\u6c49",
                    "target": "\u5370\u5ea6\u5c3c\u897f\u4e9a",
                    "value": 94903.0
                },
                {
                    "source": "\u6b66\u6c49",
                    "target": "\u9a6c\u6765\u897f\u4e9a",
                    "value": 26055.0
                }
            ],
            "nodeWidth": 20,
            "nodeGap": 8,
            "label": {
                "normal": {
                    "show": true,
                    "position": "right",
                    "textStyle": {
                        "fontSize": 12
                    }
                },
                "emphasis": {
                    "show": true,
                    "textStyle": {
                        "fontSize": 12
                    }
                }
            },
            "lineStyle": {
                "normal": {
                    "width": 1,
                    "opacity": 0.6,
                    "curveness": 0.5,
                    "type": "solid",
                    "color": "source"
                }
            }
        }
    ],
    "legend": [
        {
            "data": [
                "sankey"
            ],
            "selectedMode": "multiple",
            "show": true,
            "left": "center",
            "top": "top",
            "orient": "horizontal",
            "textStyle": {
                "fontSize": 12
            }
        }
    ],
    "animation": true,
    "color": [
        "#c23531",
        "#2f4554",
        "#61a0a8",
        "#d48265",
        "#749f83",
        "#ca8622",
        "#bda29a",
        "#6e7074",
        "#546570",
        "#c4ccd3",
        "#f05b72",
        "#ef5b9c",
        "#f47920",
        "#905a3d",
        "#fab27b",
        "#2a5caa",
        "#444693",
        "#726930",
        "#b2d235",
        "#6d8346",
        "#ac6767",
        "#1d953f",
        "#6950a1",
        "#918597",
        "#f6f5ec"
    ]
};
myChart_d74d02db7dad47d0a0dd71cde5f6158b.setOption(option_d74d02db7dad47d0a0dd71cde5f6158b);

    });
</script>





```python
# 其他描述性统计
```
