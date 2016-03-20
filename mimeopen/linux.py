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
    2. ~/.local/share/applications

    """

    associations = []
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
    app_info = {}

    for app in apps:
        for path in assoc_path:
            if app not in os.listdir(path):
                continue
            filepath = os.path.join(path, app)
            with open(filepath, 'r') as fp:
                name = ''
                exe = ''
                for line in fp:
                    if line.startswith('Name='):
                        name = line.split('=')[1]
                    if line.startswith('Exec='):
                        exe = line.split('=')[1]
                    if name and exe:
                        app_info[name] = exe
                        break

    return app_info


def get_open_with_list(associations, filename):
    """get the open with list according to file type

    this method find all the application that can open this file
    currently the method only find out the mimetype according to
    the file name.

    """
    import mimetypes
    mime, _ = mimetypes.guess_type(filename)

    apps = []
    for assoc in associations:
        with open(assoc, 'r') as fp:
            for line in fp:
                items = line.strip(';').split('=')
                if items[0] == mime:
                    apps.append(items[1])

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


def mimeopen(filename):
    """open the file

    let the user choose what to use

    """

    assocs = get_assoc_map_file()

    app_info = get_open_with_list(assocs, filename)

    return app_info
