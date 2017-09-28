#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyhaproxy.config as config


class Render(object):
    """Do rendering the config.Config object to a str

    Attributes:
        configuration (config.Configuration):
    """
    def __init__(self, configuration):
        self.configuration = configuration

    def render_configuration(self):
        config_str = ''
        # render global section
        if self.configuration.globall:
            config_str = self.render_global(self.configuration.globall)
        # render defaults sections
        for defaults_section in self.configuration.defaults:
            config_str = config_str + self.render_defaults(defaults_section)
        # render userlists sections
        for userlist_section in self.configuration.userlists:
            config_str = config_str + self.render_userlist(userlist_section)
        # render listen sections
        for listen_section in self.configuration.listens:
            config_str = config_str + self.render_listen(listen_section)
        # render frontend sections
        for frontend_section in self.configuration.frontends:
            config_str = config_str + self.render_frontend(frontend_section)
        # render backend sections
        for backend_section in self.configuration.backends:
            config_str = config_str + self.render_backend(backend_section)

        return config_str

    def dumps_to(self, filepath):
        with open(filepath, 'w') as f:
            f.write(self.render_configuration())

    def render_global(self, globall):
        globall_str = '''
global
%s
'''
        return globall_str % self.__render_config_block(
            globall.config_block)

    def render_defaults(self, defaults):
        defaults_str = '''
defaults %s
%s
'''
        return defaults_str % (defaults.name, self.__render_config_block(
            defaults.config_block))

    def render_userlist(self, userlist):
        userlist_str = '''
userlist %s
%s
'''

        return userlist_str % (
            userlist.name,
            self.__render_config_block(userlist.config_block))

    def render_listen(self, listen):
        listen_str = '''
listen %s %s
%s
'''
        host_port = ''
        if not len(listen.binds()):
            host_port = '%s:%s' % (listen.host, listen.port)

        return listen_str % (
            listen.name, host_port,
            self.__render_config_block(listen.config_block))

    def render_frontend(self, frontend):
        frontend_str = '''
frontend %s %s
%s
'''
        host_port = ''
        if not len(frontend.binds()):
            host_port = '%s:%s' % (frontend.host, frontend.port)

        return frontend_str % (
            frontend.name, host_port,
            self.__render_config_block(frontend.config_block))

    def render_backend(self, backend):
        backend_str = '''
backend %s
%s
'''
        return backend_str % (backend.name, self.__render_config_block(
            backend.config_block))

    def __render_config_block(self, config_block):
        """Summary

        Args:
            config_block [config.Item, ...]: config lines

        Returns:
            str: config block str
        """
        config_block_str = ''
        for line in config_block:
            if isinstance(line, config.Option):
                line_str = self.__render_option(line)
            elif isinstance(line, config.Config):
                line_str = self.__render_config(line)
            elif isinstance(line, config.Server):
                line_str = self.__render_server(line)
            elif isinstance(line, config.Bind):
                line_str = self.__render_bind(line)
            elif isinstance(line, config.Acl):
                line_str = self.__render_acl(line)
            elif isinstance(line, config.UseBackend):
                line_str = self.__render_usebackend(line)
            elif isinstance(line, config.User):
                line_str = self.__render_user(line)
            elif isinstance(line, config.Group):
                line_str = self.__render_group(line)
            # append line str
            config_block_str = config_block_str + line_str

        return config_block_str

    def __render_usebackend(self, usebackend):
        usebackend_line = '    %s %s %s %s\n'
        backendtype = 'use_backend'
        if usebackend.is_default:
            backendtype = 'default_backend'

        return usebackend_line % (
            backendtype, usebackend.backend_name,
            usebackend.operator, usebackend.backend_condition)

    def __render_user(self, user):
        user_line = '    user %s %s %s %s\n'
        group_fragment = ''
        if user.group_names:
            group_fragment = 'groups ' + ','.join(user.group_names)
        return user_line % (
            user.name, user.passwd_type, user.passwd, group_fragment)

    def __render_group(self, group):
        group_line = '    group %s %s\n'
        user_fragment = ''
        if group.user_names:
            user_fragment = 'users ' + ','.join(group.user_names)
        return group_line % (group.name, user_fragment)

    def __render_server(self, server):
        server_line = '    server %s %s:%s %s\n'
        return server_line % (
            server.name, server.host, server.port, ' '.join(server.attributes))

    def __render_acl(self, acl):
        acl_line = '    acl %s %s\n'
        return acl_line % (acl.name, acl.value)

    def __render_bind(self, bind):
        bind_line = '    bind %s:%s %s\n'
        return bind_line % (
            bind.host, bind.port, ' '.join(bind.attributes))

    def __render_option(self, option):
        option_line = '    option %s %s\n'
        return option_line % (option.keyword, option.value)

    def __render_config(self, config):
        config_line = '    %s %s\n'
        return config_line % (config.keyword, config.value)
