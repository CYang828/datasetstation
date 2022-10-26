from typing import Optional, List, Union, Dict, Tuple, Iterator
from enum import Enum

from pydantic import BaseModel


class ExplicitEnum(str, Enum):
    """
    Enum with more explicit error message for missing values.
    """

    @classmethod
    def _missing_(cls, value):
        raise ValueError(
            f"{value} is not a valid {cls.__name__}, please select one of {list(cls._value2member_map_.keys())}"
        )


class FileListType(BaseModel):
    """文件列表类型"""
    files: List[str]



