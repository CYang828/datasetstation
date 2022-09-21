import json

from datasetstore.util.log import getLogger
from datasetstore.util.s3 import s3_upload_files
from datasetstore.config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, TMP_PATH, D_S

from datasets.load import load_dataset
from datasets.filesystems.s3filesystem import S3FileSystem


logger = getLogger()


def sync(args):
    DATASETS = {}
    if args.f:
        with open(args.f) as f:
            DATASETS = json.load(f)

    # 对比数据集
    dataset_names_downloading = list(DATASETS.keys())
    dataset_names_downloading = set(map(
        lambda x: "fast-datasets/{ds}".format(ds=x), dataset_names_downloading
    ))

    s3 = S3FileSystem(
        key=AWS_ACCESS_KEY_ID,
        secret=AWS_SECRET_ACCESS_KEY,
        client_kwargs={"region_name": "cn-north-1"},
    )

    dataset_names_already = set(s3.ls("fast-datasets"))
    dataset_names_already = dataset_names_downloading - dataset_names_already

    already_num = len(dataset_names_already)
    logger.info('待同步的数据集有 {} 个\n{}'.format(already_num, D_S))

    if already_num:
        for dataset in dataset_names_already:  
            # 下载和准备数据集
            dataset_name = dataset[dataset.rfind('/')+1:]
            hg_dataset = DATASETS[dataset_name]
            dataset_path = TMP_PATH.format(ds=dataset_name)
            print('正在下载数据集 {} 到 {}'.format(hg_dataset, dataset_path))
            dataset = load_dataset(hg_dataset)
            dataset.save_to_disk(dataset_path)
            print('下载数据集 {} 到 {} 完成'.format(hg_dataset, dataset_path))
    
            # 上传数据集
            s3_upload_files(dataset_name, dataset_path)
            print('{}'.format(D_S))

