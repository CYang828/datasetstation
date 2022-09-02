# coding:utf8

import re
import inspect


def get_class_from_frame(fr):
    args, _, _, value_dict = inspect.getargvalues(fr)

    if len(args) and args[0] == 'self':
        instance = value_dict.get('self', None)

        if instance:
            return getattr(instance, '__class__', None)

    return None


def get_file_name_in_full_path(file_path):
    return file_path.split('/')[-1]


def get_meta_data():
    frames = inspect.stack()
    chain_list = []

    for i in range(0, len(frames)):
        _, file_path, _, func_name, _, _ = frames[i]
        file_name = get_file_name_in_full_path(file_path)

        try:
            args = re.findall('\((.*)\)', frames[i + 1][-2][0])[0]
        except IndexError as e:
            func = get_class_from_frame(frames[2][0])

            if func:
                func_name = func.__name__

            args = ''
        except TypeError as e:
            func = get_class_from_frame(frames[2][0])

            if func:
                func_name = func.__name__

            args = ''

        current_chain = '%s:%s(%s)' % (file_name, func_name, args)
        chain_list.append(current_chain)

    chain_list.reverse()
    return ' --> '.join(chain_list[:-2])


def get_simple_meta_data():
    frames = inspect.stack()
    try:
        obj, file_path, line_no, func_name, _, _ = frames[3]
        return (func_name + ':' + str(line_no))
    except IndexError as e:
        return ''
