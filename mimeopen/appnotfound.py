#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""application not found exception

design for application not found exception

created: 2016/3/17
author: smileboywtu

"""


class AppNotFound(Exception):
    """app not found
    """
    def __init__(self, msg, *args, **kwargs):
        """init the object
        """
        self.msg = msg
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        """show message
        """
        return self.msg
