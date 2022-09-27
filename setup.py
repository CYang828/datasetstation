# coding=utf-8


import sys
from setuptools import setup, find_packages


kwargs = {}
install_requires = []
version = '1.0.1.5'
if sys.version_info < (3, 0):
    with open('README.md') as f:
        kwargs['long_description'] = f.read()

    with open('requirements.txt') as f:
        for require in f:
            install_requires.append(require[:-1])
    # install_requires.append('subprocess32')
elif sys.version_info > (3, 0):
    with open('README.md', encoding='utf-8') as f:
        kwargs['long_description'] = f.read()

    with open('requirements.txt', encoding='utf-8') as f:
        for require in f:
            install_requires.append(require[:-1])

# if sys.platform.startswith('linux'):
#     install_requires.append('readline')
# elif sys.platform.startswith('win'):
#     install_requires.append('pyreadline')

kwargs['install_requires'] = install_requires

setup(
    name='datasetstore',
    version=version,
    include_package_data=True,
    packages=find_packages(),
    package_data={},
    entry_points={
        'console_scripts': [
            'china-datasets = datasetstore.command.main:main',
        ],
    },
    author='CYang',
    author_email='zhangchunyang_pri@126.com',
    description="datasetstore 快速下载中文数据集，处理数据集，数据分析、可视化分析，一站式解决数据问题",
    url="https://github.com/CYang828/datasetstore",
    long_description_content_type="text/markdown",
    **kwargs
)
