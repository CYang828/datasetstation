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

It is a charming web-server framework based on the effective technique and organized into component. These components could be used with only several config and code. It is always so easy to make a new component.It also provides many scenes to construct your apis, pages, rpc functions, tasks and so on efficiently.

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
    <img src="http://aimaksen.bslience.cn/china-datasets-logo.jpg" />
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
