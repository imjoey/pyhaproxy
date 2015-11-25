#!/bin/env python
# -*- coding: utf8 -*-

import haproxy
import node_types


if __name__ == '__main__':
    cfg_str = ''
    with open("haproxy.cfg") as f:
        for line in f:
            cfg_str = cfg_str + line

    tree = haproxy.parse(cfg_str, types=node_types)

    print tree
