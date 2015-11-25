#!/bin/env python
# -*- coding: utf8 -*-

import os

import pegnode
# import config


class Parser(object):
    """Do parsing the peg-tree and build the objects in config module

    Attributes:
        filestring (str): the content of haproxy config file
        pegtree (config.TreeNode): pegtree object for input filestring
    """
    def __init__(self, filepath='/etc/haproxy/haproxy.cfg'):
        self.filestring = self.__read_string_from_file(filepath)
        if not self.filestring:
            raise Exception('error reading from file %s' % filepath)
        self.pegtree = pegnode.parse(self.filestring)

    def build_global(self):
        """parse `global` section, and return a config.Global instance"""
        pass

    def build_defaults(self):
        """parse `defaults` sections, and return a list of config.Defaults"""
        pass

    def build_userlists(self):
        """parse `userlist` sections, and return a list of config.Userlist"""
        pass

    def build_listens(self):
        """parse `listen` sections, and return a list of config.Listen"""
        pass

    def build_frontends(self):
        """parse `frontend` sections, and return a list of config.Frontend"""
        pass

    def build_backends(self):
        """parse `backend` sections, and return a list of config.Backend"""
        pass

    def __read_string_from_file(self, filepath):
        filestring = ''
        if os.path.exists(filepath):
            with open(filepath) as f:
                f
                for line in f:
                    filestring = filestring + line
        return filestring
