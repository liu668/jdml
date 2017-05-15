# -*- coding:utf-8 -*-
import pandas as pd

train=pd.read_csv('/home/javis/jd2017/jdata/train_add_all.csv')
train_comment=pd.read_csv('/home/javis/jd2017/jdata/train_comment.csv')
train=pd.merge(train,train_comment,on='sku_id',how='left')
train.to_csv('/home/javis/jd2017/jdata/train_add_comment.csv',index=False)

train=pd.read_csv('/home/javis/jd2017/jdata/test_add_all.csv')
train_comment=pd.read_csv('/home/javis/jd2017/jdata/test_comment.csv')
train=pd.merge(train,train_comment,on='sku_id',how='left')
train.to_csv('./sub/test_add_comment.csv',index=False)