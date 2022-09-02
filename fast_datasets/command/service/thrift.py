# coding:utf8

"""autogen thrift hubcode, handler, config

Usage:
    fasthrift <idls>
              [-p --pattern=<p>]
              [-o --outhub=<oh>]
              [-c --outconfig=<oc>]
              [-d --outhandler]

Options:
    -h --help     Show this screen.
    -p --pattern=<p>  Pattern(sync|async). [default: async]
    -o --outhub=<oh>   Output thrift hub module path. [default: ]
    -c --outconfig=<oc>    Output load thrift of fastweb path. [default: ]
    -d --handler=<hd>    Output handler template code. [default: handlers]
"""

import os
from glob import iglob

from fastweb.script import Script
from fastweb.spec.idl import Parser
from fastweb.util.log import recorder
from fastweb.accesspoint import docopt
from fastweb.util.python import write_file
from fastweb.exception import ThriftParserError, FastwebException


TAB = ' '*4


class ThriftCommand(Script):
    """一个thrift文件中只允许定义一个service，定义多个service会强制报错，不要在一个service中定义过多的function。
    遵循微服务的原则，将能够独立的部分拆分成独立的service"""

    def __init__(self):
        self._idl_parser = Parser()

    def gen_thrift_auxiliary(self):
        """生成与thrift相关的桩代码（hub code）和配置文件"""

        # 获取基础参数
        cwd = os.getcwd()
        args = docopt(__doc__)
        language = ''
        hub_suffix = ''
        idls = args['<idls>']
        hub_path = args['--outhub']
        config_path = args['--outconfig']
        handler_package = args['--handler']

        if args['--pattern'] == 'async':
            language = 'py:tornado'
            hub_suffix = 'async'
        elif args['--pattern'] == 'sync':
            language = 'py'
            hub_suffix = 'sync'
        else:
            recorder('ERROR', 'pattern not support')

        # 创建thrift桩代码
        hub_module_name, service_module_pathes, program = self._create_hub_package(idls, language, hub_path, hub_suffix)

        # 创建handler包目录
        try:
            handler_path = os.path.join(cwd, handler_package)
            os.mkdir(handler_path)
            recorder('INFO', 'create dir {path}'.format(path=handler_path))

            # 创建包__init__文件
            with open(os.path.join(handler_path, '__init__.py'), 'w') as f:
                f.write('"""generate from fasthrift"""')
        except OSError:
            pass

        # 创建handler模板
        for service in program:
            handler_module_name, handler_cls_name = self._create_handler(service, handler_path)
            handler_python_path = '{package}.{module}.{cls}'.format(package=handler_package,
                                                                    module=handler_module_name,
                                                                    cls=handler_cls_name)
        # 生成配置文件
        thrift_config_template = self._create_config_file(service_module_pathes, handler_python_path, program)

        # 创建配置文件
        if config_path:
            config_path = os.path.join(cwd, config_path)
            write_file(config_path, thrift_config_template)
            recorder('INFO', 'create config file {config}'.format(config=config_path))

        recorder('DEBUG',
                 'thrift hub module path: {hub}\n'
                 'thrift handler path: {handler}\n'
                 'thrift config path: {config}'.format(hub=os.path.join(cwd, hub_module_name),
                                                       config=config_path,
                                                       handler=handler_path))

    def _create_hub_package(self, idls, language, hub_path, hub_suffix):
        """创建thrift桩代码

        :return:
          - `service_module_pathes`: 每个thrift生成的桩代码python类路径
          - `service_handler_pathes`: 自动生成的handler的python类路径
        """

        cwd = os.getcwd()
        # package 名字中不能存在`-`，无法导入
        hub_module_name = 'fastweb_thrift_{hub_package}'.format(hub_package=hub_suffix)
        hub_path = os.path.join(hub_path, hub_module_name)
        hub_abspath = os.path.join(cwd, hub_path)

        # 创建桩代码的目录
        try:
            os.mkdir(hub_abspath)
            recorder('INFO', 'create dir {path}'.format(path=hub_abspath))
        except OSError:
            pass

        services = []
        service_module_pathes = []

        for idl in iglob(idls):
            # 检验+解析
            program = self._parse_idl(idl)
            if len(program) > 1:
                recorder('ERROR', 'each thrift file can only hold one service, you define {num} service in {idl}'.format(num=len(program), idl=idl))
                raise FastwebException

            service_package_name = idl.split('/')[-1].rstrip('.thrift')

            # 通过thrift命令生成桩代码
            command = 'thrift --gen {language} -out {out} {idl} '.format(language=language, idl=idl, out=hub_path)
            self.call_subprocess(command)
            for service in program:
                service_module_path = '{hub}.{package}.{module}'.format(hub=hub_module_name,
                                                                        package=service_package_name,
                                                                        module=service.name)
                service_module_pathes.append(service_module_path)
                services.append(service)

        return hub_module_name, service_module_pathes, services

    @staticmethod
    def _create_config_file(service_module_pathes, handler_python_path, program):
        """创建fastweb配置文件"""

        thrift_config_template = ''
        module_len = len(service_module_pathes)
        for i, service_module_pathes in enumerate(service_module_pathes):
            if i == 0:
                thrift_config_template += '; fastthrift gen template\n\n'

            thrift_config_template += '[service:{service}]\n' \
                                      'port =\n' \
                                      'thrift_module = {hub}\n' \
                                      'handlers = {handler}\n' \
                                      'active = yes'.format(hub=service_module_pathes,
                                                            handler=handler_python_path,
                                                            service=program[i].name)

            if i != module_len:
                thrift_config_template += '\n\n\n'

        recorder('INFO', 'fasthrift gen config')
        recorder('CRITICAL', '{config}'.format(config=thrift_config_template))
        return thrift_config_template

    @staticmethod
    def _create_handler(service, handler_path):
        """创建handler

        :parameter:
          - `service`: 服务对象
        """

        service_handler_cls = service.name + 'Handler'
        cls_template = '# coding:utf8\n\n"""generate by fasthrift"""\n\n\n' \
                       'from fastweb.service import ABLogic\n\n\n' \
                       'class {cls}(ABLogic):\n\n'.format(tab=TAB,
                                                          cls=service_handler_cls)
        func_template = '{tab}def {func}(self):\n{tab}{tab}pass\n\n'
        funcs_template = ''

        for func in service.functions:
            funcs_template += func_template.format(tab=TAB, func=func.name)

        handler_template = cls_template + funcs_template
        handler_path = os.path.join(handler_path, service.name+'.py')
        write_file(handler_path, handler_template)
        return service.name, service_handler_cls

    def _parse_idl(self, idl):
        """解析idl文件

        :parameter:
          - `idl`: idl文件"""
        try:
            program = self._idl_parser.parse_file(idl).definitions
            return program
        except ThriftParserError:
            recorder('ERROR', 'thrift file {idl} format error'.format(idl=idl))
            raise


def gen_thrift_auxiliary():
    ThriftCommand().gen_thrift_auxiliary()


