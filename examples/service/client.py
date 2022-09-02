# coding:utf8
import logging
logging.basicConfig(level=logging.INFO)

import sys, glob
sys.path.append('fastweb_thrift_async')

from HelloService import HelloService
from HelloService.ttypes import *

from thrift import TTornado
from thrift.transport import TTransport
from thrift.protocol import TCompactProtocol
from thrift.protocol import TMultiplexedProtocol

from tornado import gen
from tornado import ioloop


@gen.coroutine
def communicate():
    # create client
    transport = TTornado.TTornadoStreamTransport('localhost', 7777)
    # open the transport, bail on error
    try:
        yield transport.open()
        print('Transport is opened')
    except TTransport.TTransportException as ex:
        logging.error(ex)
        raise gen.Return()

    protocol = TCompactProtocol.TCompactProtocolFactory()
    #pfactory = TMultiplexedProtocol.TMultiplexedProtocol(protocol, 'hello')
    client = HelloService.Client(transport, protocol)

    # ping
    yield client.sayHello()
    print("ping()")

    client._transport.close()
    raise gen.Return()


def main():
    # create an ioloop, do the above, then stop
    import time
    import _thread
    start = time.time()

    def _thread():
        ioloop.IOLoop.current().run_sync(communicate)

    for _ in range(5):
        _thread.start_new_thread(_thread, ())

    while 1:
        pass

    end = time.time()
    print((end-start))
if __name__ == "__main__":
    main()

