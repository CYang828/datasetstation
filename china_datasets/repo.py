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
        pass

    def get_dataset_info(self, dataset):
        """获取数据集信息"""
        pass

    def get(self, dataset):
        """获取数据集对象"""

        return load_from_disk(
            self._backend_storage.backend_uri.format(ds=dataset),
            fs=self._backend_storage,
        )
