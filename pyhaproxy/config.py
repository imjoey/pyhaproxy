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
        configs (list): config list
        options (list): option list
    """
    def __init__(self, configs, options):
        self.configs = configs
        self.options = options


class Default(object):
    def __init__(self, name, options, configs):
        self.name = name
        self.configs = configs
        self.options = options


class HasServer(object):

    def add_server(self, name, host, port, attributes):
        server = Server(name, host, port, attributes)
        self.servers.append(server)


class Backend(HasServer):
    '''
        `backend` section
    '''
    def __init__(self, name, options, configs):
        super(Backend, self).__init()
        self.name = name
        self.options = options
        self.configs = configs
        self.servers = []


class Listen(HasServer):
    def __init__(self, name, host, port, options, configs):
        super(Listen, self).__init__()
        self.name = name
        self.host = host
        self.port = port
        self.options = options
        self.configs = configs
        self.servers = []


class Frontend(HasServer):
    def __init__(self, name, host, port, options, configs):
        super(Frontend, self).__init__()
        self.name = name
        self.host = host
        self.port = port
        self.options = options
        self.configs = configs


class Server(object):

    def __init__(self, name, host, port, attributes):
        self.name = name
        self.host = host
        self.port = port
        self.attributes = attributes
