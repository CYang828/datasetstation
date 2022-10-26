# datasetstation

<!-- <p align="center">
    <img src="http://aimaksen.bslience.cn/china-datasets-logo.jpg">
</p> -->

<!-- <p align="center">
    <a href="https://github.com/CYang828/china-datasets">
        <img src="https://travis-ci.org/CYang828/china-datasets.svg?branch=master" alt="fastweb">
    </a>
</p> -->

datasetstation 快速下载中文数据集，处理数据集，数据分析、可视化分析，一站式解决数据问题

- 不用等了很久，结果 Timeout
- 不用每次写不规范的数据预处理代码
- 数据可视化分析不规范、每次都要重写非常麻烦
- 兼容 Tensorflow、Pytorch、HG Transformers 等主流的建模工具，一次数据处理，多平台数据建模
- 学习数据处理和分析的方法和流程，帮助你更懂数据

## 快速使用

```bash
pip install datasetstation

# 在 jupyter 中使用，执行下面命令
jupyter nbextension enable --py widgetsnbextension
jupyter labextension install jupyter-matplotlib
```

```python
from datasetstation import load_dataset, list_datasets

# 打印支持的数据集
print(list_datasets())

# 加载数据及并打印并第一个样本
hotel_review = load_dataset('hotel-review')
print(hotel_review['train'][0])

# 处理数据集 - 给每个样本增加一个文本长度的特征
hotel_review = hotel_review.map(lambda x: {"length": len(x["text"])})

# 结合 transformers 库，快速使用各种模型处理任务
from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained('bert-base-cased')

tokenized_dataset = hotel_review.map(lambda x: tokenizer(x['text']), batched=True)
```

<p align="center">
    <img src="http://aimaksen.bslience.cn/screanshot-datasets.gif" />
</p>


更多的关于 dataset 的操作，请参考 [Huggingface Datasets 文档](https://huggingface.co/docs/datasets/index)。

## 目前支持数据集

|       数据集      | 介绍                     |
|:-----------------:|--------------------------|
| hotel-review      | 【英文】酒店评价情感分析 |
| imdb              | 【英文】电影评论情感分析 |
| new-title-chinese | 【中文】新闻标题         |
| chinese-hotel-review | 【中文】携程酒店评价情感分析  |
| dbms | 【中文】豆瓣电影评论、打分数据  |
| ez-douban | 【中文】豆瓣电影信息、打分、评论  |
| waimai-review-10k | 【中文】外卖评价数据 10k 条，正负两种情绪  |
| weibo-senti-100k | 【中文】微博情感分析 100k 条，正负两种情绪  |
| simplifyweibo-4-moods | 【中文】微博情感分析，喜悦、愤怒、厌恶、低落四种情绪 |
| eshopping-10-cats | 【中文】电商 10 种商品评价，正负情感 |
| squad | 【英文】Stanford Question Answering Dataset (SQuAD) |
| stopwords-cn      |   【中文】中文停用词表  |
| stopwords-hit     | 【中文】哈工大停用词表   |
| stopwords-baidu  | 【中文】百度停用词表 |
| stopwords-scu | 【中文】四川大学机器智能实验室停用词库  |
| tangshi | 唐诗全集  |
| songshi| 宋诗全集  |
| songci| 宋词全集  |
| lunyu| 论语  |
| shijing| 诗经  |
| nalanxingde | 纳兰性德诗集 |



**（陆续上传更多中文数据集）如果你有数据集，希望也能快速使用，请联系作者公众号 @春阳CYang。存储空间有限，先到先得！**

<p align="center">
    <img src="http://aimaksen.bslience.cn/qrcode_cyang.jpg" />
</p>


## 使用方法和版本迭代

[每个版本详细的变更日志和使用方法。](https://github.com/CYang828/datasetstation/tree/master/examples)

如果觉得有帮助，希望能给我个星星⭐️
## 协议
[Apache License](https://github.com/CYang828/datasetstation/blob/master/LICENSE)

Copyright on (c) 2022-present CYang
