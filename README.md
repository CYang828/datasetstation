# china-dataset

<p align="center">
    <img src="http://aimaksen.bslience.cn/china-datasets-logo.jpg">
</p>

<p align="center">
    <a href="https://github.com/CYang828/china-datasets">
        <img src="https://travis-ci.org/CYang828/china-datasets.svg?branch=master" alt="fastweb">
    </a>
</p>

## 介绍

在国内也能快速加载数据集，并且能够使用 huggingface datasets 进行统一、快速的处理数据集。

- 不用等了很久，结果 Timeout
- 不用每次写不同的数据预处理代码

## 快速使用

```bash
pip install china-datasets
```

```python
from china_datasets import load_dataset

dataset = load_dataset('hotel-review')
print(dataset)
```

<p align="center">
    <img src="http://aimaksen.bslience.cn/screanshot-datasets.gif" />
</p>

## 目前支持数据集

|       数据集      | 介绍                     |
|:-----------------:|--------------------------|
| hotel-review      | 【英文】酒店评价情感分析 |
| imdb              | 【英文】电影评论情感分析 |
| new-title-chinese | 【中文】新闻标题         |


## 更新日志

每个版本详细的变更日志 [release notes](https://github.com/BSlience/fastweb/CHANGELOG.md).

## 协议
[Apache License](https://github.com/CYang828/china-datasets/LICENSE.md)

Copyright on (c) 2022-present CYang
