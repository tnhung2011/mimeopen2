#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""find the proper app to open file
this script work only with ubuntu currently.

created: 2016/3/17
author: smileboywtu

"""


import os

home = os.environ['HOME']
user_assoc = os.path.join(home, '.local', 'share', 'applications')
sys_assoc = os.path.join('/', 'usr', 'share', 'applications')

assoc_path = [user_assoc, sys_assoc]


def get_assoc_map_file():
    """get mimetype association files

    1. /usr/share/application/*.list
    2. ~/.local/share/applications/*.list

    """

    associations = None
    for path in assoc_path:
        for filename in os.listdir(path):
            if filename.endswith('.list'):
                associations.append(os.path.join(path, filename))

    return associations


def get_app_info(apps):
    """apps can be found in
    1. /usr/share/applications
    2. ~/.local/share/applications

    other application can only be found by command.
    """
    import re
    app_info = {} # ???

    for app in apps:
        for path in assoc_path:
            if app not in os.listdir(path):
                continue
            filepath = os.path.join(path, app)
            with open(filepath, 'r') as fp:
                name = None
                exe = None
                for line in fp:
                    if name and exe:
                        app_info[name] = exe
                        break
                    match = re.search(r'^Name=(.+)\n', line)
                    if match and not name:
                        name = match.group(1)
                    match = re.search(r'^Exec=(.+)\n', line)
                    if match and not exe:
                        exe = match.group(1)

    return app_info


def get_open_with_list(associations, filename):
    """get the open with list according to file type

    this method find all the application that can open this file
    currently the method only find out the mimetype according to
    the file name.

    """
    import re
    import mimetypes
    mime, _ = mimetypes.guess_type(filename)

    apps = None
    for assoc in associations:
        with open(assoc, 'r') as fp:
            for line in fp:
                line = line.strip('\n').strip(';')
                if mime in line:
                    items = re.split(r'[=;]', line)
                    if mime in items:
                        items.remove(mime)
                        apps.extend(items)

    apps = list(set(apps))
    app_list = get_app_info(apps)
    return app_list


def open_with_default(filename):
    """open the file with default app

    use system interface to open a file.

    """
    import subprocess

    error = subprocess.call(['xdg-open', filename])

    if error:
        error = subprocess.call(['open', filename])

    if error:
        print "can't open the file."


def query_user_choice(appinfo):
    """query the user choice from the app list.

    """
    print 'Available programs:'
    for index, name in enumerate(appinfo.keys()):
        print index, '):', name

    choice = None
    max_size = len(appinfo)
    while not choice:
        choice = int(input('choose a program: '))
        if choice < max_size and choice > -1:
            return choice
        choice = None
    return -1


def mimeopen(filename):
    """open the file

    let the user choose what to use

    """
    from subprocess import run

    assocs = get_assoc_map_file()

    app_info = get_open_with_list(assocs, filename)

    choice = query_user_choice(app_info)

    command = app_info.values()[choice]

    run([command])


if __name__ == '__main__':
    filename = 'young.mp3'
    mimeopen(filename)
