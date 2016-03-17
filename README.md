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

