from typing import List, Dict
from keras.preprocessing.text import Tokenizer
from util.tools import addr_related_txs_num_To_dict, read_txs_json, shuffle_dataset, back_up_dataset, random_data, trainset


def _data_preprocessing(rows: List[Dict], normal_addr_related_txs_num_path: str, special_addr_related_txs_num_path: str) -> List[str]:
    addresses = addr_related_txs_num_To_dict(normal_addr_related_txs_num_path, special_addr_related_txs_num_path)
    maxlength = 0
    rowslist = []
    for row in rows:
        inputs = row.get("inputs")
        outputs = row.get("outputs")

        ### 文本信息 ###
        tx_hash = row.get("hash")           # 弃用 hash
        total_value = row.get("total")
        tx_fee = row.get("fees")

        input_addr = []
        input_value = []
        input_script = []
        input_prehash = []                  # 弃用 hash

        output_addr = []
        output_value = []
        output_script = []
        output_type = []
        output_data_hex = []
        
        ### 结构信息 ###
        vin_sz = row.get("vin_sz")
        vout_sz = row.get("vout_sz")
        tx_size = row.get("size")           # 新增
        address_repeat = 0                  # 新增

        ### 关联信息 ###
        addr_related_txs_num = []           # 新增

        for a in inputs:
            input_value.append(a.get("output_value"))
            input_script.append(a.get("script"))
            input_prehash.append(a.get("prev_hash"))
            if a.get("addresses") is not None:
                for addr in a.get("addresses"):
                    addr_related_txs_num.append(addresses[addr])
                    if addr not in input_addr:
                        input_addr.append(addr)
            else:
                input_addr.append('null')
        for a in outputs:
            output_value.append(a.get("value"))
            output_script.append(a.get("script"))
            output_type.append(a.get("script_type"))
            output_data_hex.append(a.get("data_hex"))
            if a.get("addresses") is not None:
                for addr in a.get("addresses"):
                    addr_related_txs_num.append(addresses[addr])
                    if addr not in output_addr:
                        output_addr.append(addr)
            else:
                output_addr.append('null')

        addr = list(set(input_addr) & set(output_addr))
        if 'null' in addr:
            addr.remove('null')
        if addr == []:
            address_repeat = 0
        else:
            address_repeat = 1

        # 2. 调整了 原始 的字段顺序，并加入了 一些字段
        rowlist = [address_repeat, 
                   tx_size, 
                   vin_sz,                  # number
                   vout_sz,                 # number

                   total_value,             # number
                   tx_fee,                  # number
                   input_value,             # number
                   output_value,            # number
                #    addr_related_txs_num,    # number
                   input_addr,
                   output_addr,
                   input_script,
                   output_script,
                   output_type,
                   output_data_hex]

        # 1. 原始
        # rowlist = [total_value,  # number
        #            tx_fee,  # number
        #            vin_sz,  # number
        #            input_addr,
        #            input_value,  # number
        #            input_script,
        #            vout_sz,  # number
        #            output_addr,
        #            output_value,  # number
        #            output_script,
        #            output_type,
        #            output_data_hex,
        #            tx_hash,
        #            input_prehash]

        rowlist = str(rowlist)
        rowlist = rowlist.replace('\\n', '')
        rowlist = rowlist.replace('\"', '')
        rowlist = rowlist.replace('\'', '')
        rowlist = rowlist.replace('{', '')
        rowlist = rowlist.replace('}', '')
        rowlist = rowlist.replace('[', '')
        rowlist = rowlist.replace(']', '')
        rowlist = rowlist.replace(' ', '')
        rowlist = " ".join(rowlist)  # 这里在所有字符之间添加了空格，导致后续的分词只对单个字符进行分词

        length = len(rowlist)
        if length > maxlength:
            maxlength = length

        rowslist.append(rowlist)

    print("#maxlength=", maxlength)

    return rowslist


def _word_embedding(dataset_texts):
    '''
    dataset_texts 是一个列表，每一条数据是一个字符串文本；
    dataset_sequences是函数的输出，也是一个列表，每一条数据是一个数字序列，也称之为向量。
    实际上就是将字符串文本变成数字序列或者向量。
    '''
    # 1. 实例化 Tokenizer 对象
    tokenizer = Tokenizer(lower=False, num_words=100)

    # 2. 训练Tokenizer: 将文本数据分词并构建词汇表
    # tokenizer.word_counts:    每个词在所有文档中出现的次数
    # tokenizer.word_docs:      每个词出现的文档数量
    # tokenizer.word_index:     所有word对应的ID编号，从1开始
    # tokenizer.document_count: 处理的文档数
    tokenizer.fit_on_texts(dataset_texts)
    print('#######################################')
    print(tokenizer.word_counts)
    print('#######################################')
    print(tokenizer.word_docs)
    print('#######################################')
    print(tokenizer.word_index)
    print('#######################################')
    print(tokenizer.document_count)

    # 3. 文本向量化: dataset_sequences里是文本对应的整数序列，每个整数代表词汇表中的一个单词，每个整数序列代表对应一条文本数据
    dataset_sequences = tokenizer.texts_to_sequences(dataset_texts)
    print('#######################################')
    print(dataset_sequences)

    return dataset_sequences


def data_processing(normalpath, specialpath, normal_addr_related_txs_num_path, special_addr_related_txs_num_path, save_path):
    # 读取原始交易json
    normal_txs = read_txs_json(normalpath)
    special_txs = read_txs_json(specialpath)

    # 处理数据（手动特征提取）
    normal_data = _data_preprocessing(normal_txs, normal_addr_related_txs_num_path, special_addr_related_txs_num_path)
    special_data = _data_preprocessing(special_txs, normal_addr_related_txs_num_path, special_addr_related_txs_num_path)

    # 打乱数据集
    dataset_texts = normal_data + special_data
    label = [0 for _ in range(len(normal_data))] + [1 for _ in range(len(special_data))]
    dataset_texts, label = shuffle_dataset(dataset_texts, label)

    # 备份数据集
    # back_up_dataset(dataset_texts, label, save_path)

    # 词嵌入
    dataset_sequences = _word_embedding(dataset_texts)

    return dataset_sequences, label, normalpath, specialpath


if __name__ == '__main__':

    normalpath="./dataset/txs_json/1in2outPN.json"
    specialpath="./dataset/txs_json/6_DSA.json"
    normal_addr_related_txs_num_path='./dataset/addr_related_txs_num/1in2outPN_addr_related_txs_num.txt'
    special_addr_related_txs_num_path='./dataset/addr_related_txs_num/6_DSA_addr_related_txs_num.txt'
    save_path = './dataset/xlsx_DatasetAndLabel/dataset.xlsx'

    data_processing(normalpath, specialpath, normal_addr_related_txs_num_path, special_addr_related_txs_num_path, save_path)

