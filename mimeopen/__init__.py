#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse

if sys.platform.startswith('win32'):
    from win import mimeopen
elif sys.platform.startswith('darwin'):
    from mac import mimeopen
elif sys.platform.startswith('linux'):
    from linux import mimeopen
else:
    pass


def main():
    """main program entry point

    """
    parser = argparse.ArgumentParser()

    parser.add_argument('filename', type=str, help='filename to open')

    args = parser.parse_args()

    mimeopen(args.filename)


if __name__ == '__main__':
    main()
