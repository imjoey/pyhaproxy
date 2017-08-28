# Pyhaproxy ![PyPi](https://img.shields.io/pypi/v/pyhaproxy.svg)   ![Build Status](https://travis-ci.org/imjoey/pyhaproxy.svg?branch=master)
It's a Python library to parse haproxy config file. Thanks to [canopy](https://github.com/jcoglan/canopy), which I use for auto-generating Python codes by PEG grammar. But the 'Extension methods for node' feature in canopy seems broken, I always encounter the MRO errors when running `parse` function. So I modify the generated codes which mainly rename the `TreeNode*` to specified treenode name, eg: GlobalSection, GlobalHeader, BackendHeader, and also complement missing attributes.


# Install
This project uses nose for unit testing, but with no more Python libraries dependencies for running.

* Suppose that you have virtualenv installed, if not, please go [here](https://virtualenv.readthedocs.org/en/latest/installation.html) to install
* Create a virutalenv and activate it,
```bash
$ virtualenv --no-site-packages pyhaproxy
$ source pyhaproxy/bin/activate
```
* User pip (`pip install pyhaproxy`) or setuptools (`easy_install pyhaproxy`) to install it
* Install nose dependency for unittest
```bash
(pyhaproxy)$ pip install -r requirements.txt
```


# Example
Here is the simple example to show how to use it. See unittest file [test.py](https://github.com/imjoey/pyhaproxy/blob/master/pyhaproxy/test.py) for more usage details.

```python
#!/usr/bin/env python
# -*- coding: utf8 -*-

from pyhaproxy.parse import Parser
from pyhaproxy.render import Render
import pyhaproxy.config as config


# Build the configuration instance by calling Parser('config_file').build_configuration()
cfg_parser = Parser('haproxy.cfg')
configuration = cfg_parser.build_configuration()

# Get the global section
print configuration.globall  # the `global` is keyword of Python, so name it `globall`
print configuration.globall.options()  # get the 'option ...' config lines
print configuration.globall.configs()  # get config lines except 'option ...' ones


# Get all the frontend sections
frontend_sections = configuration.frontends

# Get frontend sections specifics
for fe_section in frontend_sections:
    # Get the name, host, port of the frontend section
    print fe_section.name, fe_section.host, fe_section.port
    print fe_section.options()
    print fe_section.configs()


# Find the frontend by name
the_fe_section = configuration.frontend(the_fe_section_name)

'''To get other sections is ditto.
'''


# Operates the ACL in a frontend, it much likes operating a list

#   Get all the ACLs defined in the frontend section
acls = the_fe_section.acls()   # return list(config.Acl)

#   Find the specified ACL
acl_instance = the_fe_section.acl(the_acl_name)   # return config.Acl

#   Modify existing ACL
acl_instance.value = 'hdr(host) -i modified.example.com'

#   Append the ACL into the frontend section
#       for version <= 0.2.4
the_fe_section.acls().append(config.Acl(acl_name, acl_value))
#       for version > 0.2.4
the_fe_section.add_acl(config.Acl(acl_name, acl_value))        

#   Remove ACL
#       for version <= 0.2.4
acl_instance = the_fe_section.acl(the_acl_name)
the_fe_section.acls().remove(acl_instance)
#       for version > 0.2.4
the_fe_section.remove_acl(the_acl_name)           


# Operates the use_backend / default_backend configs in a frontend

#   Get all the backend configs
usebackends = the_fe_section.usebackends()  # return list(config.UseBackend)
for usebe in usebackends:
    # Get the using backend name, operator, condition
    print usebe.backend_name, usebe.operator, usebe.backend_condition
    # Determine if it's `default_backend` line
    print usebe.is_default
#   Add a new `use_backend` or `default_backend` line
#       for version <= 0.2.4
the_fe_section.usebackends().append(config.UseBackend(backend_name, operator, backend_condition, is_default))
#       for version > 0.2.4
the_fe_section.add_usebackend(config.UseBackend(backend_name, operator, backend_condition, is_default))


# Operates the Server in a backend
the_be_section = configuration.backend(the_be_section_name)
#   Get all the Server lines in backend section
servers = the_be_section.servers()  # return list(config.Server)
#   Find the specified Server
the_server = the_be_section.server(the_server_name)  # return config.Server
#   Get the Server name, host, port
print the_server.name, the_server.host, the_server.port
#   Get the Server attributes, for line: `server web_server_1 10.1.1.2:80 cookie 1 check inter 2000 rise 3`
print the_server.attributes  # it's is ['cookie', 1, 'check', 'inter', 2000, 'rise', 3]
#   Remove the Server by name
#       for version <= 0.2.4
the_be_section.servers().remove(the_server)
#       for version > 0.2.4
the_be_section.remove_server(server_name)


# Render out to the cfg file
cfg_render = Render(configuration)
cfg_render.dumps_to('./hatest.cfg')  # you will see hatest.cfg which is same to the `haproxy.cfg` parsed previously

```


# Finished
- [x] Parse `global` section
- [x] Parse `frontend` sections
- [x] Parse `bind` config lines
- [x] Parse `backend` sections
- [x] Parse `defaults` sections
- [x] Parse `userlist` sections
- [x] Parse `listen` sections
- [x] Parse `acl` config lines
- [x] Parse `use_backend` and `default_backend` config lines
- [x] Render `global` section
- [x] Render `frontend` section
- [x] Render `backend` sections
- [x] Render `defaults` sections
- [x] Render `userlist` sections
- [x] Render `listen` sections


# TODO
- [ ] Link `backend` with `frontend` by `acl`


# Unittest
Use nose unit test framework
```bash
(pyhaproxy)$ nosetests -sv test.py
```


# Thanks
* Inspired by @subakva 's [haproxy-tools](https://github.com/subakva/haproxy-tools)
* Use [canopy](https://github.com/jcoglan/canopy) of @jcoglan for PEG parsing and Python code auto-generating
