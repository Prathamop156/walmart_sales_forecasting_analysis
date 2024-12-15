# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 20GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session
def load_data(datapath):
    data = pd.read_csv(datapath)
   
    print('Shape:', data.shape)
    
    display(data.sample(10))
    return data
traindf=load_data('../input/walmart-sales-forecast/train.csv')
testdf=load_data('../input/walmart-sales-forecast/test.csv')
featuresdf=load_data('../input/walmart-sales-forecast/features.csv')
storesdf=load_data('../input/walmart-sales-forecast/stores.csv')

traindf1=traindf.merge(featuresdf,how='left',indicator=True).merge(storesdf,how='left')
traindf2=traindf1.drop(['MarkDown1','MarkDown2','MarkDown3','MarkDown4','MarkDown5'],axis=1)
traindf2.isna().sum()
traindf2.loc[traindf2['Weekly_Sales']<=0] 

traindf3=traindf2.loc[traindf2['Weekly_Sales']>0]
traindf4=traindf3.drop(['_merge'],axis=1)

traindf4.sort_values(by='Date')
traindf4['Type'].unique() 

import matplotlib.pyplot as plt
import numpy as np



stores = ['Type A','Type B','Type C']

data = traindf4['Type'].value_counts()


fig, ax = plt.subplots()
plt.pie(data, labels = stores,autopct='%.0f%%')
ax.set_title('Which Type of stores has more sales')

plt.show()

traindf4['year'] = pd.DatetimeIndex(traindf4['Date']).year 

import matplotlib.pyplot as mp
import pandas as pd
import seaborn as sns


data = traindf4


print(data.corr())
sns.set_theme(style="whitegrid")

dataplot = sns.heatmap(data.corr(), cmap="YlGnBu", annot=True)
sns.set(rc = {'figure.figsize':(25,8)})


mp.show()

print(traindf4.dtypes)
import seaborn as sns
sns.set_theme(style="whitegrid")
tips =traindf4
ax = sns.barplot(x="year", y="Fuel_Price", data=tips)
sns.set(rc = {'figure.figsize':(10,4)})
import seaborn as sns
sns.set_theme(style="whitegrid")
tips = traindf4
ax = sns.barplot(x='Store', y="Weekly_Sales", data=tips)

import seaborn as sns
import matplotlib.pyplot as plt


data = traindf4


sns.lineplot(x="Store", y="Unemployment", data=data)
plt.show()
traindf4['Dept'].unique()

import seaborn as sns
import matplotlib.pyplot as plt


data =traindf4


sns.pointplot(x ='Dept',
			y = "Weekly_Sales",
			data = data)

sns.set(rc = {'figure.figsize':(25,8)})
plt.show()

traindf4['month'] = pd.DatetimeIndex(traindf4['Date']).month 
traindf4['week'] = pd.DatetimeIndex(traindf4['Date']).week 
traindf5=traindf4.drop(['Date'],axis=1)

from sklearn import preprocessing


label_encoder = preprocessing.LabelEncoder()


traindf5['IsHoliday']= label_encoder.fit_transform(traindf5['IsHoliday'])
traindf5['Type']= label_encoder.fit_transform(traindf5['Type'])

traindf5

data = traindf5


print(data.corr())
sns.set_theme(style="whitegrid")

dataplot = sns.heatmap(data.corr(), cmap="YlGnBu", annot=True)
sns.set(rc = {'figure.figsize':(25,8)})


mp.show()
from sklearn.inspection import permutation_importance
from sklearn.ensemble import RandomForestRegressor
import shap

Features=traindf5.drop(['Weekly_Sales'],axis=1)
Target=traindf5['Weekly_Sales']

rf = RandomForestRegressor(n_estimators=100)
rf.fit(Features,Target)

f = plt.figure()
f.set_figwidth(10)
f.set_figheight(7)
plt.barh(Features.columns, rf.feature_importances_)

F=Features.drop(["IsHoliday",'year'],axis=1)

from sklearn.model_selection import train_test_split  
x_train, x_test, y_train, y_test= train_test_split(F, Target, test_size= 0.25, random_state=0)

from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import r2_score,mean_squared_error
from math import sqrt

DTRmodel = DecisionTreeRegressor(max_depth=3,random_state=0)
DTRmodel.fit(x_train,y_train)
y_pred = DTRmodel.predict(x_test)

print("R2 score  :",r2_score(y_test, y_pred))
print("MSE score  :",mean_squared_error(y_test, y_pred))
print("RMSE: ",sqrt(mean_squared_error(y_test, y_pred)))

rf1 = RandomForestRegressor(n_estimators=50, random_state=42, n_jobs=-1, max_depth=35,
                           max_features = 'sqrt',min_samples_split = 10)
rf1.fit(x_train,y_train)
y_pred1 = rf1.predict(x_test)

print("R2 score  :",r2_score(y_test, y_pred))
print("MSE score  :",mean_squared_error(y_test, y_pred1))
print("RMSE: ",sqrt(mean_squared_error(y_test, y_pred1)))

from xgboost import XGBRegressor
model = XGBRegressor()
model.fit(x_train,y_train)

y_pred2 = model.predict(x_test)

print("R2 score  :",r2_score(y_test, y_pred2))
print("MSE score  :",mean_squared_error(y_test, y_pred2))
print("RMSE: ",sqrt(mean_squared_error(y_test, y_pred2)))

from sklearn.linear_model import Ridge
rr_model = Ridge(alpha=0.5)
rr_model.fit(x_train,y_train)

y_pred3 = model.predict(x_test)

print("R2 score  :",r2_score(y_test, y_pred3))
print("MSE score  :",mean_squared_error(y_test, y_pred3))
print("RMSE: ",sqrt(mean_squared_error(y_test, y_pred3)))

y_test