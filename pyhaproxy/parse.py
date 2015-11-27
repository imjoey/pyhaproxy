#!/bin/env python
# -*- coding: utf8 -*-

import os
import re
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
            global_node.config_block, with_server=False)
        return config.Global(
            config_block_dict['configs'], config_block_dict['options'])

    def build_config_block(self, config_block_node, with_server=True):
        """parse `config_block` in each section

        Args:
            config_block_node (TreeNode): Description
            with_server (bool): determines if to parse server_lines

        Returns:
            ({'configs': list(dict),
              'options': list(dict),
              'servers': list(dict)}
            ):
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
            elif isinstance(line_node, pegnode.ServerLine) and with_server:
                config_block_dict['servers'].append(
                    self.build_server(line_node))
        return config_block_dict

    def build_server(self, server_node):
        server_name = server_node.proxy_name.text
        host = server_node.service_address.host.text
        port = server_node.service_address.port.text

        # parse server attributes, value is similar to \
        # 'maxconn 1024 weight 3 check inter 2000 rise 2 fall 3'
        server_attributes = server_node.value.text.split(' \t')
        return config.Server(server_name, host, port, server_attributes)

    def build_defaults(self, defaults_node):
        """parse `defaults` sections, and return a config.Defaults"""
        name = defaults_node.defaults_header.proxy_name.text
        config_block_dict = self.build_config_block(defaults_node.config_block)
        return config.Defaults(
            name, config_block_dict['options'], config_block_dict['configs'])

    def build_userlist(self, userlist_node):
        """parse `userlist` sections, and return a config.Userlist"""
        pass

    def build_listen(self, listen_node):
        """parse `listen` sections, and return a config.Listen"""
        pass

    def build_frontend(self, frontend_node):
        """parse `frontend` sections, and return a config.Frontend"""
        proxy_name = frontend_node.frontend_header.proxy_name.text
        service_address = frontend_node.frontend_header.service_address

        # parse the config block
        config_block_dict = self.build_config_block(
            frontend_node.config_block, with_server=False)

        # parse host and port
        host, port = '', ''
        if isinstance(service_address, pegnode.ServiceAddress):
            host, port = service_address.host.text, service_address.port.text
        else:
            bind = self.build_bind(frontend_node.config_block)
            if bind:
                host, port = bind.host, bind.port
            else:
                raise Exception(
                    'Not specify host and port in `frontend` definition')
        return config.Frontend(
            proxy_name, host, port,
            config_block_dict['options'], config_block_dict['configs'])

    def build_bind(self, config_block):
        bind_re_str = r'[ \t]*bind[ \t]+(?P<host>[a-zA-Z0-9\.]*)[:]*(?P<port>[\d]*)[ \t]+(?P<attributes>[^#\n]*)'
        bind_pattern = re.compile(bind_re_str)
        for ele in config_block:
            match_group = bind_pattern.match(ele.text)
            if match_group:
                attributes = match_group.group('attributes').split(' \t')
                host = match_group.group('host')
                port = match_group.group('port')
                return config.Bind(host, port, attributes)

    def build_backend(self, backend_node):
        """parse `backend` sections, and return a config.Backend"""
        pass

    def __read_string_from_file(self, filepath):
        filestring = ''
        if os.path.exists(filepath):
            with open(filepath) as f:
                for line in f:
                    filestring = filestring + line
        return filestring
