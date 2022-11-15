import cufflinks as cf
import plotly.graph_objects as go
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
import string
import jieba
import jieba.posseg as pos

cf.go_offline()
cf.set_config_file(offline=False, world_readable=True)


def length_distribution(dataset, text_column_name, quantile=0.8):
    """文本长度分布"""
    dataframe = dataset.to_pandas()
    dataframe["text_len"] = dataframe[text_column_name].map(
        lambda x: len(x) if x else 0
    )
    len_count_df = dataframe.groupby("text_len", as_index=False).count()
    max_example_count = len_count_df[text_column_name].max()
    max_len = len_count_df["text_len"].max()
    len_count_df = len_count_df.rename(
        {"text_len": "文本长度", text_column_name: "样本个数"}, axis="columns"
    )

    # 适合截断长度计算
    quantile_idx = int(len(dataframe) * quantile)
    sorted_len_df = dataframe.sort_values(by=["text_len"])
    v = sorted_len_df.reset_index(drop=True)
    suitable_length = v.loc[quantile_idx - 1]

    # 画柱状图
    fig = px.bar(len_count_df, x="文本长度", y="样本个数", text_auto=True)
    fig.add_shape(
        type="line",
        x0=suitable_length["text_len"],
        y0=-10,
        x1=suitable_length["text_len"],
        y1=max_example_count + 10,
        line=dict(color="#7D9D9C", width=1),
    )

    # 画提示性文字
    fig.add_trace(
        go.Scatter(
            x=[max_len / 2],
            y=[(max_example_count + 10) / 2],
            text=[
                "文本最大长度 {}\n\r占比全数据集 {}".format(suitable_length["text_len"], quantile),
            ],
            mode="text",
            fillcolor="#7D9D9C",
        )
    )

    # 更新 layout
    layout = go.Layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    fig.update_layout(layout)
    fig.show()


# 用来正常显示中文
plt.rcParams["font.sans-serif"] = ["SimHei"]
# 用来正常显示负号
plt.rcParams["axes.unicode_minus"] = False


def wordcloud(texts):
    """绘制词云"""
    assert type(texts) == list

    # 去空
    texts = pd.Series(texts).dropna().tolist()

    wordcloud = WordCloud(
        background_color="white",
        font_path="/System/Library/Fonts/PingFang.ttc",
        width=1400,
        height=800
    ).generate(" ".join(texts))
    plt.axis("off")
    plt.imshow(wordcloud)
    plt.show()


# 字频率分布
def word_distribution(dataset):
    '''统计字频率分布'''
    assert type(dataset) == list

    # 去空、拼接
    texts = pd.Series(dataset).dropna().tolist()
    texts = ''.join(texts)

    # 中文标点转英文
    table = {ord(f): ord(t) for f, t in zip(
        u'，。！？【】（）％＃＠＆１２３４５６７８９０',
        u',.!?[]()%#@&1234567890')}
    texts = texts.translate(table)

    # 去掉无用标点符号
    exclude = set(string.punctuation)
    texts = ''.join(ch for ch in texts if ch not in exclude)
    # print(texts)

    word_dict = {}
    for i in texts:
        if i not in word_dict:
            word_dict[i] = 1
        else:
            word_dict[i] += 1

    data = pd.Series(word_dict).sort_values()
    data_mean = int(data.mean())
    data_std = int(data.std())
    middle_index = int(data.shape[0] / 2)
    low_middle_index = int(data.shape[0] / 4)
    high_middle_index = middle_index + low_middle_index

    return_dict = {}
    return_dict['频率最小的字符'] = ' '.join(data.index[data == data[0]].tolist())
    return_dict[str(data.index[0]) + '频率值'] = data[0]
    return_dict['频率最大的字符'] = ' '.join(data.index[data == data[-1]].tolist())
    return_dict[str(data.index[-1]) + '频率值'] = data[-1]
    return_dict['中间频率的字符'] = data.index[middle_index]
    return_dict['中间频率'] = data[middle_index]
    return_dict['四分之三位的字符'] = data.index[high_middle_index]
    return_dict['四分之三位的频率'] = data[high_middle_index]
    return_dict['四分之一位的字符'] = data.index[low_middle_index]
    return_dict['四分之一位的频率'] = data[low_middle_index]

    # 打印字典信息
    return_data = pd.Series(return_dict)
    print(return_data)

    # 绘制分布图像
    data.plot(kind='bar')
    plt.show()


# 词频率分布
def words_distribution(dataset):
    '''统计字频率分布'''
    assert type(dataset) == list

    # 去空、拼接
    texts = pd.Series(dataset).dropna().tolist()
    texts = ''.join(texts)

    # 中文标点转英文
    table = {ord(f): ord(t) for f, t in zip(
        u'，。！？【】（）％＃＠＆１２３４５６７８９０',
        u',.!?[]()%#@&1234567890')}
    texts = texts.translate(table)

    # 去掉无用标点符号
    exclude = set(string.punctuation)
    texts = ''.join(ch for ch in texts if ch not in exclude)
    # print(texts)

    texts = jieba.lcut(texts, cut_all=False)

    word_dict = {}
    for i in texts:
        if i not in word_dict:
            word_dict[i] = 1
        else:
            word_dict[i] += 1

    data = pd.Series(word_dict).sort_values()
    data_mean = int(data.mean())
    data_std = int(data.std())
    middle_index = int(data.shape[0] / 2)
    low_middle_index = int(data.shape[0] / 4)
    high_middle_index = middle_index + low_middle_index

    return_dict = {}
    return_dict['频率最小的词'] = ' '.join(data.index[data == data[0]].tolist())
    return_dict[str(data.index[0]) + '频率值'] = data[0]
    return_dict['频率最大的词'] = ' '.join(data.index[data == data[-1]].tolist())
    return_dict[str(data.index[-1]) + '频率值'] = data[-1]
    return_dict['中间频率的词'] = data.index[middle_index]
    return_dict['中间频率'] = data[middle_index]
    return_dict['四分之三位的词'] = data.index[high_middle_index]
    return_dict['四分之三位的频率'] = data[high_middle_index]
    return_dict['四分之一位的词'] = data.index[low_middle_index]
    return_dict['四分之一位的频率'] = data[low_middle_index]

    # 打印字典信息
    return_series = pd.Series(return_dict)
    print(return_series)

    # 绘制分布图像
    data.plot(kind='bar')
    plt.show()


# 词性频率分布
def pos_distribution(dataset):
    '''统计字频率分布'''
    assert type(dataset) == list

    # 去空、拼接
    texts = pd.Series(dataset).dropna().tolist()
    texts = ''.join(texts)

    # 中文标点转英文
    table = {ord(f): ord(t) for f, t in zip(
        u'，。！？【】（）％＃＠＆１２３４５６７８９０',
        u',.!?[]()%#@&1234567890')}
    texts = texts.translate(table)

    # 去掉无用标点符号
    exclude = set(string.punctuation)
    texts = ''.join(ch for ch in texts if ch not in exclude)
    # print(texts)

    out = pos.lcut(texts)
    sign_dict = {}

    for char, sign in out:
        if sign not in sign_dict:
            sign_dict[sign] = 1
        else:
            sign_dict[sign] += 1

    sign_series = pd.Series(sign_dict)
    # print(sign_series)

    sign_series.plot(kind='bar')
    plt.show()


if __name__ == '__main__':
    from datasets import load_from_disk

    dataset = load_from_disk('/Users/dachengzi/DeepLearn/huggingface/data/ChnSentiCorp')
    # print(dataset['train']['text'])

    # wordcloud(dataset['train']['text'])
    # words_distribution(dataset['train']['text'])
    # pos_distribution(dataset['train']['text'])
