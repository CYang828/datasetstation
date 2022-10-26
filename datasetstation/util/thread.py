# coding:utf8

from threading import Thread, Event

from fastweb.util.log import recorder


class FThread(Thread):
    """封装系统thread，方便线程停止"""

    _fthreads = []

    def __init__(self, name, task, period=0, frequency=-1):
        """初始化线程

        :parameter:
         - `name`: 线程名
         - `task`: 任务函数,线程名会作为参数传递给task
         - `period`: 执行时间间隔
         - `frequency`： 执行次数，-1为永远执行，默认为永远执行
        """

        self._event = Event()
        self._period = period
        self._task = task
        self._frequency = frequency
        self._fthreads.append(self)
        super(FThread, self).__init__(name=name)

    def __str__(self):
        return '<Fthread|{name}>'.format(name=self.getName())

    def run(self):
        """运行函数,可以通过start开始线程,该函数会被自动调用"""

        while not self._event.isSet() and self._frequency:
            self._event.wait(self._period)
            self._task(self)
            self._frequency -= 1

    def join(self, timeout=0):
        """结束当前线程"""

        self._event.set()
        Thread.join(self, timeout)

    @staticmethod
    def stop(timeout=None):
        """等待所有线程执行完毕并结束线程"""

        for thread in FThread._fthreads:
            thread.join(timeout)
