#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""module work for windows machine

mimeopen program use the registry to find the proper apps

keep care that the _winreg lib only available on windows

created: 2016/3/18
author: smileboywtu

"""


from _winreg import OpenKey, EnumKey, EnumValue, HKEY_CLASSES_ROOT


def open_by_default(filename):
    """open file by default program

    """
    import subprocess
    from appnotfound import AppNotFound

    error = subprocess.call(['cmd', '/c', 'start', filename])

    if error:
        raise AppNotFound(
            "can't found proper program to open the file: {}".format(filename))


def mimeopen(filename):
    """open a file according to it's mime type

    return a list of application that can open this filename
    """
    pass
