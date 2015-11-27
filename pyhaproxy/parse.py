#!/bin/env python
# -*- coding: utf8 -*-

import os
from collections import defaultdict

import pegnode
import config


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

    def build_configration(self):
        """Parse the haproxy config file

        Raises:
            Exception: when there are unsupported section

        Returns:
            config.Configration: haproxy config object
        """
        self.pegtree = pegnode.parse(self.filestring)
        configration = config.Configration(self.pegtree)
        for section_node in self.pegtree:
            if isinstance(section_node, pegnode.GlobalSection):
                configration.globall = self.build_global(section_node)
            elif isinstance(section_node, pegnode.FrontendSection):
                configration.frontends.append(
                    self.build_frontend(section_node))
            elif isinstance(section_node, pegnode.DefaultsSection):
                configration.defaults.append(
                    self.build_defaults(section_node))
            elif isinstance(section_node, pegnode.ListenSection):
                configration.listens.append(
                    self.build_listen(section_node))
            elif isinstance(section_node, pegnode.UserlistSection):
                configration.userlists.append(
                    self.build_userlist(section_node))
            elif isinstance(section_node, pegnode.BackendSection):
                configration.backends.append(
                    self.build_backend(section_node))
            else:
                raise Exception('Unsupported section')
        return configration

    def build_global(self, global_node):

        """parse `global` section, and return the config.Global

        Args:
            global_node (TreeNode):  `global` section treenode

        Returns:
            config.Global: an object
        """
        config_block_dict = self.build_config_block(
            global_node.config_block)
        return config.Global(config_block=config_block_dict)

    def build_config_block(self, config_block_node):
        """parse `config_block` in each section

        Args:
            config_block_node (TreeNode): Description

        Returns:
            {'configs': list(dict),
              'options': list(dict),
              'servers': list(dict),
              'binds': list(config.Bind),
              'acls': list(config.Acl),
              'usebackends': list(config.UseBackend)
            }:
                the <configs, options, servers> in `config_block`
        """
        config_block_dict = defaultdict(list)

        for line_node in config_block_node:
            if isinstance(line_node, pegnode.ConfigLine):
                config_block_dict['configs'].append(
                    dict([(line_node.keyword.text, line_node.value.text)]))
            elif isinstance(line_node, pegnode.OptionLine):
                config_block_dict['options'].append(
                    dict([(line_node.keyword.text, line_node.value.text)]))
            elif isinstance(line_node, pegnode.ServerLine):
                config_block_dict['servers'].append(
                    self.build_server(line_node))
            elif isinstance(line_node, pegnode.BindLine):
                config_block_dict['binds'].append(
                    self.build_bind(line_node))
            elif isinstance(line_node, pegnode.AclLine):
                config_block_dict['acls'].append(
                    self.build_acl(line_node))
            elif isinstance(line_node, pegnode.BackendLine):
                config_block_dict['usebackends'].append(
                    self.build_usebackend(line_node))
            else:
                # may blank_line, comment_line
                pass
        return config_block_dict

    def build_server(self, server_node):
        server_name = server_node.server_name.text
        host = server_node.service_address.host.text
        port = server_node.service_address.port.text

        # parse server attributes, value is similar to \
        # 'maxconn 1024 weight 3 check inter 2000 rise 2 fall 3'
        server_attributes = server_node.value.text.split(' \t')
        return config.Server(
            name=server_name, host=host, port=port,
            attributes=server_attributes)

    def build_bind(self, bind_node):
        service_address = bind_node.service_address
        return config.Bind(
            host=service_address.host.text,
            port=service_address.port.text,
            attributes=bind_node.value.text.split(' \t'))

    def build_acl(self, acl_node):
        acl_name = acl_node.acl_name.text
        acl_value = acl_node.value.text
        return config.Acl(name=acl_name, value=acl_value)

    def build_usebackend(self, usebackend_node):
        operator = usebackend_node.operator.text
        backendtype = usebackend_node.backendtype.text

        return config.UseBackend(
            backend_name=usebackend_node.backend_name.text,
            operator=operator,
            backend_condition=usebackend_node.backend_condition.text,
            is_default=(backendtype == 'default_backend'))

    def build_defaults(self, defaults_node):
        """parse `defaults` sections, and return a config.Defaults

        Args:
            defaults_node (TreeNode): Description

        Returns:
            config.Defaults: an object
        """
        proxy_name = defaults_node.defaults_header.proxy_name.text
        config_block_dict = self.build_config_block(
            defaults_node.config_block)
        return config.Defaults(name=proxy_name, config_block=config_block_dict)

    def build_userlist(self, userlist_node):
        """parse `userlist` sections, and return a config.Userlist"""
        pass

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
        config_block_dict = self.build_config_block(listen_node.config_block)

        # parse host and port
        host, port = '', ''
        if isinstance(service_address_node, pegnode.ServiceAddress):
            host = service_address_node.host.text
            port = service_address_node.port.text
        else:
            # use `bind` in config lines to fill in host and port
            # just use the first
            for bind in config_block_dict['binds']:
                host, port = bind.host, bind.port
                break
            else:
                raise Exception(
                    'Not specify host and port in `listen` definition')
        return config.Listen(
            name=proxy_name, host=host, port=port,
            config_block=config_block_dict)

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
        config_block_dict = self.build_config_block(
            frontend_node.config_block)

        # parse host and port
        host, port = '', ''
        if isinstance(service_address_node, pegnode.ServiceAddress):
            host = service_address_node.host.text
            port = service_address_node.port.text
        else:
            # use `bind` in config lines to fill in host and port
            # just use the first
            for bind in config_block_dict['binds']:
                host, port = bind.host, bind.port
                break
            else:
                raise Exception(
                    'Not specify host and port in `frontend` definition')
        return config.Frontend(
            name=proxy_name, host=host, port=port,
            config_block=config_block_dict)

    def build_backend(self, backend_node):
        """parse `backend` sections

        Args:
            backend_node (TreeNode): Description

        Returns:
            config.Backend: an object
        """
        proxy_name = backend_node.backend_header.proxy_name.text
        config_block_dict = self.build_config_block(backend_node.config_block)
        return config.Backend(name=proxy_name, config_block=config_block_dict)

    def __read_string_from_file(self, filepath):
        filestring = ''
        if os.path.exists(filepath):
            with open(filepath) as f:
                for line in f:
                    filestring = filestring + line
        return filestring
