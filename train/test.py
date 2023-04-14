# 忽略警告
import warnings

warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# 导入数据集,划分特征和标签
df = pd.read_csv('heart.csv')
df.columns = ['age', 'sex', 'chest_pain_type', 'resting_blood_pressure', 'cholesterol', 'fasting_blood_sugar', 'rest_ecg', 'max_heart_rate_achieved','exercise_induced_angina', 'st_depression', 'st_slope', 'num_major_vessels', 'thalassemia', 'target']
X = df.drop('target', axis=1)
y = df['target']
# 划分训练集和测试集
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=10)

# 构建随机森林模型
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(max_depth=5, n_estimators=100)
model.fit(X_train, y_train)

## 对数据进行位置索引，从而在数据表中提取出相应的数据。
X_test.iloc
# 筛选出未知样本
test_sample = X_test.iloc[2]
# 变成二维
test_sample = np.array(test_sample).reshape(1, -1)

## 对数据进行位置索引，从而在数据表中提取出相应的数据。
X_test.iloc
# 筛选出未知样本
test_sample = X_test.iloc[2]
# 变成二维
test_sample = np.array(test_sample).reshape(1, -1)

#  二分类定性分类结果
model.predict(test_sample)
# 二分类定量分类结果
model.predict_proba(test_sample)

y_pred = model.predict(X_test)
print(y_pred)
# 得到患心脏病和不患心脏病的置信度
y_pred_proba = model.predict_proba(X_test)
print(y_pred_proba)
# 切片操作 只获得患心脏病的置信度
model.predict_proba(X_test)[:,1]
import joblib
# 保存模型到本地
joblib.dump(model, "yc.pkl")

model = joblib.load('yc.pkl')
print(X_test[0:1])
yc = model.predict(X_test[0:1])
print(yc)