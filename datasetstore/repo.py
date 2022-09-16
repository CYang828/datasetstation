import os
import pathlib

from datasetstore.backend import S3StorageBackend
from datasetstore.config import DEFAULT_DATASET_PATH

from datasets import load_from_disk


class DatasetRepo(object):

    _backend_storage = S3StorageBackend()

    def __init__(self, backend="s3"):
        self._backend = backend

    def set_backend(self, backend="s3"):
        """设置存储后端"""

        if backend == "s3":
            self._backend = backend
            self._backend_storage = S3StorageBackend()

    def list(self):
        """列出数据集仓库中的数据集名称"""
        return list(self._backend_storage.walk("fast-datasets", maxdepth=1))[0][1]

    def get_dataset_info(self, dataset):
        """获取数据集信息"""
        pass

    def _load_dataset(self, name):
        """加载数据集

        :parameter:
        name: 数据集名称

        如果本地缓存中存在，则从缓存中加载，返回 dataset
        如果本地缓存中不存在，则从网络中加载，返回 dataset
        """
        dataset_path = DEFAULT_DATASET_PATH / name
        if dataset_path.exists():
            dataset = load_from_disk(dataset_path)
            return dataset
        else:
            dataset = load_from_disk(
                self._backend_storage.backend_uri.format(ds=name),
                fs=self._backend_storage,
            )
            dataset.save_to_disk(os.fspath(DEFAULT_DATASET_PATH / name))
            return dataset

    def get(self, dataset):
        """获取数据集对象"""
        # 查看目录下的结构
        folders = list(
            self._backend_storage.walk("fast-datasets/{}".format(dataset), maxdepth=1)
        )[0][1]

        # 多数据集合加载
        if folders and "train" not in folders:
            datasets = {}
            for folder in folders:
                dataset_path = "{}/{}".format(dataset, folder)
                datasets[folder] = self._load_dataset(dataset_path)

            return datasets
        else:
            # 数据集加载
            dataset = self._load_dataset(dataset)
            return dataset

    def is_exist(self, name):
        if name in self.list():
            return True
        else:
            return False
