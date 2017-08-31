#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Configuration(object):
    """Represents a whole haproxy config file

    Attributes:

    """
    def __init__(self):
        self.__defaults = []
        self.__backends = []
        self.__frontends = []
        self.__listens = []
        self.__userlists = []
        self.__globall = None

    @property
    def globall(self):
        return self.__globall

    @globall.setter
    def globall(self, globall):
        self.__globall = globall

    @property
    def userlists(self):
        return self.__userlists

    def userlist(self, name):
        for userlist in self.__userlists:
            if userlist.name == name:
                return userlist

    @property
    def listens(self):
        return self.__listens

    def listen(self, name):
        for listen in self.__listens:
            if listen.name == name:
                return listen

    @property
    def defaults(self):
        return self.__defaults

    def default(self, name):
        for default in self.__defaults:
            if default.name == name:
                return default

    @property
    def backends(self):
        return self.__backends

    def backend(self, name):
        for backend in self.__backends:
            if backend.name == name:
                return backend

    @property
    def frontends(self):
        return self.__frontends

    def frontend(self, name):
        for frontend in self.__frontends:
            if frontend.name == name:
                return frontend


class HasConfigBlock(object):

    def __init__(self, config_block):
        super(HasConfigBlock, self).__init__()
        self.config_block = config_block

    def __find_configs(self, config_type):
        configs = []
        for line in self.config_block:
            if isinstance(line, config_type):
                configs.append(line)
        return configs

    def __add_node(self, node, node_type):
        if not isinstance(node, node_type):
            raise Exception('config.%s is only supported' % node_type)
        self.config_block.append(node)

    def options(self):
        return self.__find_configs(Option)

    def option(self, keyword, value):
        for line in self.config_block:
            if isinstance(line, Option):
                if line.keyword == keyword and line.value == value:
                    return line

    def add_option(self, option):
        self.__add_node(option, Option)

    def remove_option(self, keyword, value):
        option = self.option(keyword, value)
        if option:
            self.config_block.remove(option)

    def configs(self):
        return self.__find_configs(Config)

    def config(self, keyword, value):
        for line in self.config_block:
            if isinstance(line, Config):
                if line.keyword == keyword and line.value == value:
                    return line

    def add_config(self, config):
        self.__add_node(config, Config)

    def remove_config(self, keyword, value):
        config = self.config(keyword, value)
        if config:
            self.config_block.remove(config)

    def servers(self):
        return self.__find_configs(Server)

    def server(self, name):
        for line in self.config_block:
            if isinstance(line, Server):
                if line.name == name:
                    return line

    def add_server(self, server):
        self.__add_node(server, Server)

    def remove_server(self, name):
        server = self.server(name)
        if server:
            self.config_block.remove(server)

    def binds(self):
        return self.__find_configs(Bind)

    def bind(self, host, port):
        for line in self.config_block:
            if isinstance(line, Bind):
                if line.host == host and line.port == port:
                    return line

    def add_bind(self, bind):
        self.__add_node(bind, Bind)

    def remove_bind(self, host, port):
        bind = self.bind(host, port)
        if bind:
            self.config_block.remove(bind)

    def acls(self):
        return self.__find_configs(Acl)

    def acl(self, name):
        for line in self.config_block:
            if isinstance(line, Acl):
                if line.name == name:
                    return line

    def add_acl(self, acl):
        self.__add_node(acl, Acl)

    def remove_acl(self, name):
        acl = self.acl(name)
        if acl:
            self.config_block.remove(acl)

    def users(self):
        return self.__find_configs(User)

    def user(self, name):
        for line in self.config_block:
            if isinstance(line, User):
                if line.name == name:
                    return line

    def add_user(self, user):
        self.__add_node(user, User)

    def remove_user(self, name):
        user = self.user(name)
        if user:
            self.config_block.remove(user)

    def groups(self):
        return self.__find_configs(Group)

    def group(self, name):
        for line in self.config_block:
            if isinstance(line, Group):
                if line.name == name:
                    return line

    def add_group(self, group):
        self.__add_node(group, Group)

    def remove_group(self, name):
        group = self.group(name)
        if group:
            self.config_block.remove(group)

    def usebackends(self):
        return self.__find_configs(UseBackend)

    def usebackend(self, name):
        for line in self.config_block:
            if isinstance(line, UseBackend):
                if line.backend_name == name:
                    return line

    def add_usebackend(self, usebackend):
        self.__add_node(usebackend, UseBackend)

    def remove_usebackend(self, name):
        usebackend = self.usebackend(name)
        if usebackend:
            self.config_block.remove(usebackend)


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


class Config(object):
    """Represents the `config` line in config block

    Attributes:
        keyword (srt):
        value (str):
    """
    def __init__(self, keyword, value):
        self.keyword = keyword
        self.value = value

    def __str__(self):
        return '<config_line: config %s %s>' % (
            self.keyword, self.value)


class Option(object):
    """Represents the `option` line in config block

    Attributes:
        keyword (srt):
        value (str):
    """
    def __init__(self, keyword, value):
        self.keyword = keyword
        self.value = value

    def __str__(self):
        return '<option_line: option %s %s>' % (
            self.keyword, self.value)


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
