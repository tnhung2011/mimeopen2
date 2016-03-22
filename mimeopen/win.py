# -*- coding:utf-8 -*-

"""module work for windows machine

mimeopen program use the registry to find the proper apps

keep care that the _winreg lib only available on windows

created: 2016/3/18
author: smileboywtu

"""

from _winreg import (
    QueryInfoKey, OpenKey, CreateKeyEx, SetValueEx, REG_SZ, KEY_SET_VALUE,
    HKEY_CLASSES_ROOT, HKEY_CURRENT_USER)


def open_with_list(ext):
    """get the open with list from the system registry

    this method find the HKEY_CLASSES_ROOT to load the application list.

    params:
        - ext file extention
    """

    root_cls = OpenKey(HKEY_CLASSES_ROOT, None)
    key_no = QueryInfoKey(root_cls)[1]

    all_keys = []
    for index in xrange(key_no):
        all_keys.append(EnumKey(root_cls, index))

    filter_func = (
        lambda ext_:
            (ext_.endswith(ext) or ext_.endswith(ext.upper())) and
            (ext_ != ext and ext_ != ext.upper()))

    progids = filter(filter_func, all_keys)

    return progids


def get_prog_name(progid):
    """use progid to find out the program name

    params:
        - progid id in registry
    """
    pass


def set_user_choice(ext, progid):
    """set the default program for the ext

    params:
        - ext file extention
        - progid program id in regitstry
    """

    key_seq = '\\'.join([
        'Software', 'Microsoft', 'Windows',
        'CurrentVersion', 'Explorer', 'FileExts', ext
        ])

    user_cls = OpenKey(HKEY_CURRENT_USER, key_seq)

    user_default = CreateKeyEx(user_cls, 'UserChoice', 0, KEY_SET_VALUE)

    SetValueEx(user_default, 'Progid', REG_SZ, progid)


def open_by_default(filename):
    """open file by default program

    """
    import subprocess
    from appnotfound import AppNotFound

    error = subprocess.call(['cmd', '/c', 'start', filename])

    if error:
        raise AppNotFound(
            "can't found proper program to open the file: {}".format(filename))


def open_with_prog(progid, filename):
    """open the file with the program

    params:
        progid - program id in registry
        filename - file name to open
    """
    import subprocess

    key_seq = '\\'.join([
        progid, 'Shell', 'Open', 'Command'
    ])

    prog_cls = OpenKey(HKEY_CLASSES_ROOT, key_seq)

    command = EnumValue(prog_cls, 0)[2]

    # execute the command
    pass


def mimeopen(filename):
    """open a file according to it's mime type

    return a list of application that can open this filename
    """
    pass
