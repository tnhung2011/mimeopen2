# -*- coding:utf-8 -*-

"""module work for windows machine

mimeopen program use the registry to find the proper apps

keep care that the _winreg lib only available on windows

created: 2016/3/18
author: smileboywtu

"""

from _winreg import (
    QueryInfoKey, QueryValueEx, OpenKey, EnumKey, CreateKeyEx, SetValueEx,
    REG_SZ, KEY_SET_VALUE, HKEY_CLASSES_ROOT, HKEY_CURRENT_USER,
    HKEY_LOCAL_MACHINE)


def open_with_list(ext):
    """get the open with list from the system registry

    this method find the HKEY_CLASSES_ROOT to load the application list.

    params:
        - ext file extention
    """

    key = OpenKey(HKEY_CLASSES_ROOT, None)
    key_no = QueryInfoKey(key)[0]

    all_keys = []
    for index in xrange(key_no):
        all_keys.append(EnumKey(key, index))

    filter_func = (
        lambda ext_:
            (ext_.endswith(ext) or ext_.endswith(ext.upper())) and
            (ext_ != ext and ext_ != ext.upper()))

    progids = filter(filter_func, all_keys)

    return progids


def get_prog_command(progid):
    """use the program id to find out program path

    params:
        progid - program id in registry
    """
    open_command = None
    edit_command = None

    sub_key = '\\'.join([
        progid, 'shell', 'edit', 'command'
    ])

    try:
        key = OpenKey(HKEY_CLASSES_ROOT, sub_key)
        edit_command = QueryValueEx(key, None)[0]
    except WindowsError:
        pass

    sub_key = '\\'.join([
        progid, 'shell', 'open', 'command'
    ])

    try:
        key = OpenKey(HKEY_CLASSES_ROOT, sub_key)
        open_command = QueryValueEx(key, None)[0]
    except WindowsError:
        pass

    return open_command, edit_command


def get_prog_name(progid):
    """use progid to find out the program name

    get this information from the uninstall list

    HKEY_LOCAL_MACHINE\SOFTWARE\
    Wow6432Node\Microsoft\Windows\
    CurrentVersion\Uninstall

    params:
        - program id in registry
    """
    open_comand, edit_command = get_prog_command(progid)

    prog_path = None
    prog_name = None

    if open_comand is not None:
        import re
        match = re.search(r'\"(.+)\\.+\.exe\"', open_comand)
        if match:
            prog_path = match.group(1)

    if not prog_path:
        return None

    sub_key = '\\'.join([
        'SOFTWARE', 'Wow6432Node', 'Microsoft', 'Windows',
        'CurrentVersion', 'Uninstall'
    ])

    key = OpenKey(HKEY_LOCAL_MACHINE, sub_key)
    key_no = QueryInfoKey(key)[0]

    for index in xrange(key_no):

        key_name = EnumKey(key, index)
        app_key = OpenKey(key, key_name)

        try:
            install_path = QueryValueEx(app_key, 'InstallLocation')[0]
            if prog_path in install_path:
                prog_name = QueryValueEx(app_key, 'DisplayName')[0]
                return prog_name
        except WindowsError:
            pass

        try:
            remove_path = QueryValueEx(app_key, 'UninstallString')[0]
            if prog_path in remove_path:
                prog_name = QueryValueEx(app_key, 'DisplayName')[0]
                return prog_name
        except WindowsError:
            pass

    return None


def set_user_editor(ext, progid, command):
    """set the default editor for the user

    this method rely on the program path

    params:
        ext - file ext
        progid - progid
        progpath - program execute path
    """
    sub_key = '\\'.join([
        'Software', 'Classes', ext
    ])

    key = CreateKeyEx(HKEY_CURRENT_USER, sub_key, 0, KEY_SET_VALUE)
    SetValueEx(key, None, 0, REG_SZ, progid)

    sub_key = '\\'.join([
        'Software', 'Classes', progid, 'shell', 'edit', 'command'
    ])

    key = CreateKeyEx(HKEY_CURRENT_USER, sub_key, 0, KEY_SET_VALUE)
    SetValueEx(key, None, 0, REG_SZ, command)


def set_user_choice(ext, progid):
    """set the default program for the ext

    you may batter make sure the progid exists and this program just work for
    open. do not for edit.

    params:
        - ext file extention
        - progid program id in regitstry
    """
    key_seq = '\\'.join([
        'Software', 'Microsoft', 'Windows',
        'CurrentVersion', 'Explorer', 'FileExts', ext, 'UserChoice'
        ])

    user_default = CreateKeyEx(HKEY_CURRENT_USER, key_seq, 0, KEY_SET_VALUE)

    SetValueEx(user_default, 'Progid', 0, REG_SZ, progid)


def query_user_choice(progs):
    """get the user choice from the list

    params:
        progs - program list
    """
    print "Available Program: "
    for index, prog in enumerate(progs):
        print '\t', index, ': ', prog[1]

    choice = None
    max_size = len(porgs)
    which not choice:
        choice = int(input('choose a program: '))
        if choice < max_size and choice > -1:
            return choice
        choice = None

    return -1


def execute_program(progpath, params=None):
    """run a program according to it's path on windows

    params:
        progpath - program execute path
        params - program params
    """
    import subprocess

    return subprocess.call(['CMD', '/C', progpath, params])


def mimeopen(filename):
    """mimeopen a filter_func

    open a file and supply enough programs

    params:
        filename - include the file extention
    """
    import re

    match = re.search(r'.+(\.[a-zA-Z0-9]+)', filename)
    if match:
        ext = match.group(1)

    progids = open_with_list(ext)

    proginfo = []
    for pid in progids:
        progname = get_prog_name(pid)
        if progname:
            proginfo.append((pid, progname))

    if proginfo:
        choice = query_user_choice(proginfo)
        progcommand = get_prog_command(proginfo[choice][0])
        match = re.search(r'\"(.+\.exe)\"', progcommand)
        error = execute_program(match.group(1), filename)
        if error:
            print 'Error happens when execute the program.'
    else:
        print 'No proper program found.'
