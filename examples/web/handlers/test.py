# coding:utf8

import time

from fastweb.web import Api, Page
from fastweb.exception import HttpError
from fastweb.component.request import Request
from fastweb.web import coroutine, run_on_executor


class Test(Api):
    
    @coroutine
    #@checkArgument(name=str, sex=int)
    def get(self):
        """
        #self.test_mongo.select('resource', 'mongo_question_json')
        #doc = yield self.test_mongo.find_one(limit=1)
        #
        self.load_executor(5)
        ret = yield self.test_mysql.query('select * from entity_question limit 20;')
        print(('+++++' + str(ret)))
        #yield self.test_mysql.query('select * from user;')
        print((self.test_mysql.fetch()))
        #for _ in xrange(30):
        #   yield self.test_mysql.query('select * from user;')

        #for _ in xrange(1):
            #yield self.hello_service.sayHello()

        yield self.test_redis.query('set name jackson')

        # ret = yield self.hello_service.sayHello()
        # print(ret)
        #ret = yield self.http_client.fetch('http://www.baidu.com')
        request = Request(method='GET', url='http://www.baidu.com')
        ret = yield self.http_request(request)

        r = yield self.test_executor()
        print(r)

        print('call task')
        yield self.test_task.call_async(args=(101, 2))
        x = yield self.test_task.call(args=(101, 2))
        print(('calculate: {}'.format(x)))
        """
        try:
            request = Request(method='GET', url='http://rw.okjiaoyu.cn/rw_0036a751376baf1ffd4fad61.ppt')
            r = yield self.http_request(request)
            print(r)
        except HttpError as e:
            print('http error: {e}'.format(e=type(e)))
            self.end(status_code=404)
            print('????')
            return

        self.end('SUC', log=False, **{'name': 0})
        return

    def on_chunk(self):
        print('on chunk')

    @run_on_executor
    def test_executor(self):
        time.sleep(0.1)
        return 1000


class ZohoOffice(Page):

    @coroutine
    def get(self):

        filename = 'rw_0018262027284b73f242508b.ppt'
        qiniu_url = 'http://rw.okjiaoyu.cn/{filename}'.format(filename=filename)
        print(qiniu_url)
        suffix = 'ppt'
        url = 'https://show.zoho.com/show/remotedoc.im'
        print(url)
        body = {'url': qiniu_url, 'apikey': 'd9b781738498ecf71d196c56d6353b77', 'mode': 'view', 'file_name': filename, 'lang': 'zh', 'format': suffix, 'output': 'url'}
        # body = urlencode(body)
        """
        request = Request(url=url, method='POST', body=body)
        response = yield self.http_request(request)

        print(response)
        """
        import requests
        response = requests.post(url, data=body).content
        URL = response.split('\n')[1]
        URL = URL[URL.find('=')+1:]
        print(URL)
        self.redirect(URL)


