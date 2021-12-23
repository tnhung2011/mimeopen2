# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='mimeopen',
    version='2.0-alpha',
    packages=['mimeopen'],
    description='get open with list for a file',
    author='smileboywtu',
    author_email="smileboywtu@gmail.com",
    url='http://smileboywtu.github.io/articles/2016/03/13/python-get-system-default-app-related-a-mime-type.html',
    license='GPL3',
    required=None,
    entry_points={
        'console_scripts': [
            'mimeopen = mimeopen.__init__:main',
        ]
    }
)
