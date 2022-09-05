# coding:utf8


"""call fastweb component

Usage:
    fast <configpath>

Options:
    -h --help     Show this screen.
    --args=<arg>  Remote task arguments.
"""


import os

from fastweb import app
from fastweb.accesspoint import docopt
from fastweb.util.tool import HistoryConsole
from fastweb.components import SyncComponents
from fastweb.util.log import console_recorder, colored


def main():
    cwd = os.getcwd()
    import sys
    sys.path.append(cwd)
    del sys
    args = docopt(__doc__)
    configpath = args['<configpath>']
    configpath = os.path.join(cwd, configpath)
    app.load_component(layout='service', backend='ini', path=configpath)
    components = SyncComponents()
    console_recorder('DEBUG', "[Fast command]\nyou can do anything like in fastweb")
    console = HistoryConsole(locals={'self': components})
    console.interact()



