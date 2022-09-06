import os

from china_datasets.util.log import getLogger

import boto3
from yaspin import yaspin
from yaspin.spinners import Spinners


logger = getLogger()


# All Access Permission
AWS_ACCESS_KEY_ID = "AKIAVXFFSLWHAAZD3PM6"
AWS_SECRET_ACCESS_KEY = "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"


def s3_upload_files(ds, path):
    logger.info('正在上传数据集 {}'.format(path))
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
                    bucket.put_object(Key='{}/{}'.format(ds, full_path[len(path) + 1:]), Body=data)

    spinner.text = '上传完成'
    spinner.ok("✅✅✅✅✅✅✅✅✅✅")
    logger.info('上传数据集完成 {}'.format(path))

