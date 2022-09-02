from fast_datasets.repo import DatasetRepo

from yaspin import yaspin
from yaspin.spinners import Spinners


def load_dataset(dataset, backend='s3'):
    """
    Loads the dataset.
    """
    repo = DatasetRepo()

    try:
        return repo.get(dataset)
        spinner.ok("✅ ")
    except:
        spinner.fail("🙀 ")
        return