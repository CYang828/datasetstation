# china-dataset

<!-- <p align="center">
    <img src="http://aimaksen.bslience.cn/china-datasets-logo.jpg">
</p> -->

<!-- <p align="center">
    <a href="https://github.com/CYang828/china-datasets">
        <img src="https://travis-ci.org/CYang828/china-datasets.svg?branch=master" alt="fastweb">
    </a>
</p> -->

有没有找不到中文数据集，有没有找到中文数据集下载缓慢，下载了数据集每次都要根据不同的框架写不同的预处理逻辑的痛苦。
这个包帮你搞定这些！

- 不用等了很久，结果 Timeout
- 不用每次写不同的数据预处理代码

## 快速使用

```bash
pip install china-datasets
```

```python
from china_datasets import load_dataset, list_datasets

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
| eshopping-10-cats | 【中文】电商 10 中商品，正负情感 |
| squad | 【英文】Stanford Question Answering Dataset (SQuAD) |


**如果你有数据集，希望也能快速使用，请联系作者 zhagnchunyang_pri@126.com。存储空间有限，先到先得！**


## ROADMAP

每个版本详细的变更日志 [release notes](https://github.com/CYang828/china-datasets/blob/master/ROADMAP.md).

## 协议
[Apache License](https://github.com/CYang828/china-datasets/blob/master/LICENSE)

Copyright on (c) 2022-present CYang
