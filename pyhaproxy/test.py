#!/usr/bin/env python
# -*- coding: utf-8 -*-

import parse


class TestParse(object):

    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        pass

    def setup(self):
        self.parser = parse.Parser('haproxy.cfg')
        self.configration = self.parser.build_configration()

    def teardown(self):
        pass

    def test_parse_global_section(self):
        print self.configration.globall.configs
        print '-' * 30
        print self.configration.globall.options

    def test_parse_frontend_section(self):
        for frontend in self.configration.frontends:
            print frontend.name, frontend.host, frontend.port
            print frontend.configs
            print frontend.options
            print '-' * 30

    def test_parse_defaults_section(self):
        for defaults in self.configration.defaults:
            print defaults.name
            print defaults.options
            print defaults.configs

    def test_parse_listen_section(self):
        for listen in self.configration.listens:
            print listen.name, listen.host, listen.port
            print listen.options
            print listen.configs

    def test_parse_backend_section(self):
        for backend in self.configration.backends:
            print backend.name
            print backend.options
            print backend.configs
