#!/usr/bin/env python
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

    def default(self, name):
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


class HasConfigBlock(object):

    def __init__(self, config_block):
        super(HasConfigBlock, self).__init__()
        self.config_block = config_block

    def options(self):
        return self.config_block['options']

    def configs(self):
        return self.config_block['configs']

    def servers(self):
        return self.config_block['servers']

    def server(self, name):
        for a_server in self.servers():
            if a_server.name == name:
                return a_server

    def binds(self):
        return self.config_block['binds']

    def acls(self):
        return self.config_block['acls']

    def acl(self, name):
        for a_acl in self.acls():
            if a_acl.name == name:
                return a_acl


class Global(HasConfigBlock):
    """Represens a `global` section
    """
    pass


class Defaults(HasConfigBlock):

    def __init__(self, name, config_block):
        super(Defaults, self).__init__(config_block)
        self.name = name


class Backend(HasConfigBlock):

    def __init__(self, name, config_block):
        super(Backend, self).__init__(config_block)
        self.name = name


class Listen(HasConfigBlock):
    def __init__(self, name, host, port, config_block):
        super(Listen, self).__init__(config_block)
        self.name = name
        self.host = host
        self.port = port


class Frontend(HasConfigBlock):
    def __init__(self, name, host, port, config_block):
        super(Frontend, self).__init__(config_block)
        self.name = name
        self.host = host
        self.port = port


class Server(object):
    """Represents the `server` line in config block

    Attributes:
        attributes (list): Description
        host (str): Description
        name (str): Description
        port (str): Description
    """
    def __init__(self, name, host, port, attributes):
        super(Server, self).__init__()
        self.name = name
        self.host = host
        self.port = port
        self.attributes = attributes or []

    def render(self):
        return '    server    %s    %s:%s    %s\n' % (
            self.name, self.host, self.port, ' '.join(self.attributes))

    def __str__(self):
        return self.render()


class Bind(object):
    """Represents the `bind` line in config block

    Attributes:
        attributes (str):
        host (srt):
        port (list):
    """
    def __init__(self, host, port, attributes):
        self.host = host
        self.port = port
        self.attributes = attributes or []

    def render(self):
        return '    bind    %s:%s    %s\n' % (
            self.host, self.port, ' '.join(self.attributes))

    def __str__(self):
        return self.render()


class Acl(object):
    """Represents the `acl` line in config block

    Attributes:
        name (str):
        value (str):
    """
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def render(self):
        return '    acl    %s    %s\n' % (self.name, self.value)

    def __str__(self):
        return self.render()


class UseBackend(object):
    """Represents the `use_backend` or `default_backend` line in config block

    Attributes:
        backend_condition (str): Description
        backend_name (str): Description
        is_default (bool): Description
        operator (str): Description
    """
    def __init__(self, backend_name, operator,
                 backend_condition, is_default=False):
        self.backend_name = backend_name
        self.operator = operator
        self.backend_condition = backend_condition
        self.is_default = is_default

    def render(self):
        backendtype = 'default_backend' if self.is_default else 'use_backend'
        return '    %s    %s    %s    %s\n' % (
            backendtype, self.backend_name,
            self.operator, self.backend_condition)

    def __str__(self):
        return self.render()
