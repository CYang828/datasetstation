# coding:utf8


import os
import uuid
import code
import atexit
import readline
from threading import Timer

from fastweb.accesspoint import ioloop, coroutine, Return

from celery import (Celery, platforms)


def get_celery_from_object(name, obj=None):
    """获取celery对象"""

    platforms.C_FORCE_ROOT = True
    celery = Celery(name)
    obj and celery.config_from_object(obj)
    return celery


def time_delay(times, delay=10, divisor=10):
    """根据次数时间延时"""

    for i in range(times):
        yield divisor * i + delay


def uniqueid(bit=64):
    """获取64位requesid"""

    return uuid.uuid1().int >> bit


class timing(object):
    """计时器"""

    __unitfactor = {'s': 1,
                    'ms': 1000,
                    'us': 1000000}

    def __init__(self, unit='s', precision=4):
        self.start = None
        self.end = None
        self.total = 0
        self.unit = unit
        self.precision = precision

    def __enter__(self):
        if self.unit not in timing.__unitfactor:
            raise KeyError('Unsupported time unit.')
        self.start = ioloop.IOLoop.current().time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = ioloop.IOLoop.current().time()
        self.total = (self.end - self.start) * timing.__unitfactor[self.unit]
        self.total = round(self.total, self.precision)
        return False

    def __str__(self):
        return '{total}{unit}'.format(total=self.total, unit=self.unit)


class RetryPolicy(Exception):
    """重试策略"""

    def __init__(self, times, error, interval=0, delay=0):
        self.times = times
        self.error = error
        self.interval = interval
        self.delay = delay
        self.retry = 0


class Retry(object):
    """重试机制"""

    def __init__(self, obj, name, func, *args, **kwargs):
        self._obj = obj
        self._name = name
        self._func = func
        self._args = args
        self._kwargs = kwargs

    def run_sync(self):
        """运行重试机制"""

        try:
            return self._func(*self._args, **self._kwargs)
        except RetryPolicy as e:
            if e.retry < e.times:
                delay = e.interval * e.retry + e.delay
                e.retry += 1
                self._obj.recorder('WARN', '{name} <{retry}> retry in {delay} second...'.format(name=self._name, retry=e.retry, delay=delay))
                if delay:
                    Timer(delay, self.run).start()
                else:
                    return self.run_sync()
            else:
                self._obj.recorder('ERROR', '{name} retry error raise {exc}'.format(name=self._name, exc=e.error))
                raise e.error

    @coroutine
    def run_asyn(self):
        try:
            ret = yield self._func(*self._args, **self._kwargs)
            raise Return(ret)
        except RetryPolicy as e:
            if e.retry < e.times:
                delay = e.interval * e.retry + e.delay
                e.retry += 1
                self._obj.recorder('WARN', '{name} <{retry}> retry in {delay} second...'.format(name=self._name, retry=e.retry, delay=delay))
                if delay:
                    Timer(delay, self.run).start()
                else:
                    ret = yield self.run_asyn()
                    raise Return(ret)
            else:
                self._obj.recorder('ERROR', '{name} retry error raise {exc}'.format(name=self._name, exc=e.error))
                raise e.error


class HistoryConsole(code.InteractiveConsole):
    def __init__(self, locals=None, filename="<console>", histfile=os.path.expanduser("~/.console-history")):
        code.InteractiveConsole.__init__(self, locals, filename)
        self.init_history(histfile)

    def init_history(self, histfile):
        readline.parse_and_bind("tab: complete")
        if hasattr(readline, "read_history_file"):
            try:
                readline.read_history_file(histfile)
            except IOError:
                pass
            atexit.register(self.save_history, histfile)

    def save_history(self, histfile):
        readline.set_history_length(1000)
        readline.write_history_file(histfile)