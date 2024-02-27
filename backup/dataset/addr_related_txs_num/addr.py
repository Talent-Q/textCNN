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


def scheme_get_tx_num_from_addr(tx_path: str, output_path: str):
    res = {}
    with open(output_path, 'a') as f1:
        with open(tx_path, 'r') as f2:
            txs = f2.readlines()
            for i in range(0, len(txs)):
                txs[i] = json.loads(txs[i].rstrip('\n'))  # 一行 字符串 转换成 字典
                for j in txs[i]['addresses']:
                    if j not in res.keys():
                        res[j] = 1
                    else:
                        res[j] += 1
        for key, value in res.items():
            f1.write(key + ' ' + str(value) + '\n')


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


if __name__ == '__main__':

    ## 1in2outPN.json
    # txs_path = "../txs_json/1in2outPN.json"
    # output_path = "./1in2outPN.txt"
    # get_addr_from_txs(txs_path, output_path)
    # get_tx_num_from_addr('./1in2outPN.txt', './1in2outPN_addr_related_txs_num.txt')

    ## others
    # scheme_get_tx_num_from_addr('../txs_json/1_LSB.json', './1_LSB_addr_related_txs_num.txt')
    # scheme_get_tx_num_from_addr('../txs_json/2_yxb.json', './2_yxb_addr_related_txs_num.txt')
    # scheme_get_tx_num_from_addr('../txs_json/3_stz_ver3.2.json', './3_stz_ver3.2_addr_related_txs_num.txt')
    # scheme_get_tx_num_from_addr('../txs_json/4_opreturn.json', './4_opreturn_addr_related_txs_num.txt')
    # scheme_get_tx_num_from_addr('../txs_json/6_DSA.json', './6_DSA_addr_related_txs_num.txt')
    # scheme_get_tx_num_from_addr('../txs_json/7_CHT02.json', './7_CHT02_addr_related_txs_num.txt')
    # scheme_get_tx_num_from_addr('../txs_json/8_lq_LSB_7.json', './8_lq_LSB_7_addr_related_txs_num.txt')
    
    pass
