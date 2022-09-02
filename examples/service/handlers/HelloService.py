# coding:utf8

"""generate by fasthrift"""


from fastweb.service import ABLogic


class HelloServiceHandler(ABLogic):

    def sayHello(self):
        import pdb; pdb.set_trace()
        print('hello')
        pass




