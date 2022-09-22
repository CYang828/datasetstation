from pathlib import Path

from pandas_profiling import ProfileReport


def quick_analysis(dataset, title="数据集快速分析报告"):
    profile = ProfileReport(
        dataset.to_pandas(), config_file=Path(__file__).parent / "profiling.yml", title=title, explorative=True, dark_mode=True
    )
    return profile
