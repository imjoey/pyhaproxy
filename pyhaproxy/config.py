#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Configuration(object):
    """Represents a whole haproxy config file

    Attributes:
        pegtree (TreeNode): the original parsing pegtree
    """
    def __init__(self, pegtree):
        self.pegtree = pegtree
        self.defaults = []
        self.backends = []
        self.frontends = []
        self.listens = []
        self.userlists = []
        self.globall = None

    def userlist(self, name):
        for userlist in self.userlists:
            if userlist.name == name:
                return userlist

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

    def users(self):
        return self.config_block['users']

    def user(self, name):
        for user in self.users():
            if user.name == name:
                return user

    def groups(self):
        return self.config_block['groups']

    def group(self, name):
        for group in self.groups():
            if group.name == name:
                return group

    def usebackends(self):
        return self.config_block['usebackends']


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


class Userlist(HasConfigBlock):
    """Represents the `userlist` section

    Attributes:
        name (str): Description
    """
    def __init__(self, name, config_block):
        super(Userlist, self).__init__(config_block)
        self.name = name


class Server(object):
    """Represents the `server` line in config block

    Attributes:
        name (str): Description
        host (str): Description
        port (str): Description
        attributes (list): Description
    """
    def __init__(self, name, host, port, attributes=[]):
        super(Server, self).__init__()
        self.name = name
        self.host = host
        self.port = port
        self.attributes = [attr.strip() for attr in attributes]

    def __str__(self):
        return '<server_line: %s %s:%s %s>' % (
            self.name, self.host, self.port, ' '.join(self.attributes))


class Bind(object):
    """Represents the `bind` line in config block

    Attributes:
        host (srt):
        port (list):
        attributes (str):
    """
    def __init__(self, host, port, attributes):
        self.host = host
        self.port = port
        self.attributes = attributes or []

    def __str__(self):
        return '<bind_line: bind %s:%s %s>' % (
            self.host, self.port, ' '.join(self.attributes))


class Acl(object):
    """Represents the `acl` line in config block

    Attributes:
        name (str):
        value (str):
    """
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        return '<acl_line: acl %s %s>' % (self.name, self.value)


class User(object):
    """Represents the `user` line in config block

    Attributes:
        name (str): Description
        passwd (str): Description
        passwd_type ('password' or 'insecure-password'): Description
        group_names (list(str)): Description
    """
    def __init__(self, name, passwd, passwd_type, group_names):
        super(User, self).__init__()
        self.name = name
        self.passwd = passwd
        self.passwd_type = passwd_type
        self.group_names = group_names or []

    def __str__(self):
        if self.group_names:
            group_fragment = 'groups ' + ','.join(self.group_names)
        else:
            group_fragment = ''
        return '<user_line: user %s %s %s %s>' % (
            self.name, self.passwd_type, self.passwd, group_fragment)


class Group(object):
    """Represents the `group` line in config block

    Attributes:
        name (str): Description
        user_names (list(str)): Description
    """
    def __init__(self, name, user_names):
        super(Group, self).__init__()
        self.name = name
        self.user_names = user_names or []

    def __str__(self):
        if self.user_names:
            user_fragment = 'users ' + ', '.join(self.user_names)
        else:
            user_fragment = ''

        return '<group_line: group %s %s>' % (self.name, user_fragment)


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

    def __str__(self):
        backendtype = 'default_backend' if self.is_default else 'use_backend'
        return '<backend_line: %s %s %s %s>' % (
            backendtype, self.backend_name,
            self.operator, self.backend_condition)
