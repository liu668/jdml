# -*- coding:utf-8 -*-
from datetime import date, datetime
import pandas as pd
from datetime import timedelta
import numpy as np
import matplotlib.pyplot as plt
action8=pd.read_csv(u'D:/Competition/JD/JNEWdata/action8.csv')
action8['time']=pd.to_datetime(action8['time'],format='%Y/%m/%d %H:%M:%S')
action8['date']=pd.to_datetime(action8['date'],format='%Y/%m/%d')

#训练集T：4/2-4/8
end_day=datetime(2016,4,9)
window_len=7
#提取4/2-4/8数据
train_data=action8[(action8.date>=(end_day-timedelta(window_len))) & (action8.date<=(end_day-timedelta(1)))]
#取4、8所有交互用户-商品对
train_end=train_data[train_data.date==(end_day-timedelta(1))][['user_id']].drop_duplicates()
#去除4、2--4、7只有浏览的用户
train_before6=train_data[train_data.date<(end_day-timedelta(1))]
def del_only_broswe(df):
    if (1 in df.values) & (2 not in df.values) & (3 not in df.values)& (4 not in df.values) &(5 not in df.values)&(6 in df.values):
         return 0
    else:
         return 1
train_before6=train_before6.groupby(['user_id'])['type'].apply(del_only_broswe).reset_index()
train_before6.columns = ['user_id','flag']
train_before6=pd.DataFrame(train_before6)
# print train_before6.head(20)
train_before6=train_before6[train_before6['flag']==1]
#融合得到所有需要的用户
train=pd.concat([train_end,train_before6])[['user_id']].drop_duplicates()
#train里user的行为
action_user=pd.merge(train,action8,on='user_id',how='left')