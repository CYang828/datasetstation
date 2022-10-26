import pathlib


S3_BUCKET_URI = "s3://fast-datasets/{ds}"

# Read Only Access
AWS_ACCESS_KEY_ID = "AKIAVXFFSLWHED2I7WGB"
AWS_SECRET_ACCESS_KEY = "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"

# Download Temp Path
TMP_PATH = "/tmp/{ds}"

# 默认数据集存储地址
DEFAULT_DATASET_PATH = pathlib.Path('/Users/zhangchunyang/.cache/datasetstation/datasets/')

# Divide String
D_S = "=" * 50
