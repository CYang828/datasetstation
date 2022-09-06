from china_datasets.repo import DatasetRepo
from china_datasets.config import TMP_PATH, D_S
from china_datasets.util.s3 import s3_upload_files
from china_datasets.util.log import getLogger

from datasets import Dataset, load_dataset as hg_load_datasets
from yaspin import yaspin
from yaspin.spinners import Spinners


logger = getLogger()


def load_dataset(path, backend='s3', **kwargs):
    """
    Loads the dataset.
    """

    # 读取本地文件
    if path in ('csv', 'json', 'text', 'csv', 'parquet') and kwargs.get('data_files'):
        dataset = hg_load_datasets(path, **kwargs)
        return dataset
    else:
        repo = DatasetRepo()

        if not repo.is_exist(path):
            logger.warning('当前仓库不存在此数据集，请联系管理员上传 <zhangchunyang_pri@126.com>')
            return None

        with yaspin(Spinners.moon, text="下载中...") as spinner:
            try:
                dataset = repo.get(path)
                spinner.text = "下载完成"
                spinner.ok("✅✅✅✅✅✅✅✅✅✅")
                return dataset
            except BaseException as e:
                logger.error(e)
                spinner.text = "下载失败，请联系管理员 <zhangchunyang_pri@126.com>"
                spinner.fail("🙀🙀🙀🙀🙀🙀🙀🙀🙀🙀")
                return None 


def upload_dataset(dataset, name, **dataset_info):
    # 验证数据集是否合法
    if not isinstance(dataset, Dataset):
        logger.error('当前 dataset 对象不合法，目前支持 Huggingface Dataset 对象')
        return None

    repo = DatasetRepo()
    if repo.is_exist(name):
        logger.warning('当前 dataset 名字已在仓库中存在，无需重复上传')
        return None

    # 将数据集保存到本地
    dataset_path = TMP_PATH.format(ds=name)
    dataset.save_to_disk(dataset_path)

    # 上传数据到远端
    s3_upload_files(name, dataset_path)
    return dataset
