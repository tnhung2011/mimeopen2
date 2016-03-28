# -*- coding:utf-8 -*-

"""mimeopen implementation for mac

created: 2016/3/28
author: smileboywtu
"""

import os
import re
from plistlib import readPlist
from xml.parsers.expat import ExpatError

HOME = os.environ['HOME']

sys_app = os.path.join('/', 'Applications')
usr_app = os.path.join(HOME, 'Applications')

app_dir = [sys_app, usr_app]


def is_support_ext(appdir, ext):
    """get the program supported mimetype and execute path

    params:
        appdir -- directory to the app
        ext -- file extention
    """
    path = os.path.join(appdir, 'Contents', 'Info.plist')
    try:
        info = readPlist(path)
        for data in info['CFBundleDocumentTypes']:
            supported = data['CFBundleTypeExtensions']
            if ext in supported or '*' in supported:
                return info['CFBundleName']
    except KeyError:
        pass
    except ExpatError:
        print 'not well-formed, ', path

    return None


def get_open_with_list(ext):
    """use the file extention to get the proper application

    params:
        ext -- extention for the filename
    """
    apps = []
    for path in app_dir:
        for prog in os.listdir(path):
            match = re.search(r'.+\.app$', prog)
            if match:
                road = os.path.join(path, prog)
                name = is_support_ext(road, ext)
                if name:
                    apps.append((name, road))
            elif os.path.isdir(os.path.join(path, prog)):
                nest = os.path.join(path, prog)
                for prog in os.listdir(nest):
                    match = re.search(r'.+\.app$', prog)
                    if match:
                        road = os.path.join(nest, prog)
                        name = is_support_ext(road, ext)
                        if name:
                            apps.append((name, road))
    return apps


def open_with_default(filename):
    """open with the default program

    params:
        filename --  file to be opened
    """
    import subprocess

    error = subprocess.call(['open', filename])

    if error:
        print 'fail to open the file.'


def query_user_choice(apps):
    """let the user choose the proper apps

    params:
        apps -- proper app to choose to open the file
    """
    print 'Available program:'
    for index, prog in enumerate(apps):
        print index, '):', prog[0]

    max_size = len(apps)
    choice = None

    while not choice:
        choice = int(input('choose a program: '))
        if choice < max_size and choice > -1:
            return choice
        choice = None


def mimeopen(filename):
    """use the available application to open a file

    params:
        filename -- the file to be opened, must contains the file extention

    """
    import subprocess

    match = re.search(r'.+\.(\w+)$', filename)
    if not match:
        print 'no file extention found, the program may be failed on this.'

    ext = match.group(1)

    apps = get_open_with_list(ext)

    choice = query_user_choice(apps)

    subprocess.call(['open', '-a', apps[choice][1], filename])


if __name__ == '__main__':
    filename = 'young.docx'
    mimeopen(filename)
