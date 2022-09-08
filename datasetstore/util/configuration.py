# coding:utf8


import re
import collections
import configparser

from fastweb.util.log import recorder
from fastweb.util.python import to_iter, str2everything
from fastweb.exception import ParameterError


class ConfigurationParser(object):
    """Configuration Parser"""

    parser = {'ini': '_ini_parser'}

    def __init__(self, t, **setting):
        """parse config file

        :parameter:
          - `t`: type
          - `setting`: setting

        parse result:
            `configs`: {'section': {setting}}
        """

        self.configs = None
        self.get_configs(t, setting)

    @staticmethod
    def _check_setting(eattr, setting):
        """check backend setting

        :parameter:
          - `eattr`: essential attribute
          - `setting`: setting
        """

        for attr in eattr:
            v = setting.get(attr)
            if not v:
                recorder('CRITICAL', 'configuration backend setting error! '
                                     'right options {options}'.format(options=eattr))
                raise ParameterError

    def _ini_parser(self, setting):
        """ini file parser

        :parameter:
          - `setting`: setting
        """

        eattr = ['path']
        self._check_setting(eattr, setting)
        path = setting.get('path')
        cf = configparser.ConfigParser()
        cf.read(path)
        configs = collections.defaultdict(dict)

        for section in cf.sections():
            options = cf.items(section)
            for key, value in options:
                value = str2everything(value)
                configs[section][key] = value
        return configs

    def get_configs(self, t, setting):
        """get configs from the type

        :parameter:
          - `backend`: type
          - `setting`: setting
        """

        parser = self.parser.get(t)
        if parser:
            self.configs = getattr(self, parser)(setting)
        else:
            raise ParameterError

    def get_components(self, components):
        """get components protocol

        :parameter:
          - `components`: component name, may be a list

        :return:
          { section:
            { 'component': component_name,
             'object': component_type }
          }
        """

        match_components = {}
        components = to_iter(components)

        for component in components:
            component_exp = r'(%s):(\w*)' % component
            exp = re.compile(component_exp)

            for section in list(self.configs.keys()):
                match = exp.match(section)
                if match:
                    match_components[section] = {'component': match.group(1), 'object': match.group(2)}

        return match_components
