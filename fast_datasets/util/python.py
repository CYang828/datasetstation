# coding:utf8

"""python util"""

import six
import json
import hashlib
from importlib import import_module
from thrift.TTornado import TTransportException

import fastweb
from fastweb.accesspoint import coroutine, Return


def head(o, h):
    return '{head}{ori}'.format(head=h, ori=o)


def write_file(filepath, content, pattern='a+'):
    with open(filepath, pattern) as f:
        f.write(content)


def filepath2pythonpath(filepath):
    if filepath.startswith('./'):
        filepath = filepath.lstrip('./')

    if filepath.endswith('/'):
        filepath = filepath.rstrip('/')

    pythonpath = filepath.replace('/', '.')
    return pythonpath


def format(st, whole=0):
    if whole:
        return '\n'.join([head(e, whole * ' ') for e in st.split('\n')])
    else:
        return st


def dumps(obj, indent, whole=0):
    if whole:
        return '\n'.join([head(e, whole * ' ') for e in json.dumps(obj, indent=indent).split('\n')])
    else:
        return json.dumps(obj, indent=indent)


def to_iter(e):
    """转换可迭代形式"""

    if isinstance(e, (six.string_types, six.string_types, six.class_types, six.text_type,
                      six.binary_type, six.class_types, six.integer_types, float)):
        return e,
    elif isinstance(e, list):
        return e
    else:
        return e


def to_plain(i):
    """转换不可迭代形式"""

    if isinstance(i, dict):
        plain = ''
        for key, value in i:
            plain += "{key}:{value}".format(key=key, value=value)
        return plain
    elif isinstance(i, (list, set)):
        return ','.join([utf8(a) for a in i])
    else:
        return i


def mixin(cls, mixcls, resume=False):
    """动态继承"""

    mixcls = to_iter(mixcls)

    if resume:
        cls.__bases__ = mixcls
    else:
        for mcls in mixcls:
            cls.__bases__ += (mcls,)


class ExceptionProcessor(object):
    """异常处理器"""

    def __init__(self, exception, processor):
        self.exception = exception
        self.processor = processor


class AsynProxyCall(object):
    """异步调用代理,用来解决__getattr__无法传递多个参数的问题"""

    def __init__(self, proxy, method, throw_exception=None, exception_processor=None):
        self.proxy = proxy
        self._method = method
        self._throw_exception = throw_exception
        self._exception_processor = exception_processor
        self._arg = None
        self._kwargs = None

    @coroutine
    def __call__(self, *arg, **kwargs):
        self._arg = arg
        self._kwargs = kwargs
        self.proxy.recorder('INFO', 'call {proxy} <{method}> start'.format(proxy=self.proxy, method=self._method))
        try:
            with fastweb.util.tool.timing('ms', 8) as t:
                ret = yield getattr(self.proxy.other, self._method)(*arg, **kwargs)
            self.proxy.recorder('INFO', 'call {proxy} <{method}> successful\n{ret} <{time}>'.format(proxy=self.proxy,
                                                                                                    method=self._method,
                                                                                                    ret=ret,
                                                                                                    time=t))
            raise Return(ret)
        except TTransportException as e:
            self.proxy.recorder('ERROR',
                                'call {proxy} <{method}> error {e} ({msg})\nreconnect'.format(proxy=self.proxy,
                                                                                              method=self._method,
                                                                                              e=type(e), msg=e))
            yield self._exception_processor.processor()
            self(*self._arg, **self._kwargs)
        else:
            raise self._throw_exception


def load_module(path):
    return import_module(path)


def load_object(path):
    """Load an object given its absolute object path, and return it.

    object can be a class, function, variable or an instance.
    path ie: 'scrapy.downloadermiddlewares.redirect.RedirectMiddleware'
    """
    try:
        dot = path.rindex('.')
    except ValueError:
        raise ValueError("Error loading object '%s': not a full path" % path)

    module, name = path[:dot], path[dot + 1:]
    mod = import_module(module)

    try:
        obj = getattr(mod, name)
    except AttributeError:
        raise NameError("Module '%s' doesn't define any object named '%s'" % (module, name))

    return obj


def merge():
    """类合并"""
    pass


def enum(**enums):
    return type('Enum', (), enums)


def isset(v):
    try:
        type(eval(v))
    except:
        return False
    else:
        return True


def md5(s):
    md = hashlib.md5()
    md.update(s)
    return md.hexdigest()


def guess_type(v):
    if v.isdigit():
        return int(v)
    else:
        return str(v)


def utf8(d):
    if isinstance(d, bytes):
        return d.decode('utf-8')
    if isinstance(d, dict):
        return dict(map(utf8, d.items()))
    if isinstance(d, tuple):
        return map(utf8, d)
    return d


def list2dict(l):
    for idx, v in enumerate(l):
        if v.isdigit():
            l[idx] = int(v)

    return dict(zip(l[0::2], l[1::2]))


def dict2list(d):
    l = []
    for k, v in zip(d.keys(), d.values()):
        l.append(str(k))
        l.append("'" + str(v) + "'")
    return l


def list2sequence(l):
    s = ''
    for idx, i in enumerate(l):
        if isinstance(i, dict):
           i = '"' + dict2sequence(i) + '"'
        s += str(i)
        if idx != len(l) - 1:
            s += ' '
    return s


def dict2sequence(d):
    return ' '.join(dict2list(d))


def sequence2dict(s):
    sq = sequence2list(utf8(s))

    if len(sq) == 1:
        return s
    else:
        return list2dict(sq)


def sequence2list(s):
    l = []
    lv = ''
    fs = False

    for w in s:
        w = utf8(w)
        if w == "'" and not fs:
            fs = True
            continue
        elif w == "'" and fs:
            fs = False
            lv and l.append(lv)
            lv = ''
            continue
        elif w == ' ' and not fs:
            lv and l.append(lv)
            lv = ''
            continue
        lv += w
    return l


def str2everything(s):
    """convert str to the most possibility type

    support type:
        int
        float
        boolean: yes, no
        str,
        list
    """

    try:
        # int, float
        c = eval(s)
        if isinstance(c, (int, float)):
            return c
        else:
            return utf8(s)
    except NameError:
        # boolean, str, list
        if s.lower() == 'yes':
            return True
        elif s.lower() == 'no':
            return False
        elif len(s.split(',')) > 1:
            return [i for i in s.split(',') if i]
        else:
            return utf8(s)
    except (SyntaxError, TypeError):
        return utf8(s)


