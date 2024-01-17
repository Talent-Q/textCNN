# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
#
# FileName:     addr
# Author:       TalentQ
# Date:         2023-8-24
#
# -------------------------------------------------------------------------------
import json
from blockcypher import get_address_overview


# a = get_address_overview('bc1qxhmdufsvnuaaaer4ynz88fspdsxq2h9e9cetdj')
# print(a['final_n_tx'])
# print(json.dumps(a, sort_keys=True, indent=4))


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


def get_tx_num_from_addr(addr_path: str, output_path: str):
    with open(output_path, 'a') as f1:
        with open(addr_path, 'r') as f2:
            lines = f2.readlines()
            for i in range(0, len(lines)):
                lines[i] = lines[i].rstrip('\n')
                res = get_address_overview(lines[i])
                tmp = lines[i] + ' ' + str(res['final_n_tx'])
                print(str(i) + ': ' + tmp)
                f1.write(tmp + '\n')


def cht02_get_tx_num_from_addr(addr_path: str, output_path: str):
    with open(output_path, 'a') as f1:
        with open(addr_path, 'r') as f2:
            lines = f2.readlines()
            for i in range(0, len(lines)):
                lines[i] = lines[i].rstrip('\n')
                f1.write(lines[i] + ' 2\n')


def get_addr_from_txs(txs_path: str, output_path: str):
    addresses = []

    with open(output_path, 'w') as f1:
        with open(txs_path, 'r') as f2:
            txs = f2.readlines()
            for i in range(0, len(txs)):
                txs[i] = json.loads(txs[i].rstrip('\n'))  # 一行 字符串 转换成 字典
                for j in txs[i]['addresses']:
                    if j not in addresses:
                        addresses.append(j)
                        f1.write(j+'\n')


# txs_path = "../1in2outPN.json"
# output_path = "./1in2outPN.txt"
# get_addr_from_txs(txs_path, output_path)

# get_tx_num_from_addr('./1in2outPN.txt', './1in2outPN_addr_num.txt')
cht02_get_tx_num_from_addr('./7_CHT02.txt', './7_CHT02_addr_num.txt')
