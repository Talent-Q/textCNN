import pandas as pd
import tensorflow.keras as keras
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.layers import Conv1D, GlobalAveragePooling1D, GlobalMaxPooling1D, MaxPooling1D
from keras.datasets import imdb
from sklearn.metrics import accuracy_score, classification_report
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.losses import BinaryCrossentropy
import random
import numpy as np
from keras.preprocessing.text import Tokenizer
from keras.layers import Conv1D, MaxPool1D, Dense, Flatten, concatenate, Embedding, Input
from keras.models import Model
from sklearn import metrics
from tensorflow.keras import backend
import tensorflow as tf
import w_datachuli
import time
import os
import sys


# print("*************************【 指定GPU**************************")

# 返回True或者False
# tf.config.list_physical_devices('GPU')

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_XLA_FLAGS'] = '--tf_xla_enable_xla_devices'
os.environ["CUDA_VISIBLE_DEVICES"] = "0,1"  # 使用第一、二块GPU（从0开始

# print("*************************指定GPU 】**************************")



# 解决报错 NotFoundError: No algorithm worked! 
# start
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession

config = ConfigProto()
config.gpu_options.allow_growth = True
session = InteractiveSession(config=config)
# end


class Logger(object):
    def __init__(self, filename='default.log', stream=sys.stdout):
        self.terminal = stream
        self.log = open(filename, 'w')

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass


sys.stdout = Logger('./dataset/a.txt', sys.stdout)  # 生成日志文件
sys.stderr = Logger('./dataset/a.log_file', sys.stderr)


def get_lr_metric(optimizer):  # printing the value of the learning rate
    def lr(y_true, y_pred):
        return optimizer.lr

    return lr


def train_model(train_data, train_label, test_data, test_label):
    # 构建模型
    main_input = Input(shape=(max_length,), dtype='int32')
    # 词嵌入（使用预训练的词向量）
    embedder = Embedding(61, 300, input_length=max_length, trainable=False)
    embed = embedder(main_input)

    cnn1 = Conv1D(256, 3, padding='same', strides=1, activation='relu')(embed)
    cnn1 = MaxPooling1D(pool_size=48)(cnn1)
    cnn2 = Conv1D(256, 4, padding='same', strides=1, activation='relu')(embed)
    cnn2 = MaxPooling1D(pool_size=48)(cnn2)
    cnn3 = Conv1D(256, 5, padding='same', strides=1, activation='relu')(embed)
    cnn3 = MaxPooling1D(pool_size=48)(cnn3)
    cnn4 = Conv1D(256, 20, padding='same', strides=1, activation='relu')(embed)
    cnn4 = MaxPooling1D(pool_size=48)(cnn4)
    cnn5 = Conv1D(256, 30, padding='same', strides=1, activation='relu')(embed)
    cnn5 = MaxPooling1D(pool_size=48)(cnn5)
    cnn6 = Conv1D(256, 40, padding='same', strides=1, activation='relu')(embed)
    cnn6 = MaxPooling1D(pool_size=48)(cnn6)

    cnn = concatenate([cnn1, cnn2, cnn3, cnn4, cnn5, cnn6], axis=-1)
    flat = Flatten()(cnn)
    drop = Dropout(0.4)(flat)

    main_output = Dense(2, activation='softmax')(drop)  # 修改输出空间维度
    model = Model(inputs=main_input, outputs=main_output)

    optimizer = tf.keras.optimizers.Adam(learning_rate=0.005, beta_1=0.85, beta_2=0.999)
    lr_metric = get_lr_metric(optimizer)

    model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy', lr_metric])
    lr = backend.get_value(model.optimizer.lr)
    print("初始lr=", lr)
    model.summary()

    # 模型训练
    lr_reduce = keras.callbacks.ReduceLROnPlateau(monitor='val_loss',
                                                  factor=0.5,
                                                  patience=15,
                                                  verbose=1,
                                                  mode='auto',
                                                  cooldown=0)
    early_stop = keras.callbacks.EarlyStopping(monitor='val_loss',
                                               min_delta=0,
                                               patience=50,
                                               verbose=1,
                                               mode='auto')
    checkpoint = keras.callbacks.ModelCheckpoint(
        './checkpoints/model.h5',
        monitor='val_loss',
        verbose=1,
        save_best_only=True,
        save_weights_only=True,
        mode='auto',
        period=1)
    model.fit(train_data,
              train_label,
              batch_size=150,
              epochs=50,
              callbacks=[checkpoint, early_stop],
              validation_split=0.1,
              shuffle=True)

    # 模型预测
    model.load_weights('./checkpoints/model.h5')
    result = model.predict(test_data, verbose=1)  # 预测样本属于每个类别的概率
    result_labels = np.argmax(result, axis=1)  # 获得最大概率对应的标签
    test_labal_predict = list(map(str, result_labels))
    test_label = np.argmax(test_label, axis=1)
    test_labal_true = list(map(str, test_label))

    train_data_result = model.predict(train_data)
    train_label_result = np.argmax(train_data_result, axis=1)
    train_labal_predict = list(map(str, train_label_result))
    train_label = np.argmax(train_label, axis=1)
    train_labal_true = list(map(str, train_label))

    # with open('./detect_result.txt', 'a+') as f:
        # f.write(f"{'准确率':20}{str(metrics.accuracy_score(test_labal_true, test_labal_predict))}\n")
        # f.write(f"{'精度！':20}{str(metrics.precision_score(test_labal_true, test_labal_predict, average='weighted'))}\n")
        # f.write(f"{'召回率':20}{str(metrics.recall_score(test_labal_true, test_labal_predict, average='weighted'))}\n")
        # f.write(f"{'f1-score':20}{str(metrics.f1_score(test_labal_true, test_labal_predict, average='weighted'))}\n")
        # f.write(f"{'Test accuracy':20}{str(round(metrics.accuracy_score(test_labal_true, test_labal_predict), 3))}\n\n\n")

    return (str(metrics.accuracy_score(test_labal_true, test_labal_predict)), 
            str(metrics.precision_score(test_labal_true, test_labal_predict, average='weighted')), 
            str(metrics.recall_score(test_labal_true, test_labal_predict, average='weighted')), 
            str(metrics.f1_score(test_labal_true, test_labal_predict, average='weighted')))
    # print('准确率', '精度', '召回率', '平均f1-score')
    # print(metrics.accuracy_score(test_labal_true, test_labal_predict))  # 返回正确分类的比例
    # print(metrics.precision_score(test_labal_true, test_labal_predict, average='weighted'))
    # print(metrics.recall_score(test_labal_true, test_labal_predict, average='weighted'))
    # print(metrics.f1_score(test_labal_true, test_labal_predict, average='weighted'))

    # print('\n\nCNN 1D - Train accuracy:',
    #       round(metrics.accuracy_score(train_labal_true, train_labal_predict), 3))  # 训练数据的准确度
    # print('\nCNN 1D of Training data\n', metrics.classification_report(train_labal_true, train_labal_predict))
    # print('\nCNN 1D - Train Confusion Matrix\n\n',
    #       pd.crosstab(np.array(train_labal_true), np.array(train_labal_predict),
    #                   rownames=['Actuall'], colnames=['Predicted']))
    # print('\nCNN 1D - Test accuracy:', round(metrics.accuracy_score(test_labal_true, test_labal_predict), 3))
    # print('\nCNN 1D of Test data\n', classification_report(test_labal_true, test_labal_predict))
    # print('\nCNN 1D - Test Confusion Matrix\n\n', pd.crosstab(np.array(test_labal_true), np.array(test_labal_predict),
    #                                                           rownames=['Actuall'], colnames=['Predicted']))


if __name__ == '__main__':

    detect_result_dir = './detect/'
    normalpath = "./dataset/1in2outPN.json"
    normal_addr_txs_num_path = './dataset/data_ql/1in2outPN_addr_num.txt'
    specialpath_and_addr_txs_num_path = [
        ('1_LSB', './dataset/1_LSB.json', './dataset/data_ql/1_LSB_addr_num.txt'), # 1_LSB
        ('2_yxb', './dataset/2_yxb.json', './dataset/data_ql/2_yxb_addr_num.txt'), # 2_yxb
        ('3_stz_ver3.2', './dataset/3_stz_ver3.2.json', './dataset/data_ql/3_stz_ver3.2_addr_num.txt'), # 3_stz_ver3.2
        ('4_opreturn', './dataset/4_opreturn.json', './dataset/data_ql/4_opreturn_addr_num.txt'), # 4_opreturn
        ('6_DSA', './dataset/6_DSA.json', './dataset/data_ql/6_DSA_addr_num.txt'), # 6_DSA
        ('7_CHT02', './dataset/7_CHT02.json', './dataset/data_ql/7_CHT02_addr_num.txt'), # 7_CHT02
        ('8_lq_LSB_7', './dataset/8_lq_LSB_7.json', './dataset/data_ql/8_lq_LSB_7_addr_num.txt') # 8_lq_LSB_7
    ]

    time_path = time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time()))
    detect_result_path = detect_result_dir + 'result_' + time_path + '.txt'
    for schema in specialpath_and_addr_txs_num_path:
        now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

        with open(detect_result_path, 'a+') as f:
            f.write(f"\n\n\n{'|'}{'-'*87}{'|'}\n{'|   | '}{schema[0]:<19}{'|'}{' '*42}{now}{' |'}\n{'|---'}{'+--------------------'*4}{'|'}\n")
            f.write(f"{'|   '}{'| accuracy':<21}{'| precision':<21}{'| recall':<21}{'| F1':<21}{'|'}\n{'|---'}{'+--------------------'*4}{'|'}\n")

        for i in range(5):
            alldata_t, all_label, normalpath, specialpath = w_datachuli.shujuchuli(normalpath=normalpath, 
                                                                                    specialpath=schema[1],
                                                                                    normal_addr_txs_num_path=normal_addr_txs_num_path, 
                                                                                    special_addr_txs_num_path=schema[2])
            max_length = 1400  # 将句子填充到最大长度400 使数据长度保持一致
            alldata = sequence.pad_sequences(alldata_t, maxlen=max_length, padding='post')
            print("alldata[1]", alldata[1])
            all_label_oh = keras.utils.to_categorical(all_label, num_classes=2)  # 将标签转换为one-hot编码，改变标签的维度
            print("all_label_oh[1008]", all_label_oh[1008], len(all_label_oh))

            allnum = len(alldata)
            num1 = int(allnum * 0.8)  # 1820
            train_data = alldata[:num1]
            train_label = all_label_oh[:num1]
            val_data = alldata[num1:]
            val_label = all_label_oh[num1:]
            # print("train_data_num:", len(train_data))
            # print("train_label_num:", len(train_label))
            # print("val_data_num:", len(val_data))
            # print("val_label_num:", len(val_label))

            result = train_model(train_data, train_label, val_data, val_label)

            with open(detect_result_path, 'a+') as f:
                f.write(f"{'| '}{i+1:<2}{'| '}{result[0]:<19}{'| '}{result[1]:19}{'| '}{result[2]:19}{'| '}{result[3]:19}{'|'}\n{'|---'}{'+--------------------'*4}{'|'}\n")

            # print("normalpath:", normalpath)
            # print("specialpath:", specialpath)

            # print("耗时:" + str(time.time() - time_start))
