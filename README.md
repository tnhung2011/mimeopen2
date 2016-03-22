# mimeopen

open a file with file mimetype

this library is used when I design a desktop applicaiton in a
company. I need to let the user choose an editor to open a file.

current the library just support windows, mac, and ubuntu(linux).

Be care that the lib just test on ubuntu linux. for other platform
not guarantee. if you meet good idea, you can tell me.

# install

you can clone this repository, and then install it from source:

``` shell

python setup.py install

```

# usage

it's very simple:

``` shell

mimeopen filename

```

# implementation

## ubuntu

**1.** get the open with list from:

- **~/.local/share/applications/mimeapps.list**
- **/usr/share/applications/defaults.list**

**2.** you can get all apps from **/usr/share/applications**

after you find the file type associations, you can find the application
information inside the .desktop file.

## Windows

on window all the program information is saved in the registry, so just check the
registry to find out the program information.

**1.** the **HKEY_CLASSES_ROOT** contains information merged from the **HKEY_CURRENT_USER**
and **HKEY_LOCAL_MACHINE**, you can find the all the program can deal with ext.

**2.** if you want to set the default program for the current user, you can set the
program id for the UserChoice under **HKEY_CURRENT_USER\Software\Microsoft\Windows\Explorer\FileExts\ext\UserChoice**

**3.** if you want to open with a program id, you can just use the program id to get
the program shell command to open the program.
