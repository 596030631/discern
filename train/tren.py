
import tensorflow as tf
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow import feature_column
from tensorflow.keras import layers

path_msg = 'heart.csv'
dataframe = pd.read_csv(path_msg)
print(dataframe.head())


train, test = train_test_split(dataframe, test_size=0.2)
train, val = train_test_split(train, test_size=0.2)
print(len(train), 'train examples')
print(len(val), 'validation examples')
print(len(test), 'test examples')


def df_to_dataset(dataframe,shuffle=True,batch_size=32):
    dataframe = dataframe.copy()
    labels = dataframe.pop('target')
    # print('---------------------')
    # print(dict(dataframe))
    # print('+++++++++++++++++++++')
    ds = tf.data.Dataset.from_tensor_slices((dict(dataframe),labels))

    if shuffle:
        #将数据混乱
        ds = ds.shuffle(buffer_size=len(dataframe))
    ds = ds.batch(batch_size)

    return ds


#创建数据输入管道
batch_size = 5
train_ds = df_to_dataset(train,batch_size=batch_size)
val_ds = df_to_dataset(val,shuffle=False,batch_size=batch_size)
test_ds = df_to_dataset(test,shuffle=False,batch_size=batch_size)


#检测管道返回的数据格式是否匹配
for feature_batch, label_batch in train_ds.take(1):
  print('Every feature:', list(feature_batch.keys()))
  print('A batch of ages:', feature_batch['age'])
  print('A batch of targets:', label_batch )



# # 我们将使用此批处理来演示几种类型的特征列
# example_batch = next(iter(train_ds))[0]
#
# # 用于创建特征列和转换批量数据
# def demo(feature_column):
#   feature_layer = layers.DenseFeatures(feature_column)
#   print(feature_layer(example_batch).numpy())



feature_columns = []

age = feature_column.numeric_column("age")


# numeric 数字列
for header in ['age', 'trestbps', 'chol', 'thalach', 'oldpeak', 'slope', 'ca']:
  feature_columns.append(feature_column.numeric_column(header))

# bucketized 分桶列
age_buckets = feature_column.bucketized_column(age, boundaries=[18, 25, 30, 35, 40, 45, 50, 55, 60, 65])
feature_columns.append(age_buckets)

# indicator 指示符列
thal = feature_column.categorical_column_with_vocabulary_list(
      'thal', ['fixed', 'normal', 'reversible'])
thal_one_hot = feature_column.indicator_column(thal)
feature_columns.append(thal_one_hot)

# embedding 嵌入列
thal_embedding = feature_column.embedding_column(thal, dimension=8)
feature_columns.append(thal_embedding)

# crossed 交叉列
crossed_feature = feature_column.crossed_column([age_buckets, thal], hash_bucket_size=1000)
crossed_feature = feature_column.indicator_column(crossed_feature)
feature_columns.append(crossed_feature)

#使用DenseFeatures层将feature_columns输入到keras中
feature_layer = tf.keras.layers.DenseFeatures(feature_columns)

#提取32的输入管道
batch_size = 32
train_ds = df_to_dataset(train, batch_size=batch_size)
val_ds = df_to_dataset(val, shuffle=False, batch_size=batch_size)
test_ds = df_to_dataset(test, shuffle=False, batch_size=batch_size)

#构建模型层
model = tf.keras.Sequential([
  feature_layer,
  layers.Dense(128, activation='relu'),
  layers.Dense(128, activation='relu'),
  layers.Dense(1, activation='sigmoid')
])

#定义模型优化器，损失函数，以及训练中显示的值（下面显示的是成功率accuracy）
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

#定义模型训练输入（train_ds）,模型输出labels（val_ds）,训练次数
model.fit(train_ds,
          validation_data=val_ds,
          epochs=5)


#使用evaluate进行模型检测，返回值为损失率（loss）和成功率（accuracy）
loss , accuracy = model.evaluate(test_ds)
print('当前预测成功率为:',accuracy)
