import os

from china_datasets.repo_list import DATASETS

import boto3
from yaspin import yaspin
from yaspin.spinners import Spinners
from datasets import load_dataset
from datasets.filesystems import S3FileSystem


# All Access Permission
AWS_ACCESS_KEY_ID = "AKIAVXFFSLWHAAZD3PM6"
AWS_SECRET_ACCESS_KEY = "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"
# Download Temp Path
TMP_PATH = "/tmp/{ds}"


def s3_upload_files(ds, path):
    print('正在上传数据集 {}'.format(path))
    session = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name='cn-north-1'
    )
    s3 = session.resource('s3')
    bucket = s3.Bucket('fast-datasets')
 
    with yaspin(Spinners.moon, text="上传中...") as spinner:
        for subdir, _, files in os.walk(path):
            for file in files:
                full_path = os.path.join(subdir, file)
                spinner.text = full_path
                with open(full_path, 'rb') as data:
                    bucket.put_object(Key='{}/{}'.format(ds, full_path[len(path)+1:]), Body=data)

    spinner.text = '上传完成'        
    print('上传数据集完成 {}'.format(path))


def main():
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
    main()
