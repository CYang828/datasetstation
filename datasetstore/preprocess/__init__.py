from tqdm import tqdm
from datasets.arrow_dataset import Dataset

from collections.abc import Iterable, Callable



def preprocessing(dataset: Dataset, field: str, func_chain: Iterable = []) -> Dataset:
    pbar = tqdm(func_chain)
    for func in pbar:
        pbar.set_description('正在执行预处理 {}'.format(func.__name__))
        dataset = dataset.map(lambda x: func(x[field]))
    pbar.set_description('预处理完成')
    return dataset