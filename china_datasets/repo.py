from china_datasets.backend import S3StorageBackend


from datasets import load_from_disk


class DatasetRepo(object):

    _backend_storage = None

    def __init__(self, backend="s3"):
        self._backend = backend
        self.set_backend(backend)

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

    def get(self, dataset):
        """获取数据集对象"""
        # 查看目录下的结构
        folders = list(
            self._backend_storage.walk("fast-datasets/{}".format(dataset), maxdepth=1)
        )[0][1]

        if "train" in folders:
            return load_from_disk(
                self._backend_storage.backend_uri.format(ds=dataset),
                fs=self._backend_storage,
            )
        else:
            datasets = {}
            for folder in folders:
                dataset_path = '{}/{}'.format(dataset, folder)
                datasets[folder] = load_from_disk(
                    self._backend_storage.backend_uri.format(ds=dataset_path),
                    fs=self._backend_storage,
                )
            return datasets

    def is_exist(self, name):
        if name in self.list():
            return True
        else:
            return False
