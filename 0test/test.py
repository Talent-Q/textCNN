import os
import tensorflow as tf

print("*************************【 指定GPU**************************")

# os.environ['TF_XLA_FLAGS'] = '--tf_xla_enable_xla_devices'
# os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
# print(tf.__version__)
# a = tf.constant(1.)
# b = tf.constant(2.)
# print(a)
# print(b)
os.environ['TF_XLA_FLAGS'] = '--tf_xla_enable_xla_devices'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
tf.config.list_physical_devices('GPU')

print("*************************指定GPU 】**************************")

print('\n\n\n')
print(os.environ)
