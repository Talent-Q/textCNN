from typing import List, Dict
from keras.preprocessing.text import Tokenizer
from util.tools import addr_related_txs_num_To_dict, read_txs_json, shuffle_dataset, back_up_dataset, random_data, trainset


def _data_preprocessing(rows: List[Dict], normal_addr_related_txs_num_path: str, special_addr_related_txs_num_path: str) -> List[str]:
    addresses = addr_related_txs_num_To_dict(normal_addr_related_txs_num_path, special_addr_related_txs_num_path)
    maxlength = 0
    rowslist = []
    for row in rows:
        tx_hash = row.get("hash")
        total_value = row.get("total")
        tx_fee = row.get("fees")
        vin_sz = row.get("vin_sz")
        vout_sz = row.get("vout_sz")

        inputs = row.get("inputs")
        outputs = row.get("outputs")

        input_addr = []
        input_value = []
        input_script = []
        input_prehash = []

        output_addr = []
        output_value = []
        output_script = []
        output_type = []
        output_data_string = []

        addr_related_txs_num = []

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
            output_data_string.append(a.get("data_hex"))
            if a.get("addresses") is not None:
                for addr in a.get("addresses"):
                    addr_related_txs_num.append(addresses[addr])
                    if addr not in output_addr:
                        output_addr.append(addr)
            else:
                output_addr.append('null')

        # 6. 调整了 原始 的字段顺序，并删除了几个字段, 并加入 addr_related_txs_num (0.926, 0.959, 0.933)
        # rowlist = [row.get("total"),    # number
        #            row.get("fees"),     # number
        #            row.get("vin_sz"),   # number
        #            input_value,          # number
        #            row.get("vout_sz"),  # number
        #            output_value,         # number
        #            addr_related_txs_num,        # number
        #            input_addr,
        #            output_addr,
        #            input_script,
        #            output_script]

        # 5. 调整了 原始 的字段顺序，并加入 addr_related_txs_num (0.945, 0.952, 0.911, 0.947, 0.926) => 0.94
        rowlist = [row.get("total"),    # number
                   row.get("fees"),     # number
                   row.get("vin_sz"),   # number
                   input_value,          # number
                   row.get("vout_sz"),  # number
                   output_value,         # number
                   addr_related_txs_num,        # number
                   input_addr,
                   output_addr,
                   tx_hash,
                   input_prehash,
                   input_script,
                   output_script,
                   output_type,
                   output_data_string]

        # 4. 原始， 加入 addr_related_txs_num （0.935, 0.921, 0.971, 0.94, 0.945）=> 0.94
        # rowlist = [row.get("total"),  # number
        #            row.get("fees"),  # number
        #            row.get("vin_sz"),  # number
        #            addr_related_txs_num,  # number，加入的字段
        #            input_addr,
        #            input_value,  # number
        #            input_script,
        #            row.get("vout_sz"),  # number
        #            output_addr,
        #            output_value,  # number
        #            output_script,
        #            output_type,
        #            output_data_string,
        #            tx_hash,
        #            input_prehash]

        # 3. 调整了 原始 的字段顺序，并删除了几个字段 (0.861, 0.778, 0.816, 0.825, 0.84) => 0.827
        # rowlist = [row.get("total"),    # number
        #            row.get("fees"),     # number
        #            row.get("vin_sz"),   # number
        #            input_value,          # number
        #            row.get("vout_sz"),  # number
        #            output_value,         # number
        #            input_addr,
        #            output_addr,
        #            input_script,
        #            output_script]

        # 2. 调整了 原始 的字段顺序 (0.804, 0.785, 0.792, 0.773, 0.847) => 0.794
        # rowlist = [row.get("total"),    # number
        #            row.get("fees"),     # number
        #            row.get("vin_sz"),   # number
        #            input_value,          # number
        #            row.get("vout_sz"),  # number
        #            output_value,         # number
        #            input_addr,
        #            output_addr,
        #            tx_hash,
        #            input_prehash,
        #            input_script,
        #            output_script,
        #            output_type,
        #            output_data_string]

        # 1. 原始 (0.761, 0.684,  0.77, 0.768, 0.763) => 0.764
        # rowlist = [row.get("total"),  # number
        #            row.get("fees"),  # number
        #            row.get("vin_sz"),  # number
        #            input_addr,
        #            input_value,  # number
        #            input_script,
        #            row.get("vout_sz"),  # number
        #            output_addr,
        #            output_value,  # number
        #            output_script,
        #            output_type,
        #            output_data_string,
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

    # "total": 98992600,
    # "fees": 7400,
    #
    # "vin_sz": 1,
    # "input_addrdressed": ["1Phsizjg38ZMju6EdgzuBDc8keNq7gdgub"],
    # "input_value": ["99000000"],
    # "input_script":"47304402200dd69d1300bf612abf09130d1d2e39073aa9a724fbb80c65846b14bfc8e628ea02204f4da818e35b734743494232507978e7b10ba067fd3043d50ba957fb78dafa20014104bd7ff41dcc3cf34c9feac1beb48ce1844dc1faee3432f2800c0b6c8214cd90e4e4d71a5594c74964dc2234f69fe854494a199ca7d8dc4cec0778d12073ae8e8c",
    #
    # "vout_sz": 3,
    # "output_addrdressed":[NULL,"16Wnx5y6V3yjEFHrCrGPnbAZ4fscA8AhAo","1FwZt9qtRVXxS1wNbuBF1AhVdf2GFrtCBX"],
    # "output_value":[0,98654723,337877,],
    # "output_script":["6a4c504441343144434143463735453543443536323344384339333839443642453435343734383243464542343643393537423046333638464336313038303536393337343635373337343331333133313045","76a9143c7b0c79baf8111a251e60af4a27b0b705e4710788ac","76a914a3e3abdee5f8cb30cc556a9a70d763905723390688ac",
    #                ]
    # "output_data_string":["DA41DCACF75E5CD5623D8C9389D6BE4547482CFEB46C957B0F368FC610805693746573743131310E",NULL,NULL]


def _word_embedding(dataset_texts):
    # 构建索引字典
    tokenizer = Tokenizer(lower=False, num_words=100)

    # 构建索引单词
    tokenizer.fit_on_texts(dataset_texts)
    # print("#word_index", tokenizer.word_index)

    # 将字符串转换为整数索引组成的列表
    dataset_sequences = tokenizer.texts_to_sequences(dataset_texts)

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
    back_up_dataset(dataset_texts, label, save_path)

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

