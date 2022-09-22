from pathlib import Path

from pandas_profiling import ProfileReport


def quick_analysis(dataset, title="数据集快速分析报告", minimal=False):
    # config_file=Path(__file__).parent / "profiling.yml",
    df = dataset.to_pandas()
    df.dropna(axis=0, how="any", inplace=True)
    profile = ProfileReport(
        df,
        title=title,
        explorative=True,
        dark_mode=True,
        minimal=minimal,
    )
    return profile
