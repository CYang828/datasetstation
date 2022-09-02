# coding:utf8


from fastweb.loader import app
from fastweb.service import start_service_server


if __name__ == '__main__':
    app.load_recorder('service.log', system_level='DEBUG')
    app.load_component(layout='service', backend='ini', path='service.ini')
    app.load_component(layout='service', backend='ini', path='component.ini')
    start_service_server()

