# Pyhaproxy
It's a Python library to parse haproxy config file. Thanks to [canopy](https://github.com/jcoglan/canopy), which I use for auto-generating Python codes by PEG grammar. But the 'Extension methods for node' feature in canopy seems broken, I always encounter the MRO errors when running `parse` function. So I modify the generated codes which mainly rename the `TreeNode*` to specified treenode name, eg: GlobalSection, GlobalHeader, BackendHeader, and so on.

# Install
This project uses nose for unit testing, but with no more Python libraries dependencies for running.
* Suppose that you have virtualenv installed, if not, please go [here](https://virtualenv.readthedocs.org/en/latest/installation.html) to install
* Create a virutalenv and activate it,
```bash
$ virtualenv --no-site-packages pyhaproxy
$ source pyhaproxy/bin/activate
```
* Clone code
* Install dependencies
```bash
(pyhaproxy)$ pip install -r requirements.txt
```

# Example
Here is the simple example to show how to use it.
```python
#!/bin/env python
# -*- coding: utf8 -*-

import config
import parse

parser = parse.Parser('haproxy.cfg')
configration = parser.build_configration()

# print global section
print configration.globall
print configration.globall.configs
print configration.globall.options

# print frontend sections
for frontend in configration.frontends:
    print frontend.name, frontend.host, frontend.port
    print frontend.configs
    print frontend.options
    print '-' * 30

```

# TODO
- [x] ~~Parse `global` section~~
- [x] ~~Parse `frontend` sections~~
- [x] ~~Parse `bind` config lines~~
- [x] ~~Parse `backend` sections~~
- [x] ~~Parse `defaults` sections~~
- [ ] Parse `userlist` sections
- [x] ~~Parse `listen` sections~~
- [x] Parse `acl` config lines
- [x] Parse `use_backend` and `default_backend` config lines
- [ ] Link `backend` with `frontend` by `acl`
- [ ] Render `global` section
- [ ] Render `frontend` section
- [ ] Render `backend` sections
- [ ] Render `defaults` sections
- [ ] Render `userlist` sections
- [ ] Render `listen` sections

# Unittest
Use nose unit test framework
```bash
(pyhaproxy)$ nosetests -sv test.py
```


# Thanks
* Inspired by @subakva 's [haproxy-tools](https://github.com/subakva/haproxy-tools)
* Use [canopy](https://github.com/jcoglan/canopy) of @jcoglan for PEG parsing and Python code auto-generating
