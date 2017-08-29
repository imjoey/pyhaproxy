#!/usr/bin/env python
# -*- coding: utf8 -*-

import os

import pyhaproxy.pegnode as pegnode
import pyhaproxy.config as config


class Parser(object):
    """Do parsing the peg-tree and build the objects in config module

    Attributes:
        filepath (str): the absolute path of haproxy config file
        filestring (str): the content of haproxy config file
    """
    def __init__(self, filepath='/etc/haproxy/haproxy.cfg', filestring=None):
        if filestring:
            self.filestring = filestring
        elif filepath:
            self.filestring = self.__read_string_from_file(filepath)
        else:
            raise Exception('please validate your input')

    def build_configuration(self):
        """Parse the haproxy config file

        Raises:
            Exception: when there are unsupported section

        Returns:
            config.Configuration: haproxy config object
        """
        configuration = config.Configuration()
        pegtree = pegnode.parse(self.filestring)
        for section_node in pegtree:
            if isinstance(section_node, pegnode.GlobalSection):
                configuration.globall = self.build_global(section_node)
            elif isinstance(section_node, pegnode.FrontendSection):
                configuration.frontends.append(
                    self.build_frontend(section_node))
            elif isinstance(section_node, pegnode.DefaultsSection):
                configuration.defaults.append(
                    self.build_defaults(section_node))
            elif isinstance(section_node, pegnode.ListenSection):
                configuration.listens.append(
                    self.build_listen(section_node))
            elif isinstance(section_node, pegnode.UserlistSection):
                configuration.userlists.append(
                    self.build_userlist(section_node))
            elif isinstance(section_node, pegnode.BackendSection):
                configuration.backends.append(
                    self.build_backend(section_node))

        return configuration

    def build_global(self, global_node):

        """parse `global` section, and return the config.Global

        Args:
            global_node (TreeNode):  `global` section treenode

        Returns:
            config.Global: an object
        """
        config_block_lines = self.__build_config_block(
            global_node.config_block)
        return config.Global(config_block=config_block_lines)

    def __build_config_block(self, config_block_node):
        """parse `config_block` in each section

        Args:
            config_block_node (TreeNode): Description

        Returns:
            [line_node1, line_node2, ...]
        """
        node_lists = []

        for line_node in config_block_node:
            if isinstance(line_node, pegnode.ConfigLine):
                node_lists.append(self.__build_config(line_node))
            elif isinstance(line_node, pegnode.OptionLine):
                node_lists.append(self.__build_option(line_node))
            elif isinstance(line_node, pegnode.ServerLine):
                node_lists.append(
                    self.__build_server(line_node))
            elif isinstance(line_node, pegnode.BindLine):
                node_lists.append(
                    self.__build_bind(line_node))
            elif isinstance(line_node, pegnode.AclLine):
                node_lists.append(
                    self.__build_acl(line_node))
            elif isinstance(line_node, pegnode.BackendLine):
                node_lists.append(
                    self.__build_usebackend(line_node))
            elif isinstance(line_node, pegnode.UserLine):
                node_lists.append(
                    self.__build_user(line_node))
            elif isinstance(line_node, pegnode.GroupLine):
                node_lists.append(
                    self.__build_group(line_node))
            else:
                # may blank_line, comment_line
                pass
        return node_lists

    def build_defaults(self, defaults_node):
        """parse `defaults` sections, and return a config.Defaults

        Args:
            defaults_node (TreeNode): Description

        Returns:
            config.Defaults: an object
        """
        proxy_name = defaults_node.defaults_header.proxy_name.text
        config_block_lines = self.__build_config_block(
            defaults_node.config_block)
        return config.Defaults(
            name=proxy_name,
            config_block=config_block_lines)

    def build_userlist(self, userlist_node):
        """parse `userlist` sections, and return a config.Userlist"""
        proxy_name = userlist_node.userlist_header.proxy_name.text
        config_block_lines = self.__build_config_block(
            userlist_node.config_block)
        return config.Userlist(
            name=proxy_name,
            config_block=config_block_lines)

    def build_listen(self, listen_node):
        """parse `listen` sections, and return a config.Listen

        Args:
            listen_node (TreeNode): Description

        Returns:
            config.Listen: an object
        """
        proxy_name = listen_node.listen_header.proxy_name.text
        service_address_node = listen_node.listen_header.service_address

        # parse the config block
        config_block_lines = self.__build_config_block(
            listen_node.config_block)

        # parse host and port
        host, port = '', ''
        if isinstance(service_address_node, pegnode.ServiceAddress):
            host = service_address_node.host.text
            port = service_address_node.port.text
        else:
            # use `bind` in config lines to fill in host and port
            # just use the first
            for line in config_block_lines:
                if isinstance(line, config.Bind):
                    host, port = line.host, line.port
                    break
            else:
                raise Exception(
                    'Not specify host and port in `listen` definition')
        return config.Listen(
            name=proxy_name, host=host, port=port,
            config_block=config_block_lines)

    def build_frontend(self, frontend_node):
        """parse `frontend` sections, and return a config.Frontend

        Args:
            frontend_node (TreeNode): Description

        Raises:
            Exception: Description

        Returns:
            config.Frontend: an object
        """
        proxy_name = frontend_node.frontend_header.proxy_name.text
        service_address_node = frontend_node.frontend_header.service_address

        # parse the config block
        config_block_lines = self.__build_config_block(
            frontend_node.config_block)

        # parse host and port
        host, port = '', ''
        if isinstance(service_address_node, pegnode.ServiceAddress):
            host = service_address_node.host.text
            port = service_address_node.port.text
        else:
            # use `bind` in config lines to fill in host and port
            # just use the first
            for line in config_block_lines:
                if isinstance(line, config.Bind):
                    host, port = line.host, line.port
                    break
            else:
                raise Exception(
                    'Not specify host and port in `frontend` definition')
        return config.Frontend(
            name=proxy_name, host=host, port=port,
            config_block=config_block_lines)

    def build_backend(self, backend_node):
        """parse `backend` sections

        Args:
            backend_node (TreeNode): Description

        Returns:
            config.Backend: an object
        """
        proxy_name = backend_node.backend_header.proxy_name.text
        config_block_lines = self.__build_config_block(
            backend_node.config_block)
        return config.Backend(name=proxy_name, config_block=config_block_lines)

    def __build_server(self, server_node):
        server_name = server_node.server_name.text
        host = server_node.service_address.host.text
        port = server_node.service_address.port.text

        # parse server attributes, value is similar to \
        # 'maxconn 1024 weight 3 check inter 2000 rise 2 fall 3'
        server_attributes = server_node.value.text.split(' \t')
        return config.Server(
            name=server_name, host=host, port=port,
            attributes=server_attributes)

    def __build_config(self, config_node):
        return config.Config(keyword=config_node.keyword.text,
                             value=config_node.value.text)

    def __build_option(self, option_node):
        return config.Option(keyword=option_node.keyword.text,
                             value=option_node.value.text)

    def __build_bind(self, bind_node):
        service_address = bind_node.service_address
        return config.Bind(
            host=service_address.host.text,
            port=service_address.port.text,
            attributes=bind_node.value.text.split(' \t'))

    def __build_acl(self, acl_node):
        acl_name = acl_node.acl_name.text
        acl_value = acl_node.value.text
        return config.Acl(name=acl_name, value=acl_value)

    def __build_usebackend(self, usebackend_node):
        operator = usebackend_node.operator.text
        backendtype = usebackend_node.backendtype.text

        return config.UseBackend(
            backend_name=usebackend_node.backend_name.text,
            operator=operator,
            backend_condition=usebackend_node.backend_condition.text,
            is_default=(backendtype == 'default_backend'))

    def __build_user(self, user_node):
        groups_fragment = user_node.groups_fragment.text
        group_names = groups_fragment.split(',') if groups_fragment else []
        return config.User(
            name=user_node.user_name.text,
            passwd=user_node.password.text,
            passwd_type=user_node.passwd_type.text,
            group_names=group_names)

    def __build_group(self, group_node):
        users_fragment = group_node.users_fragment.text
        user_names = users_fragment.split(',') if users_fragment else []
        return config.Group(
            name=group_node.group_name.text,
            user_names=user_names)

    def __read_string_from_file(self, filepath):
        filestring = ''
        if os.path.exists(filepath):
            with open(filepath) as f:
                filestring = f.read()
        return filestring
