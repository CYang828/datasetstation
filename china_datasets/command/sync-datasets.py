import argparse

from china_datasets.repo_list import DATASETS
from china_datasets.util.s3 import s3_upload_files
from china_datasets.config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

from datasets import load_dataset
from datasets.filesystems import S3FileSystem


# Download Temp Path
TMP_PATH = "/tmp/{ds}"


def main(parser):
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
    if already_num:
        print('待同步的数据集有 {} 个\n--------------------'.format(already_num))
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
            print('--------------------')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='同步数据集')
    main(parser)
