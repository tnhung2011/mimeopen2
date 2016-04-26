# -*- coding:utf-8 -*-

"""module work for windows machine

mimeopen program use the registry to find the proper apps

keep care that the _winreg lib only available on windows

created: 2016/3/18
author: smileboywtu

"""

from _winreg import (
    QueryInfoKey, QueryValueEx, OpenKey, EnumKey, CreateKeyEx, SetValueEx,
    ExpandEnvironmentStrings, REG_SZ, KEY_SET_VALUE,
    HKEY_CLASSES_ROOT, HKEY_CURRENT_USER, HKEY_LOCAL_MACHINE
)


def get_command(key, sub_key):
    """get the open and edit command under the key
    @params:
        key -- registry key
        sub_key -- sub key
    @return:
        command
    """
    command = None
    try:
        key = OpenKey(key, sub_key)
        command = QueryValueEx(key, None)[0]
    except OSError:
        pass
    return command


def get_exe_command(exe):
    """get the application run command

    @params:
        exe -- application
    @return:
        command -- command
    """
    sub_key = '\\'.join([
        'Applications', exe
    ])

    try:
        key = OpenKey(HKEY_CLASSES_ROOT, sub_key)
    except WindowsError:
        return None

    sub_key = '\\'.join([
        'shell', 'edit', 'command'
    ])
    edit_command = get_command(key, sub_key)
    sub_key = '\\'.join([
        'shell', 'open', 'command'
    ])
    open_command = get_command(key, sub_key)

    if not (open_command or edit_command):
        return None

    return edit_command or open_command


def get_wildcard_program():
    """find all exe inside the wildcard key
    @params:
        None
    @return
        [(name, command)] -- program name and command
    """
    import re

    sub_key = r'\*\OpenWithList'
    key = OpenKey(HKEY_CLASSES_ROOT, sub_key)

    key_no = QueryInfoKey(key)[0]

    exes = []
    for index in xrange(key_no):
        exe = EnumKey(key, index)
        if exe.lower().endswith('.exe'):
            command = get_exe_command(exe)
            if not command:
                continue
            match = re.search(u'.+\\\\(\w+)\.exe', command,  flags=re.IGNORECASE)
            if match:
                name = match.group(1)
                progid = '.'.join([name, 'edo'])
                exes.append((name, progid, command))
        else:
            sub_key = '\\'.join([
                exe, 'shell', 'edit', 'command'
            ])
            edit_command = get_command(key, sub_key)
            sub_key = '\\'.join([
                exe, 'shell', 'open', 'command'
            ])
            open_command = get_command(key, sub_key)

            if not (open_command or edit_command):
                continue

            command = edit_command or open_command
            match = re.search(u'.+\\\\(\w+)\.exe', command,  flags=re.IGNORECASE)
            if match:
                name = match.group(1)
                progid = '.'.join([name, 'edo'])
                exes.append((name, progid, command))
    return exes


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

    if not (open_command or edit_command):
        return None

    return edit_command or open_command


def open_program(ext):
    """get the open with list for the ext

    1. open with list

    2. open with progids

    @params:
        ext -- file extention
    @return
        (name, progid, command) -- program name and program command
    """
    import re

    # get the open with list
    sub_key = '\\'.join([
        ext, 'OpenWithList'
    ])

    try:
        key = OpenKey(HKEY_CLASSES_ROOT, sub_key)
    except WindowsError:
        return None

    key_no = QueryInfoKey(key)[0]

    exes = []
    for index in xrange(key_no):
        exe = EnumKey(key, index)
        if exe.lower().endswith('.exe'):
            command = get_exe_command(exe)
            if not command:
                continue
            match = re.search(u'.+\\\\(\w+)\.exe', command,  flags=re.IGNORECASE)
            if match:
                name = match.group(1)
                progid = '.'.join([name, 'edo'])
                exes.append((name, progid, command))
        else:
            sub_key = '\\'.join([
                exe, 'shell', 'edit', 'command'
            ])
            edit_command = get_command(key, sub_key)
            sub_key = '\\'.join([
                exe, 'shell', 'open', 'command'
            ])
            open_command = get_command(key, sub_key)

            if not (open_command or edit_command):
                continue

            command = edit_command or open_command
            match = re.search(u'.+\\\\(\w+)\.exe', command,  flags=re.IGNORECASE)
            if match:
                name = match.group(1)
                progid = '.'.join([name, 'edo'])
                exes.append((name, progid, command))
    return exes


def edit_program(ext):
    """get the edit progid
    @params:
        ext -- file extention
    @return
        (name, command) -- program name and program command
    """
    import re

    key = OpenKey(HKEY_CLASSES_ROOT, None)
    key_no = QueryInfoKey(key)[0]

    # get all sub keys
    all_keys = []
    for index in xrange(key_no):
        all_keys.append(EnumKey(key, index))

    # check if the default program already in list
    key = OpenKey(HKEY_CLASSES_ROOT, ext)
    progids = [QueryValueEx(key, None)[0]]
    key_no = QueryInfoKey(key)[0]
    for index in xrange(key_no):
        _id = EnumKey(key, index)
        if _id in all_keys:
            progids.append(_id)

    key = OpenKey(HKEY_CLASSES_ROOT, None)
    key_no = QueryInfoKey(key)[0]

    filter_func = (
        lambda ext_:
            (ext_.endswith(ext) or ext_.endswith(ext.upper())) and
            (ext_ != ext and ext_ != ext.upper()))
    progids.extend(filter(filter_func, all_keys))

    exes = []
    for progid in progids:
        name = get_prog_name(progid)
        command = get_prog_command(progid)
        if name and command:
            exes.append((name, progid, command))
        if command and not name:
            match = re.search(u'.+\\\\(\w+)\.exe', command,  flags=re.IGNORECASE)
            if match:
                name = match.group(1)
                exes.append((name, progid, command))
    return exes


def assoc_ext_programs(ext):
    """get all the programs can deal with the ext

    params:
        ext -- file extention
    return:
        (name, path) -- program name and run time command
    """
    programs = []

    # try to get edit_program
    programs.extend(edit_program(ext))

    # try to get open_program
    if not programs:
        programs.extend(open_program(ext))

    # append wildcard
    programs.extend(get_wildcard_program())

    return list(set(programs))


def search_name(locals, prog_path):
    """use the prog_path to find out the program display name

    locals: -- (main_key, sub_key)
    prog_path: -- program execute path

    return prog_name

    """

    for local in locals:

        key = OpenKey(*local)
        key_no = QueryInfoKey(key)[0]

        for index in xrange(key_no):

            key_name = EnumKey(key, index)
            app_key = OpenKey(key, key_name)

            for value_name in ('InstallLocation', 'LocationRoot', 'UninstallString'):
                try:
                    value_data = QueryValueEx(app_key, value_name)[0]
                    if value_data and (value_data.startswith(prog_path) or prog_path.startswith(value_data)):
                        prog_name = QueryValueEx(app_key, 'DisplayName')[0]
                        return prog_name
                except WindowsError:
                    pass

    return None


def get_prog_name(progid):
    """use progid to find out the program name

    get this information from the uninstall list

    HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall

    HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Uninstall

    HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall

    params:
        - program id in registry
    """
    command = get_prog_command(progid)

    prog_path = None

    if command:
        import re
        match = re.search(u'\"(.+)\\\\\w+\.exe\"\s',
                          command, flags=re.IGNORECASE)
        if match:
            prog_path = match.group(1)

    if not prog_path:
        return None

    locals = []

    main_key = HKEY_LOCAL_MACHINE
    sub_key = '\\'.join([
        'SOFTWARE', 'Wow6432Node', 'Microsoft', 'Windows',
        'CurrentVersion', 'Uninstall'
    ])
    locals.append((main_key, sub_key))

    main_key = HKEY_LOCAL_MACHINE
    sub_key = '\\'.join([
        'Software', 'Microsoft', 'Windows',
        'CurrentVersion', 'Uninstall'
    ])
    locals.append((main_key, sub_key))

    main_key = HKEY_CURRENT_USER
    sub_key = '\\'.join([
        'SOFTWARE', 'Microsoft', 'Windows',
        'CurrentVersion', 'Uninstall'
    ])
    locals.append((main_key, sub_key))

    return search_name(locals, prog_path)


def set_user_editor(ext, progid, command):
    """set the default editor for the user

    this method rely on the program path

    params:
        ext - file ext
        progid - progid
        progpath - program execute path
    """

    # must use the expand winreg string, if not, you may not have access
    # to the app and you need to use REG_EXPAND_SZ value type
    command = ExpandEnvironmentStrings(command)

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
    for index, name, progid, command in enumerate(progs):
        print '\t', index, ': ', name

    choice = None
    max_size = len(progs)
    while not choice:
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

    match = re.search(r'.+(\.[\w]+)', filename)
    if match:
        ext = match.group(1)

    proginfo = assoc_ext_programs(ext)

    if proginfo:
        choice = query_user_choice(proginfo)
        command = ExpandEnvironmentStrings(proginfo[choice][2])
        match = re.search(r'\"(.+\.exe)\"', command[0])
        error = execute_program(match.group(1), filename)
        if error:
            print 'Error happens when execute the program.'
    else:
        print 'No proper program found.'
