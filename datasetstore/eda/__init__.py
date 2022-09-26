from pathlib import Path

from datasets.arrow_dataset import Dataset
from pandas_profiling import ProfileReport


def quick_analysis(dataset, title="数据集快速分析报告", minimal=False, explorative=True, dark_mode=True, orange_mode=False):
    # config_file=Path(__file__).parent / "profiling.yml",
    df = dataset.to_pandas()
    # issue: pandas_profiling 在处理空字符串时会报错，无法继续生成报告
    df.dropna(axis=0, how="any", inplace=True)
    profile = ProfileReport(
        df,
        title=title,
        explorative=explorative,
        dark_mode=dark_mode,
        minimal=minimal,
        orange_mode=orange_mode
    )
    profile.to_notebook_iframe()
    dataset = Dataset.from_pandas(df)
    return dataset
