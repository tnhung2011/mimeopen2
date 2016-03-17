#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

if sys.platform.startswith('win32'):
    from win import mimeopen
elif sys.platform.startswith('darwin'):
    from mac import mimeopen
elif sys.platform.startswith('linux'):
    from linux import mimeopen
else:
    pass
