# -*- coding: UTF-8 -*-
import pandas as pd
from sklearn import cross_validation
from sklearn import linear_model

action = "/home/javis/jd2017/jdata/all_train_new429.csv"

def get_from_jdata_csv(csv):
    train =  pd.read_csv(csv,header=0)
    train.fillna(0,inplace=True)
    
    return train

def load_data_regressiong(data):
    y_train=data.label1
    x_train=data.drop([ 'label1','label2', 'label3', 'user_id', 'sku_id'],axis=1)
    data= cross_validation.train_test_split(x_train.values,y_train.values,test_size=0.1,random_state=0)
    
    return data

def test_LogisticRegressor(*data):
    test=pd.read_csv("/home/javis/jd2017/jdata/all_test_new429.csv")
    test.fillna(0,inplace=True)     
    test_x=test.drop([ 'user_id', 'sku_id'],axis=1)  
    x_train,x_test,y_train,y_test=data


    regr=linear_model.LogisticRegression(penalty='l2',max_iter=2000,C=1500.0,solver='sag',class_weight='balanced')
    regr.fit_intercept=True
    regr.fit(x_train,y_train)
    

    test['pred']=regr.predict(test_x)
    pred1=test[['user_id','sku_id','pred']]
    
    pred=pred1.sort_values('pred',ascending=False)[:1500]
    #pred=pred1[pred1.pred==1]
    pred.to_csv('./sub/logistic_result.csv',index=False)

    print regr.coef_
    print"tracing score:%f"%regr.score(x_train,y_train)
    print"testing score:%f"%regr.score(x_test,y_test)

if __name__ == '__main__':

    data = get_from_jdata_csv(action)    
    x_train,x_test,y_train,y_test=load_data_regressiong(data)
    test_LogisticRegressor(x_train,x_test,y_train,y_test)    