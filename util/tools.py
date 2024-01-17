# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
#
# FileName:     tools
# Author:       TalentQ
# Date:         2023-8-31
#
# -------------------------------------------------------------------------------
def str_to_json(path1: str, path2: str) -> dict:
    addresses = {}
    with open(path1, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.rstrip()
            res = line.split()
            addresses[res[0]] = res[1]
    with open(path2, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.rstrip()
            res = line.split()
            addresses[res[0]] = res[1]
    return addresses
