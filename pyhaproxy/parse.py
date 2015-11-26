#!/bin/env python
# -*- coding: utf8 -*-

import os

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
        configs, options, _ = self.build_config_block(
            global_node.config_block, with_server=False)
        return config.Global(configs, options)

    def build_config_block(self, config_block_node, with_server=True):
        """parse `config_block` in each section

        Args:
            config_block_node (TreeNode): Description
            with_server (bool): determines if to parse server_lines

        Returns:
            (list, list, list):
                the <configs, options, servers> in `config_block`
        """
        configs, options, servers = [], [], []
        for line_node in config_block_node:
            if isinstance(line_node, pegnode.ConfigLine):
                configs.append(
                    dict([(line_node.keyword.text, line_node.value.text)]))
            elif isinstance(line_node, pegnode.OptionLine):
                options.append(
                    dict([(line_node.keyword.text, line_node.value.text)]))
            elif isinstance(line_node, pegnode.ServerLine) and with_server:
                servers.append(self.build_server(line_node))
        return configs, options, servers

    def build_server(self, server_node):
        pass

    def build_defaults(self, defaults_node):
        """parse `defaults` sections, and return a config.Defaults"""
        pass

    def build_userlist(self, userlist_node):
        """parse `userlist` sections, and return a config.Userlist"""
        pass

    def build_listen(self, listen_node):
        """parse `listen` sections, and return a config.Listen"""
        pass

    '''
    class Frontend(HasServer):
        def __init__(self, name, host, port, options, configs):
            super(Frontend, self).__init__()
            self.name = name
            self.host = host
            self.port = port
            self.options = options
            self.configs = configs
    '''

    def build_frontend(self, frontend_node):
        """parse `frontend` sections, and return a config.Frontend"""
        proxy_name = frontend_node.frontend_header.proxy_name
        service_address = frontend_node.frontend_header.service_address
        # parse the config block
        options, configs, _ = self.build_config_block(
            frontend_node.config_block, with_server=False)

        return config.FrontendSection(
            proxy_name, service_address.host,
            service_address.port, options, configs)

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


if __name__ == '__main__':
    parser = Parser('haproxy.cfg')
    configration = parser.build_configration()
    print configration.globall.configs, '----', configration.globall.options
