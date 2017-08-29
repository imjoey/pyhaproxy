#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyhaproxy.parse as parse
import pyhaproxy.render as render
import pyhaproxy.config as config


class TestParse(object):

    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        pass

    def setup(self):
        filestring = r"""
global
      maxconn     4096
      nbproc      1
      debug
      daemon
      log         127.0.0.1   local0

defaults
      mode        http
      option      httplog
      log         global

userlist L1
      group G1 users tiger,scott
      group G2 users xdb,sc

      user tiger password $6$k6y3o.eP$JlKBx9za9667qe4(...)xHSwRv6J.C0/D7cV91
      user scott insecure-password elgato
      user xdb insecure-password hello

userlist L2
      group G1
      group G2

      user tiger password $6$k6y3o.eP$JlKBx(...)xHSwRv6J.C0/D7cV91 groups G1
      user scott insecure-password elgato groups G1,G2
      user xdb insecure-password hello groups G2

frontend unsecured *:80
      timeout     client      86400000
      mode        http
      option      httpclose
      option      forwardfor  #forward’s clients IP to app
      bind-process odd
     #catch all domains that begin with 'www.'
      acl host_www1      hdr_beg(host) -i www.
      reqirep ^Host:\ www.(.*)$ Host:\ \1 if host_www
      redirect code 301 prefix / if host_www

     # Define hosts
      acl host_niftykick hdr(host) -i niftykick.com
      acl host_chatleap hdr(host) -i chatleap.com
      acl host_trevordev hdr(host) -i trevordev.com
      acl host_jokeydoke hdr(host) -i jokeydoke.com
      acl host_swiftnifty hdr(host) -i swiftnifty.trevordev.com

     #redirect to https
      redirect    prefix https://niftykick.com code 301 if host_niftykick

     ## figure out which one to use
      use_backend niftykick if host_niftykick
      use_backend chatleap if host_chatleap
      use_backend trevordev if host_trevordev
      use_backend swiftnifty if host_swiftnifty
      use_backend jokeydoke if host_jokeydoke

     default_backend         devbrick

frontend  secured
      timeout     client 86400000
      mode        http
      option      httpclose
      option      forwardfor

     #catch all domains that begin with 'www.'
      acl host_www2      hdr_beg(host) -i www.
      reqirep ^Host:\ www.(.*)$ Host:\ \1 if host_www
      redirect code 301 prefix / if host_www

     acl host_coyote path_beg /fileServer/
      acl host_niftykick hdr(host) -i niftykick.com

     bind        0.0.0.0:443 ssl crt /etc/haproxy/niftykickCert.pem

     use_backend fileServer if host_coyote
     use_backend niftykick if host_niftykick

backend devbrick
      mode        http
      option      forwardfor  #this sets X-Forwarded-For
      timeout     server      30000
      timeout     connect     4000
      server      server1     localhost:3000 weight 1 maxconn 1024 check

backend chatleap
      mode        http
      option      forwardfor  #this sets X-Forwarded-For
      timeout     server      30000
      timeout     connect     4000
      server      server1     localhost:3001 weight 1 maxconn 1024 check

backend jokeydoke
      mode        http
      option      forwardfor  #this sets X-Forwarded-For
      timeout     server      30000
      timeout     connect     4000
      server      server1     localhost:3002 weight 1 maxconn 1024 check

backend trevordev
      mode        http
      option      forwardfor  #this sets X-Forwarded-For
      timeout     server      30000
      timeout     connect     4000
      server      server1     localhost:3003 weight 1 maxconn 1024 check

backend niftykick
      mode        http
      option      forwardfor  #this sets X-Forwarded-For
      timeout     server      30000
      timeout     connect     4000
      server      server1     localhost:3005 weight 1 maxconn 1024 check

backend fileServer
      mode        http
      option      forwardfor  #this sets X-Forwarded-For
      timeout     server      30000
      timeout     connect     4000
      reqrep ^([^\ :]*)\ /fileServer/(.*)     \1\ /\2
      server      server1     localhost:3008 weight 1 maxconn 1024 check

backend swiftnifty
      mode        http
      option      forwardfor  #this sets X-Forwarded-For
      timeout     server      30000
      timeout     connect     4000
      server      server1     localhost:3007 weight 1 maxconn 1024 check

"""
        self.parser = parse.Parser(filestring=filestring)
        self.configration = self.parser.build_configuration()

    def teardown(self):
        pass

    def test_parse_global_section(self):
        print self.configration
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

    def test_update_config_block(self):
        backend = self.configration.backend('chatleap')
        new_server = config.Server('newly1', '8.8.8.8', 1234)
        backend.add_server(new_server)
        server1 = backend.server('server1')
        server1.name = 'server2'
        backend.add_config(config.Config('conf_key_1', 'conf_key_2'))
        self.render = render.Render(self.configration)
        self.render.dumps_to('./hatest.cfg')
