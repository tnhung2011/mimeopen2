#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import platform
import argparse import ArgumentParser

if platform.startswith('win32'):
    from win import mimeopen
elif platform.startswith('darwin'):
    from mac import mimeopen
elif platform.startswith('linux'):
    from linux import mimeopen
else:
    pass


def main():
    """main program entry point

    """
    parser = ArgumentParser()
    parser.add_argument('filename', type=str, help='filename to open')
    args = parser.parse_args()

    mimeopen(args.filename)


if __name__ == '__main__':
    main()
