# -*- coding: utf-8 -*-


"""
author ： xiaodongdong@163.com
time : 2017-04-30_18-38

基于lasso的特征选择
这个功能一般和其他的分类器一起使用
或直接内置于其他分类器算中

"""

#action1 = "D:/pythonworkspaces/data/feature/All20160409-20160415(201704028).csv"
action = "D:/pythonworkspaces/data/all_train_new430.csv"
test = "D:/pythonworkspaces/data/ysb/test.csv"
train2 = "D:/pythonworkspaces/data/ysb/train12.csv"
train3 = "D:/pythonworkspaces/data/ysb/train13.csv"
train4 = "D:/pythonworkspaces/data/ysb/train14.csv"
train5 = "D:/pythonworkspaces/data/ysb/train15.csv"
import pandas as pd
import numpy as np
import time
import sklearn.datasets
from sklearn.svm import LinearSVC
from sklearn import linear_model
from sklearn.datasets import load_iris
from sklearn.feature_selection import SelectFromModel
from sklearn.metrics import r2_score
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_boston
from sklearn.linear_model import Lasso
import matplotlib.pyplot as plt  
from sklearn import datasets,linear_model,discriminant_analysis,cross_validation
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb 

    #读取文件 
def get_from_jdata_csv(csv):
    train =  pd.read_csv(csv,header=0)
    train.fillna(0,inplace=True)
    
    return train
  



def test_Lasso(*data):
    test=pd.read_csv("D:/pythonworkspaces/data/all_test_new429.csv")
    test.fillna(0,inplace=True)    
    test_x=test.drop([ 'user_id', 'sku_id'],axis=1)  
   
    x_train,x_test,y_train,y_test = data   
    regr = RandomForestClassifier()
    #regr = linear_model.Lasso()   
 
    regr.fit_intercept = True
    regr.fit(x_train,y_train)  
    test['pred']=regr.predict(test_x)
    pred1=test[['user_id','sku_id','pred']]
    pred=pred1[pred1.pred==1]
    pred.to_csv('test_result.csv',index=False)
    
    #print('Coefficients: %s ,intercept %.2f '%(regr.coef_,regr.intercept_))
    #print len(regr.coef_)
    #print("Residual sum of squares: %.2f"%np.mean((regr.predict(x_test) - y_test)**2))
    #print ('Score :%.2f'%regr.score(x_test,y_test))       
    
def load_data(data):
    train_Y = data.label1
    train_X = data.drop([ 'label1','label2', 'label3', 'user_id', 'sku_id'],axis=1)   
    #x_train = x_train.drop([ 'label2', 'label3', 'user_id', 'sku_id'], axis=1)
    data = cross_validation.train_test_split(train_X,train_Y,test_size=0.25,random_state=0)
   
    
    return data


#检验不同的@值对于预测性能的影响，给出预测函数
def test_Lasso_alpha(*data):
    x_train,x_test,y_train,y_test = data
    alphas = [0.01,0.02,0.05,0.1,0.2,0.5,1,2,5,10,20,50,100,200,500,1000]
    scores = []
    for i , alpha in enumerate(alphas):
        regr = linear_model.Lasso(alpha = alpha)
        regr.fit(x_train,y_train)
        scores.append(regr.score(x_test,y_test))
    ##绘图：
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.plot(alphas,scores)
    ax.set_xlabel(r"$\alpha$")
    ax.set_ylabel(r"score")
    ax.set_xscale('log')
    ax.set_title('Lasso')
    plt.show()
    

if __name__ == "__main__" :
    
    print "开始运行了--runn Lasso.py"   
   
    
    x_train,x_test,y_train,y_test = load_data(data)   
       
    test_Lasso(x_train,x_test,y_train,y_test)
    #test_Lasso_alpha(x_train,x_test,y_train,y_test)
    
    