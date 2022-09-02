# coding:utf8


from fastweb.service import ABLogic


class HelloServiceHandler(ABLogic):
    def sayHello(self):
        # self.test_mysql.query('select * from entity_question limit 20;')
        # print self.test_mysql.fetch()
        # import pdb; pdb.Pdb().set_trace()
        print('sayHello')
        return 'hello'
