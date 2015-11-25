# Pyhaproxy
This is a Python library to parse haproxy config file. Thanks to [canopy](https://github.com/jcoglan/canopy), I use it for auto-generating python codes by PEG grammar. But the 'Extension methods for node' in canopy seems broken, I alwayls encounter the MRO errors when running `parse` function. So I modify the generated codes which mainly rename the `TreeNode*` to specified treenode name, eg: GlobalSection, GlobalHeader, BackendHeader, and so on.

# Install
This project has no other libraries dependency. Just clone the code is enough.

# Run
To implemented.

# Thanks
* Inspired by @subakva 's [haproxy-tools](https://github.com/subakva/haproxy-tools)
* Use [canopy](https://github.com/jcoglan/canopy) for PEG parsing and Python code auto-generating