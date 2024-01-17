# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
#
# FileName:     test
# Author:       TalentQ
# Date:         2023-8-29
#
# -------------------------------------------------------------------------------
with open('7_CHT02.txt', 'r') as f:
    lines = f.readlines()
    for i in range(0, len(lines)-1):
        if lines[i] == lines[i+1]:
            print(f"{i} ")
