#!/bin/env python
# -*- coding: utf8 -*-

import config


if __name__ == '__main__':
    cfg_str = ''
    with open("haproxy.cfg") as f:
        for line in f:
            cfg_str = cfg_str + line

    tree = config.parse(cfg_str)
    for ele in tree.elements:
        print type(ele)
        print ele.offset, ele.text
