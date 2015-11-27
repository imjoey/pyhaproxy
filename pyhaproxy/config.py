#!/usr/bin/env
# -*- coding: utf-8 -*-


class Configration(object):
    """Represents a whole haproxy config file

    Attributes:
        backends (list): the `backend` sections
        defaults (list): the `defaults` sections
        frontends (list): the `frontend` sections
        globall (config.Global): the `global` section
        listens (list): the `listen` sections
        pegtree (TYPE): the original parsing pegtree
    """
    def __init__(self, pegtree):
        self.pegtree = pegtree
        self.defaults = []
        self.backends = []
        self.frontends = []
        self.listens = []
        self.globall = None

    def listen(self, name):
        for listen in self.listens:
            if listen.name == name:
                return listen

    def defaults(self, name):
        for default in self.defaults:
            if default.name == name:
                return default

    def backend(self, name):
        for backend in self.backends:
            if backend.name == name:
                return backend

    def frontend(self, name):
        for frontend in self.frontends:
            if frontend.name == name:
                return frontend


class Global(object):
    """Represens a `global` section

    Attributes:
        config_block (dict):
    """
    def __init__(self, config_block):
        super(Global, self).__init__()
        self.config_block = config_block


class Defaults(object):
    def __init__(self, name, config_block):
        super(Defaults, self).__init__()
        self.name = name
        self.config_block = config_block


class Backend(object):
    '''
        `backend` section
    '''
    def __init__(self, name, config_block):
        super(Backend, self).__init__()
        self.name = name
        self.config_block = config_block


class Listen(object):
    def __init__(self, name, host, port, config_block):
        super(Listen, self).__init__()
        self.name = name
        self.host = host
        self.port = port
        self.config_block = config_block


class Frontend(object):
    def __init__(self, name, host, port, config_block):
        super(Frontend, self).__init__()
        self.name = name
        self.host = host
        self.port = port
        self.config_block = config_block


class Server(object):

    def __init__(self, name, host, port, attributes):
        super(Server, self).__init__()
        self.name = name
        self.host = host
        self.port = port
        self.attributes = attributes or []


class Bind(object):
    def __init__(self, host, port, attributes):
        self.host = host
        self.port = port
        self.attributes = attributes or []


class Acl(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value


class UseBackend(object):
    def __init__(self, backend_name, operator,
                 backend_condition, is_default=False):
        self.backend_name = backend_name
        self.operator = operator
        self.backend_condition = backend_condition
        self.is_default = is_default
