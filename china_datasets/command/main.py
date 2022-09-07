import argparse

from china_datasets.command.sync_datasets import sync


def main():
    parser = argparse.ArgumentParser(description='china-datasets 命令行工具')
    subparsers = parser.add_subparsers(dest="subparser_name")
    sync_parser = subparsers.add_parser('sync')
    sync_parser.add_argument('-f', type=str, help='待同步的数据集配置文件')
    sync_parser.add_argument('-d', type=list, help='待同步的数据集名称')
    args = parser.parse_args()

    if args.subparser_name == 'sync':
        sync(args)


if __name__ == '__main__':
    main()

    