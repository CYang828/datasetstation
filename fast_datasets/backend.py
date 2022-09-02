from ABC import abstractclassmethod

from fast_datasets.config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, S3_BUCKET_URI


from datasets.filesystems import S3FileSystem


class StorageBackend(object):

    backend_storage = None
    backend_uri = None
    
    @abstractclassmethod
    def download():
        pass


class S3StorageBackend(StorageBackend, S3FileSystem):

    backend_uri = S3_BUCKET_URI

    def __init__(self, bucket_name):
        self.backend_storage = S3FileSystem(
            key=AWS_ACCESS_KEY_ID,
            secret=AWS_SECRET_ACCESS_KEY,
            client_kwargs={"region_name": "cn-north-1"})
        return self.backend_storage




