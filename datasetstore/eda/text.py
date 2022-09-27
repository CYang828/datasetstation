import cufflinks as cf
import plotly.graph_objects as go
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt


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


#用来正常显示中文
plt.rcParams["font.sans-serif"]=["SimHei"]
#用来正常显示负号
plt.rcParams["axes.unicode_minus"]=False

def wordcloud(texts):
    """绘制词云"""
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

# 词频率分布

# 词性频率分布
