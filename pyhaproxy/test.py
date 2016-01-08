#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyhaproxy.parse as parse
import pyhaproxy.render as render


class TestParse(object):

    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        pass

    def setup(self):
        self.parser = parse.Parser('haproxy.cfg')
        self.configration = self.parser.build_configuration()

    def teardown(self):
        pass

    def test_parse_global_section(self):
        print self.configration.globall.configs()
        print '-' * 30
        print self.configration.globall.options()

    def test_parse_frontend_section(self):
        for frontend in self.configration.frontends:
            print '-' * 15
            print frontend.name, frontend.host, frontend.port
            for acl in frontend.acls():
                print acl

    def test_parse_defaults_section(self):
        for defaults in self.configration.defaults:
            print defaults.name
            print defaults.options()
            print defaults.configs()

    def test_parse_listen_section(self):
        for listen in self.configration.listens:
            print listen.name, listen.host, listen.port
            print listen.options()
            print listen.configs()

    def test_parse_backend_section(self):
        for backend in self.configration.backends:
            print backend.name
            print backend.options()
            print backend.configs()

    def test_parse_userlist_section(self):
        for userlist in self.configration.userlists:
            print userlist.name
            print 'groups:\n'
            for group in userlist.groups():
                print group.name
                print group.user_names
            print 'users:\n'
            for user in userlist.users():
                print user.name, '-', user.passwd, '-', user.passwd_type
                print user.group_names

    def test_render(self):
        self.render = render.Render(self.configration)
        self.render.dumps_to(
            './hatest.cfg')
        parser = parse.Parser('haproxy.cfg')
        configration = parser.build_configuration()
        print configration
