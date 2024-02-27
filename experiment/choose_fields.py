'''
1

# 字段：只保留 “文本信息”  10 fields
# 效果：只对 op_return 方案有效，准确度达到 1
# 结论：需要添加字段

rowlist = [total_value,             # number
            tx_fee,                  # number
        #    vin_sz,                  # number
            input_value,             # number
        #    vout_sz,                 # number
            output_value,            # number
        #    addr_related_txs_num,    # number
            input_addr,
            output_addr,
        #    tx_hash,
        #    input_prehash,
            input_script,
            output_script,
            output_type,
            output_data_string]
'''

'''
2

# 字段：“文本信息” “结构信息” “关联信息”  13 fields
# 效果：很好
# 结论：目前这样的准确度已经够了

rowlist = [total_value,             # number
            tx_fee,                  # number
            vin_sz,                  # number
            input_value,             # number
            vout_sz,                 # number
            output_value,            # number
            addr_related_txs_num,    # number
            input_addr,
            output_addr,
        #    tx_hash,
        #    input_prehash,
            input_script,
            output_script,
            output_type,
            output_data_hex]

'''
