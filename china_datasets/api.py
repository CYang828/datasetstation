from china_datasets.repo import DatasetRepo

from yaspin import yaspin
from yaspin.spinners import Spinners


def load_dataset(dataset, backend='s3'):
    """
    Loads the dataset.
    """
    repo = DatasetRepo()

    with yaspin(Spinners.moon, text="下载中...") as spinner:
        try:
            dataset = repo.get(dataset)
            spinner.text = "下载完成"
            spinner.ok("✅✅✅✅✅✅✅✅✅✅")
            return dataset
        except BaseException:
            spinner.text = "下载失败，请联系管理员<zhangchunyang_pri@126.com>"
            spinner.fail("🙀🙀🙀🙀🙀🙀🙀🙀🙀🙀")
            return
