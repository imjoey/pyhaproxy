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

# Run
Use nose unit testing to run the code
* Run unittest
```bash
(pyhaproxy)$ nosetests test.py
```


# Thanks
* Inspired by @subakva 's [haproxy-tools](https://github.com/subakva/haproxy-tools)
* Use [canopy](https://github.com/jcoglan/canopy) of @jcoglan for PEG parsing and Python code auto-generating
