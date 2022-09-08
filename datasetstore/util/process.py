# coding:utf8

"""进程模块"""

from multiprocessing import Process

from fastweb.util.log import recorder


class FProcess(Process):

    _fprocesses = []

    def __init__(self, name, task, *args, **kwargs):
        super(FProcess, self).__init__(name=name)
        self._task = task
        self._fprocesses.append(self)
        self._args = args
        self._kwargs = kwargs

    def __str__(self):
        return '<FProcess|{name}|{pid}>'.format(name=self.name, pid=self.pid)

    def run(self):
        recorder('INFO', '{proc} start'.format(proc=self))
        self._task(*self._args, **self._kwargs)
        recorder('INFO', '{proc} end normally'.format(proc=self))

    def stop(self, entire=False):

        if entire:
            for process in self._fprocesses:
                process.terminate()
            recorder('INFO', 'entire processes stop')
        else:
            self.terminate()
            recorder('INFO', '{proc} stop'.format(proc=self))
