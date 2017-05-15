# -*- coding:utf-8 -*-
from datetime import date, datetime, timedelta,time
import pandas as pd

actionAll_raw=pd.read_csv(u'/home/javis/jd2017/jdata/JData_actionAll_drop_duplicates.csv')
actionAll_raw['date']=pd.to_datetime(actionAll_raw['date'],format='%Y/%m/%d')
action8=pd.read_csv(u'/home/javis/jd2017/jdata/action8.csv')
action8['date']=pd.to_datetime(action8['date'],format='%Y/%m/%d')
enddays=[date(2016,4,15)]
# 取前10天交互的user-item对
select_user_item = action8[(action8.date >= enddays - timedelta(34)) & (action8.date <= enddays - timedelta(5))]
train = select_user_item[['user_id']].drop_duplicates()

# 特征提取
actionAll = actionAll_raw[(actionAll_raw.date <= enddays - timedelta(5))]
actionAll['time_diff'] = [-int(i.days) for i in (actionAll['date'] - (enddays - timedelta(4)))]

actionAll=actionAll[['user_id','type','cate','brand','date','time_diff']]
#用户购买次数与各行为的比值
user_all_type_action=actionAll[['user_id','type','time_diff']]
df = pd.get_dummies(user_all_type_action['type'], prefix='type')
user_all_type_action1 = pd.concat([user_all_type_action[['user_id']], df], axis=1)
df=user_all_type_action1.groupby(['user_id']).sum().reset_index()
train_temp=train[['user_id']].drop_duplicates()
for i in (1,2,3,5,6):
    df['all_user_type4_rate_type%s'%(i)]=(df.type_4)*1.0/(df['type_%s'%(i)]+0.00001)
    train_temp=pd.merge(train_temp,df[['user_id','all_user_type4_rate_type%s'%(i)]],on='user_id',how='left')
train=pd.merge(train,train_temp,on='user_id',how='left')

temp_action=actionAll[actionAll.time_diff<=61][['user_id','type','time_diff']]
df = pd.get_dummies(temp_action['type'], prefix='type')
temp = pd.concat([temp_action[['user_id']], df], axis=1)
df=temp.groupby(['user_id']).sum().reset_index()
train_temp=train[['user_id']].drop_duplicates()
for i in (1,2,3,5,6):
    df['all_before61_user_type4_rate_type%s'%(i)]=(df.type_4)*1.0/(df['type_%s'%(i)]+0.00001)
    train_temp=pd.merge(train_temp,df[['user_id','all_before61_user_type4_rate_type%s'%(i)]],on='user_id',how='left')
train=pd.merge(train,train_temp,on='user_id',how='left')

temp_action=actionAll[actionAll.time_diff<=56][['user_id','type','time_diff']]
df = pd.get_dummies(temp_action['type'], prefix='type')
temp = pd.concat([temp_action[['user_id']], df], axis=1)
df=temp.groupby(['user_id']).sum().reset_index()
train_temp=train[['user_id']].drop_duplicates()
for i in (1,2,3,5,6):
    df['all_before56_user_type4_rate_type%s'%(i)]=(df.type_4)*1.0/(df['type_%s'%(i)]+0.00001)
    train_temp=pd.merge(train_temp,df[['user_id','all_before56_user_type4_rate_type%s'%(i)]],on='user_id',how='left')
train=pd.merge(train,train_temp,on='user_id',how='left')

temp_action=actionAll[actionAll.time_diff<=49][['user_id','type','time_diff']]
df = pd.get_dummies(temp_action['type'], prefix='type')
temp = pd.concat([temp_action[['user_id']], df], axis=1)
df=temp.groupby(['user_id']).sum().reset_index()
train_temp=train[['user_id']].drop_duplicates()
for i in (1,2,3,5,6):
    df['all_before49_user_type4_rate_type%s'%(i)]=(df.type_4)*1.0/(df['type_%s'%(i)]+0.00001)
    train_temp=pd.merge(train_temp,df[['user_id','all_before49_user_type4_rate_type%s'%(i)]],on='user_id',how='left')
train=pd.merge(train,train_temp,on='user_id',how='left')

temp_action=actionAll[actionAll.time_diff<=42][['user_id','type','time_diff']]
df = pd.get_dummies(temp_action['type'], prefix='type')
temp = pd.concat([temp_action[['user_id']], df], axis=1)
df=temp.groupby(['user_id']).sum().reset_index()
train_temp=train[['user_id']].drop_duplicates()
for i in (1,2,3,5,6):
    df['all_before42_user_type4_rate_type%s'%(i)]=(df.type_4)*1.0/(df['type_%s'%(i)]+0.00001)
    train_temp=pd.merge(train_temp,df[['user_id','all_before42_user_type4_rate_type%s'%(i)]],on='user_id',how='left')
train=pd.merge(train,train_temp,on='user_id',how='left')

temp_action=actionAll[actionAll.time_diff<=35][['user_id','type','time_diff']]
df = pd.get_dummies(temp_action['type'], prefix='type')
temp = pd.concat([temp_action[['user_id']], df], axis=1)
df=temp.groupby(['user_id']).sum().reset_index()
train_temp=train[['user_id']].drop_duplicates()
for i in (1,2,3,5,6):
    df['all_before35_user_type4_rate_type%s'%(i)]=(df.type_4)*1.0/(df['type_%s'%(i)]+0.00001)
    train_temp=pd.merge(train_temp,df[['user_id','all_before35_user_type4_rate_type%s'%(i)]],on='user_id',how='left')
train=pd.merge(train,train_temp,on='user_id',how='left')

temp_action=actionAll[actionAll.time_diff<=28][['user_id','type','time_diff']]
df = pd.get_dummies(temp_action['type'], prefix='type')
temp = pd.concat([temp_action[['user_id']], df], axis=1)
df=temp.groupby(['user_id']).sum().reset_index()
train_temp=train[['user_id']].drop_duplicates()
for i in (1,2,3,5,6):
    df['all_before28_user_type4_rate_type%s'%(i)]=(df.type_4)*1.0/(df['type_%s'%(i)]+0.00001)
    train_temp=pd.merge(train_temp,df[['user_id','all_before28_user_type4_rate_type%s'%(i)]],on='user_id',how='left')
train=pd.merge(train,train_temp,on='user_id',how='left')


user_all_before21_type_action=actionAll[actionAll.time_diff<=21][['user_id','type','time_diff']]
df = pd.get_dummies(user_all_before21_type_action['type'], prefix='type')
temp = pd.concat([user_all_before21_type_action[['user_id']], df], axis=1)
df=temp.groupby(['user_id']).sum().reset_index()
train_temp=train[['user_id']].drop_duplicates()
for i in (1,2,3,5,6):
    df['all_before21_user_type4_rate_type%s'%(i)]=(df.type_4)*1.0/(df['type_%s'%(i)]+0.00001)
    train_temp=pd.merge(train_temp,df[['user_id','all_before21_user_type4_rate_type%s'%(i)]],on='user_id',how='left')
train=pd.merge(train,train_temp,on='user_id',how='left')

user_all_before14_type_action=actionAll[actionAll.time_diff<=14][['user_id','type','time_diff']]
df = pd.get_dummies(user_all_before14_type_action['type'], prefix='type')
temp = pd.concat([user_all_before14_type_action[['user_id']], df], axis=1)
df=temp.groupby(['user_id']).sum().reset_index()
train_temp=train[['user_id']].drop_duplicates()
for i in (1,2,3,5,6):
    df['all_before14_user_type4_rate_type%s'%(i)]=(df.type_4)*1.0/(df['type_%s'%(i)]+0.00001)
    train_temp=pd.merge(train_temp,df[['user_id','all_before14_user_type4_rate_type%s'%(i)]],on='user_id',how='left')
train=pd.merge(train,train_temp,on='user_id',how='left')

user_all_before7_type_action=actionAll[actionAll.time_diff<=7][['user_id','type','time_diff']]
df = pd.get_dummies(user_all_before7_type_action['type'], prefix='type')
temp = pd.concat([user_all_before7_type_action[['user_id']], df], axis=1)
df=temp.groupby(['user_id']).sum().reset_index()
train_temp=train[['user_id']].drop_duplicates()
for i in (1,2,3,5,6):
    df['all_before7_user_type4_rate_type%s'%(i)]=(df.type_4)*1.0/(df['type_%s'%(i)]+0.00001)
    train_temp=pd.merge(train_temp,df[['user_id','all_before7_user_type4_rate_type%s'%(i)]],on='user_id',how='left')
train=pd.merge(train,train_temp,on='user_id',how='left')

#用户cate8个行为总数，比值总行为数
user_all_cate8_action=actionAll[['user_id','type','cate']]
df = pd.get_dummies(user_all_cate8_action['type'], prefix='type')
temp = pd.concat([user_all_cate8_action[['user_id','cate']], df], axis=1)
df=temp.groupby(['user_id','cate']).sum().reset_index()
def user_cate8_type1_rate_all(df):
    return df[df.cate==8].type_1.sum()*1.0/(df.type_1.sum()+0.0001)
temp=df.groupby('user_id')[['cate','type_1']].apply(user_cate8_type1_rate_all).reset_index()
temp.columns=['user_id','user_cate8_type1_rate_all']
train=pd.merge(train,temp,on='user_id',how='left')

def user_cate8_type2_rate_all(df):
    return df[df.cate==8].type_2.sum()*1.0/(df.type_2.sum()+0.0001)
temp=df.groupby('user_id')[['cate','type_2']].apply(user_cate8_type2_rate_all).reset_index()
temp.columns=['user_id','user_cate8_type2_rate_all']
train=pd.merge(train,temp,on='user_id',how='left')

def user_cate8_type3_rate_all(df):
    return df[df.cate==8].type_3.sum()*1.0/(df.type_3.sum()+0.0001)
temp=df.groupby('user_id')[['cate','type_3']].apply(user_cate8_type3_rate_all).reset_index()
temp.columns=['user_id','user_cate8_type3_rate_all']
train=pd.merge(train,temp,on='user_id',how='left')

def user_cate8_type4_rate_all(df):
    return df[df.cate==8].type_4.sum()*1.0/(df.type_4.sum()+0.0001)
temp=df.groupby('user_id')[['cate','type_4']].apply(user_cate8_type4_rate_all).reset_index()
temp.columns=['user_id','user_cate8_type4_rate_all']
train=pd.merge(train,temp,on='user_id',how='left')

def user_cate8_type5_rate_all(df):
    return df[df.cate==8].type_5.sum()*1.0/(df.type_5.sum()+0.0001)
temp=df.groupby('user_id')[['cate','type_5']].apply(user_cate8_type5_rate_all).reset_index()
temp.columns=['user_id','user_cate8_type5_rate_all']
train=pd.merge(train,temp,on='user_id',how='left')

def user_cate8_type6_rate_all(df):
    return df[df.cate==8].type_6.sum()*1.0/(df.type_6.sum()+0.0001)
temp=df.groupby('user_id')[['cate','type_6']].apply(user_cate8_type6_rate_all).reset_index()
temp.columns=['user_id','user_cate8_type6_rate_all']
train=pd.merge(train,temp,on='user_id',how='left')


# ##用户前61天cate8个行为总数，比值总行为数
# user_all_before61_cate8_action=actionAll[actionAll.time_diff<=61][['user_id','type','cate']]
# df = pd.get_dummies(user_all_before61_cate8_action['type'], prefix='type')
# temp = pd.concat([user_all_before61_cate8_action[['user_id','cate']], df], axis=1)
# df=temp.groupby(['user_id','cate']).sum().reset_index()
# def user_cate8_type1_rate_all(df):
#     return df[df.cate==8].type_1.sum()*1.0/(df.type_1.sum()+0.0001)
# temp=df.groupby('user_id')[['cate','type_1']].apply(user_cate8_type1_rate_all).reset_index()
# temp.columns=['user_id','user_cate8_type1_rate_all_before61']
# train=pd.merge(train,temp,on='user_id',how='left')
#
# def user_cate8_type2_rate_all(df):
#     return df[df.cate==8].type_2.sum()*1.0/(df.type_2.sum()+0.0001)
# temp=df.groupby('user_id')[['cate','type_2']].apply(user_cate8_type2_rate_all).reset_index()
# temp.columns=['user_id','user_cate8_type2_rate_all_before61']
# train=pd.merge(train,temp,on='user_id',how='left')
#
# def user_cate8_type3_rate_all(df):
#     return df[df.cate==8].type_3.sum()*1.0/(df.type_3.sum()+0.0001)
# temp=df.groupby('user_id')[['cate','type_3']].apply(user_cate8_type3_rate_all).reset_index()
# temp.columns=['user_id','user_cate8_type3_rate_all_before61']
# train=pd.merge(train,temp,on='user_id',how='left')
#
# def user_cate8_type4_rate_all(df):
#     return df[df.cate==8].type_4.sum()*1.0/(df.type_4.sum()+0.0001)
# temp=df.groupby('user_id')[['cate','type_4']].apply(user_cate8_type4_rate_all).reset_index()
# temp.columns=['user_id','user_cate8_type4_rate_all_before61']
# train=pd.merge(train,temp,on='user_id',how='left')
#
# def user_cate8_type5_rate_all(df):
#     return df[df.cate==8].type_5.sum()*1.0/(df.type_5.sum()+0.0001)
# temp=df.groupby('user_id')[['cate','type_5']].apply(user_cate8_type5_rate_all).reset_index()
# temp.columns=['user_id','user_cate8_type5_rate_all_before61']
# train=pd.merge(train,temp,on='user_id',how='left')
#
# def user_cate8_type6_rate_all(df):
#     return df[df.cate==8].type_6.sum()*1.0/(df.type_6.sum()+0.0001)
# temp=df.groupby('user_id')[['cate','type_6']].apply(user_cate8_type6_rate_all).reset_index()
# temp.columns=['user_id','user_cate8_type6_rate_all_before61']
# train=pd.merge(train,temp,on='user_id',how='left')
#
# ##用户前56天cate8个行为总数，比值总行为数
# user_all_before56_cate8_action=actionAll[actionAll.time_diff<=56][['user_id','type','cate']]
# df = pd.get_dummies(user_all_before56_cate8_action['type'], prefix='type')
# temp = pd.concat([user_all_before56_cate8_action[['user_id','cate']], df], axis=1)
# df=temp.groupby(['user_id','cate']).sum().reset_index()
# def user_cate8_type1_rate_all(df):
#     return df[df.cate==8].type_1.sum()*1.0/(df.type_1.sum()+0.0001)
# temp=df.groupby('user_id')[['cate','type_1']].apply(user_cate8_type1_rate_all).reset_index()
# temp.columns=['user_id','user_cate8_type1_rate_all_before56']
# train=pd.merge(train,temp,on='user_id',how='left')
#
# def user_cate8_type2_rate_all(df):
#     return df[df.cate==8].type_2.sum()*1.0/(df.type_2.sum()+0.0001)
# temp=df.groupby('user_id')[['cate','type_2']].apply(user_cate8_type2_rate_all).reset_index()
# temp.columns=['user_id','user_cate8_type2_rate_all_before56']
# train=pd.merge(train,temp,on='user_id',how='left')
#
# def user_cate8_type3_rate_all(df):
#     return df[df.cate==8].type_3.sum()*1.0/(df.type_3.sum()+0.0001)
# temp=df.groupby('user_id')[['cate','type_3']].apply(user_cate8_type3_rate_all).reset_index()
# temp.columns=['user_id','user_cate8_type3_rate_all_before56']
# train=pd.merge(train,temp,on='user_id',how='left')
#
# def user_cate8_type4_rate_all(df):
#     return df[df.cate==8].type_4.sum()*1.0/(df.type_4.sum()+0.0001)
# temp=df.groupby('user_id')[['cate','type_4']].apply(user_cate8_type4_rate_all).reset_index()
# temp.columns=['user_id','user_cate8_type4_rate_all_before56']
# train=pd.merge(train,temp,on='user_id',how='left')
#
# def user_cate8_type5_rate_all(df):
#     return df[df.cate==8].type_5.sum()*1.0/(df.type_5.sum()+0.0001)
# temp=df.groupby('user_id')[['cate','type_5']].apply(user_cate8_type5_rate_all).reset_index()
# temp.columns=['user_id','user_cate8_type5_rate_all_before56']
# train=pd.merge(train,temp,on='user_id',how='left')
#
# def user_cate8_type6_rate_all(df):
#     return df[df.cate==8].type_6.sum()*1.0/(df.type_6.sum()+0.0001)
# temp=df.groupby('user_id')[['cate','type_6']].apply(user_cate8_type6_rate_all).reset_index()
# temp.columns=['user_id','user_cate8_type6_rate_all_before56']
# train=pd.merge(train,temp,on='user_id',how='left')
#
# ##用户前49天cate8个行为总数，比值总行为数
# user_all_before49_cate8_action=actionAll[actionAll.time_diff<=49][['user_id','type','cate']]
# df = pd.get_dummies(user_all_before49_cate8_action['type'], prefix='type')
# temp = pd.concat([user_all_before49_cate8_action[['user_id','cate']], df], axis=1)
# df=temp.groupby(['user_id','cate']).sum().reset_index()
# def user_cate8_type1_rate_all(df):
#     return df[df.cate==8].type_1.sum()*1.0/(df.type_1.sum()+0.0001)
# temp=df.groupby('user_id')[['cate','type_1']].apply(user_cate8_type1_rate_all).reset_index()
# temp.columns=['user_id','user_cate8_type1_rate_all_before49']
# train=pd.merge(train,temp,on='user_id',how='left')
#
# def user_cate8_type2_rate_all(df):
#     return df[df.cate==8].type_2.sum()*1.0/(df.type_2.sum()+0.0001)
# temp=df.groupby('user_id')[['cate','type_2']].apply(user_cate8_type2_rate_all).reset_index()
# temp.columns=['user_id','user_cate8_type2_rate_all_before49']
# train=pd.merge(train,temp,on='user_id',how='left')
#
# def user_cate8_type3_rate_all(df):
#     return df[df.cate==8].type_3.sum()*1.0/(df.type_3.sum()+0.0001)
# temp=df.groupby('user_id')[['cate','type_3']].apply(user_cate8_type3_rate_all).reset_index()
# temp.columns=['user_id','user_cate8_type3_rate_all_before49']
# train=pd.merge(train,temp,on='user_id',how='left')
#
# def user_cate8_type4_rate_all(df):
#     return df[df.cate==8].type_4.sum()*1.0/(df.type_4.sum()+0.0001)
# temp=df.groupby('user_id')[['cate','type_4']].apply(user_cate8_type4_rate_all).reset_index()
# temp.columns=['user_id','user_cate8_type4_rate_all_before49']
# train=pd.merge(train,temp,on='user_id',how='left')
#
# def user_cate8_type5_rate_all(df):
#     return df[df.cate==8].type_5.sum()*1.0/(df.type_5.sum()+0.0001)
# temp=df.groupby('user_id')[['cate','type_5']].apply(user_cate8_type5_rate_all).reset_index()
# temp.columns=['user_id','user_cate8_type5_rate_all_before49']
# train=pd.merge(train,temp,on='user_id',how='left')
#
# def user_cate8_type6_rate_all(df):
#     return df[df.cate==8].type_6.sum()*1.0/(df.type_6.sum()+0.0001)
# temp=df.groupby('user_id')[['cate','type_6']].apply(user_cate8_type6_rate_all).reset_index()
# temp.columns=['user_id','user_cate8_type6_rate_all_before49']
# train=pd.merge(train,temp,on='user_id',how='left')

##用户前42天cate8个行为总数，比值总行为数
user_all_before42_cate8_action=actionAll[actionAll.time_diff<=42][['user_id','type','cate']]
df = pd.get_dummies(user_all_before42_cate8_action['type'], prefix='type')
temp = pd.concat([user_all_before42_cate8_action[['user_id','cate']], df], axis=1)
df=temp.groupby(['user_id','cate']).sum().reset_index()
def user_cate8_type1_rate_all(df):
    return df[df.cate==8].type_1.sum()*1.0/(df.type_1.sum()+0.0001)
temp=df.groupby('user_id')[['cate','type_1']].apply(user_cate8_type1_rate_all).reset_index()
temp.columns=['user_id','user_cate8_type1_rate_all_before42']
train=pd.merge(train,temp,on='user_id',how='left')

def user_cate8_type2_rate_all(df):
    return df[df.cate==8].type_2.sum()*1.0/(df.type_2.sum()+0.0001)
temp=df.groupby('user_id')[['cate','type_2']].apply(user_cate8_type2_rate_all).reset_index()
temp.columns=['user_id','user_cate8_type2_rate_all_before42']
train=pd.merge(train,temp,on='user_id',how='left')

def user_cate8_type3_rate_all(df):
    return df[df.cate==8].type_3.sum()*1.0/(df.type_3.sum()+0.0001)
temp=df.groupby('user_id')[['cate','type_3']].apply(user_cate8_type3_rate_all).reset_index()
temp.columns=['user_id','user_cate8_type3_rate_all_before42']
train=pd.merge(train,temp,on='user_id',how='left')

def user_cate8_type4_rate_all(df):
    return df[df.cate==8].type_4.sum()*1.0/(df.type_4.sum()+0.0001)
temp=df.groupby('user_id')[['cate','type_4']].apply(user_cate8_type4_rate_all).reset_index()
temp.columns=['user_id','user_cate8_type4_rate_all_before42']
train=pd.merge(train,temp,on='user_id',how='left')

def user_cate8_type5_rate_all(df):
    return df[df.cate==8].type_5.sum()*1.0/(df.type_5.sum()+0.0001)
temp=df.groupby('user_id')[['cate','type_5']].apply(user_cate8_type5_rate_all).reset_index()
temp.columns=['user_id','user_cate8_type5_rate_all_before42']
train=pd.merge(train,temp,on='user_id',how='left')

def user_cate8_type6_rate_all(df):
    return df[df.cate==8].type_6.sum()*1.0/(df.type_6.sum()+0.0001)
temp=df.groupby('user_id')[['cate','type_6']].apply(user_cate8_type6_rate_all).reset_index()
temp.columns=['user_id','user_cate8_type6_rate_all_before42']
train=pd.merge(train,temp,on='user_id',how='left')

##用户前35天cate8个行为总数，比值总行为数
user_all_before35_cate8_action=actionAll[actionAll.time_diff<=35][['user_id','type','cate']]
df = pd.get_dummies(user_all_before35_cate8_action['type'], prefix='type')
temp = pd.concat([user_all_before35_cate8_action[['user_id','cate']], df], axis=1)
df=temp.groupby(['user_id','cate']).sum().reset_index()
def user_cate8_type1_rate_all(df):
    return df[df.cate==8].type_1.sum()*1.0/(df.type_1.sum()+0.0001)
temp=df.groupby('user_id')[['cate','type_1']].apply(user_cate8_type1_rate_all).reset_index()
temp.columns=['user_id','user_cate8_type1_rate_all_before35']
train=pd.merge(train,temp,on='user_id',how='left')

def user_cate8_type2_rate_all(df):
    return df[df.cate==8].type_2.sum()*1.0/(df.type_2.sum()+0.0001)
temp=df.groupby('user_id')[['cate','type_2']].apply(user_cate8_type2_rate_all).reset_index()
temp.columns=['user_id','user_cate8_type2_rate_all_before35']
train=pd.merge(train,temp,on='user_id',how='left')

def user_cate8_type3_rate_all(df):
    return df[df.cate==8].type_3.sum()*1.0/(df.type_3.sum()+0.0001)
temp=df.groupby('user_id')[['cate','type_3']].apply(user_cate8_type3_rate_all).reset_index()
temp.columns=['user_id','user_cate8_type3_rate_all_before35']
train=pd.merge(train,temp,on='user_id',how='left')

def user_cate8_type4_rate_all(df):
    return df[df.cate==8].type_4.sum()*1.0/(df.type_4.sum()+0.0001)
temp=df.groupby('user_id')[['cate','type_4']].apply(user_cate8_type4_rate_all).reset_index()
temp.columns=['user_id','user_cate8_type4_rate_all_before35']
train=pd.merge(train,temp,on='user_id',how='left')

def user_cate8_type5_rate_all(df):
    return df[df.cate==8].type_5.sum()*1.0/(df.type_5.sum()+0.0001)
temp=df.groupby('user_id')[['cate','type_5']].apply(user_cate8_type5_rate_all).reset_index()
temp.columns=['user_id','user_cate8_type5_rate_all_before35']
train=pd.merge(train,temp,on='user_id',how='left')

def user_cate8_type6_rate_all(df):
    return df[df.cate==8].type_6.sum()*1.0/(df.type_6.sum()+0.0001)
temp=df.groupby('user_id')[['cate','type_6']].apply(user_cate8_type6_rate_all).reset_index()
temp.columns=['user_id','user_cate8_type6_rate_all_before35']
train=pd.merge(train,temp,on='user_id',how='left')

##用户前28天cate8个行为总数，比值总行为数
user_all_before28_cate8_action=actionAll[actionAll.time_diff<=28][['user_id','type','cate']]
df = pd.get_dummies(user_all_before28_cate8_action['type'], prefix='type')
temp = pd.concat([user_all_before28_cate8_action[['user_id','cate']], df], axis=1)
df=temp.groupby(['user_id','cate']).sum().reset_index()
def user_cate8_type1_rate_all(df):
    return df[df.cate==8].type_1.sum()*1.0/(df.type_1.sum()+0.0001)
temp=df.groupby('user_id')[['cate','type_1']].apply(user_cate8_type1_rate_all).reset_index()
temp.columns=['user_id','user_cate8_type1_rate_all_before28']
train=pd.merge(train,temp,on='user_id',how='left')

def user_cate8_type2_rate_all(df):
    return df[df.cate==8].type_2.sum()*1.0/(df.type_2.sum()+0.0001)
temp=df.groupby('user_id')[['cate','type_2']].apply(user_cate8_type2_rate_all).reset_index()
temp.columns=['user_id','user_cate8_type2_rate_all_before28']
train=pd.merge(train,temp,on='user_id',how='left')

def user_cate8_type3_rate_all(df):
    return df[df.cate==8].type_3.sum()*1.0/(df.type_3.sum()+0.0001)
temp=df.groupby('user_id')[['cate','type_3']].apply(user_cate8_type3_rate_all).reset_index()
temp.columns=['user_id','user_cate8_type3_rate_all_before28']
train=pd.merge(train,temp,on='user_id',how='left')

def user_cate8_type4_rate_all(df):
    return df[df.cate==8].type_4.sum()*1.0/(df.type_4.sum()+0.0001)
temp=df.groupby('user_id')[['cate','type_4']].apply(user_cate8_type4_rate_all).reset_index()
temp.columns=['user_id','user_cate8_type4_rate_all_before28']
train=pd.merge(train,temp,on='user_id',how='left')

def user_cate8_type5_rate_all(df):
    return df[df.cate==8].type_5.sum()*1.0/(df.type_5.sum()+0.0001)
temp=df.groupby('user_id')[['cate','type_5']].apply(user_cate8_type5_rate_all).reset_index()
temp.columns=['user_id','user_cate8_type5_rate_all_before28']
train=pd.merge(train,temp,on='user_id',how='left')

def user_cate8_type6_rate_all(df):
    return df[df.cate==8].type_6.sum()*1.0/(df.type_6.sum()+0.0001)
temp=df.groupby('user_id')[['cate','type_6']].apply(user_cate8_type6_rate_all).reset_index()
temp.columns=['user_id','user_cate8_type6_rate_all_before28']
train=pd.merge(train,temp,on='user_id',how='left')

##用户前21天cate8个行为总数，比值总行为数
user_all_before21_cate8_action=actionAll[actionAll.time_diff<=21][['user_id','type','cate']]
df = pd.get_dummies(user_all_before21_cate8_action['type'], prefix='type')
temp = pd.concat([user_all_before21_cate8_action[['user_id','cate']], df], axis=1)
df=temp.groupby(['user_id','cate']).sum().reset_index()
def user_cate8_type1_rate_all(df):
    return df[df.cate==8].type_1.sum()*1.0/(df.type_1.sum()+0.0001)
temp=df.groupby('user_id')[['cate','type_1']].apply(user_cate8_type1_rate_all).reset_index()
temp.columns=['user_id','user_cate8_type1_rate_all_before21']
train=pd.merge(train,temp,on='user_id',how='left')

def user_cate8_type2_rate_all(df):
    return df[df.cate==8].type_2.sum()*1.0/(df.type_2.sum()+0.0001)
temp=df.groupby('user_id')[['cate','type_2']].apply(user_cate8_type2_rate_all).reset_index()
temp.columns=['user_id','user_cate8_type2_rate_all_before21']
train=pd.merge(train,temp,on='user_id',how='left')

def user_cate8_type3_rate_all(df):
    return df[df.cate==8].type_3.sum()*1.0/(df.type_3.sum()+0.0001)
temp=df.groupby('user_id')[['cate','type_3']].apply(user_cate8_type3_rate_all).reset_index()
temp.columns=['user_id','user_cate8_type3_rate_all_before21']
train=pd.merge(train,temp,on='user_id',how='left')

def user_cate8_type4_rate_all(df):
    return df[df.cate==8].type_4.sum()*1.0/(df.type_4.sum()+0.0001)
temp=df.groupby('user_id')[['cate','type_4']].apply(user_cate8_type4_rate_all).reset_index()
temp.columns=['user_id','user_cate8_type4_rate_all_before21']
train=pd.merge(train,temp,on='user_id',how='left')

def user_cate8_type5_rate_all(df):
    return df[df.cate==8].type_5.sum()*1.0/(df.type_5.sum()+0.0001)
temp=df.groupby('user_id')[['cate','type_5']].apply(user_cate8_type5_rate_all).reset_index()
temp.columns=['user_id','user_cate8_type5_rate_all_before21']
train=pd.merge(train,temp,on='user_id',how='left')

def user_cate8_type6_rate_all(df):
    return df[df.cate==8].type_6.sum()*1.0/(df.type_6.sum()+0.0001)
temp=df.groupby('user_id')[['cate','type_6']].apply(user_cate8_type6_rate_all).reset_index()
temp.columns=['user_id','user_cate8_type6_rate_all_before21']
train=pd.merge(train,temp,on='user_id',how='left')

#前15
user_all_before14_cate8_action=actionAll[actionAll.time_diff<=15][['user_id','type','cate']]

df = pd.get_dummies(user_all_before14_cate8_action['type'], prefix='type')
temp = pd.concat([user_all_before14_cate8_action[['user_id','cate']], df], axis=1)
df=temp.groupby(['user_id','cate']).sum().reset_index()
def user_cate8_type1_rate_all(df):
    return df[df.cate==8].type_1.sum()*1.0/(df.type_1.sum()+0.0001)
temp=df.groupby('user_id')[['cate','type_1']].apply(user_cate8_type1_rate_all).reset_index()
temp.columns=['user_id','user_cate8_type1_rate_all_before15']
train=pd.merge(train,temp,on='user_id',how='left')

def user_cate8_type2_rate_all(df):
    return df[df.cate==8].type_2.sum()*1.0/(df.type_2.sum()+0.0001)
temp=df.groupby('user_id')[['cate','type_2']].apply(user_cate8_type2_rate_all).reset_index()
temp.columns=['user_id','user_cate8_type2_rate_all_before15']
train=pd.merge(train,temp,on='user_id',how='left')

def user_cate8_type3_rate_all(df):
    return df[df.cate==8].type_3.sum()*1.0/(df.type_3.sum()+0.0001)
temp=df.groupby('user_id')[['cate','type_3']].apply(user_cate8_type3_rate_all).reset_index()
temp.columns=['user_id','user_cate8_type3_rate_all_before15']
train=pd.merge(train,temp,on='user_id',how='left')

def user_cate8_type4_rate_all(df):
    return df[df.cate==8].type_4.sum()*1.0/(df.type_4.sum()+0.0001)
temp=df.groupby('user_id')[['cate','type_4']].apply(user_cate8_type4_rate_all).reset_index()
temp.columns=['user_id','user_cate8_type4_rate_all_before15']
train=pd.merge(train,temp,on='user_id',how='left')

def user_cate8_type5_rate_all(df):
    return df[df.cate==8].type_5.sum()*1.0/(df.type_5.sum()+0.0001)
temp=df.groupby('user_id')[['cate','type_5']].apply(user_cate8_type5_rate_all).reset_index()
temp.columns=['user_id','user_cate8_type5_rate_all_before15']
train=pd.merge(train,temp,on='user_id',how='left')

def user_cate8_type6_rate_all(df):
    return df[df.cate==8].type_6.sum()*1.0/(df.type_6.sum()+0.0001)
temp=df.groupby('user_id')[['cate','type_6']].apply(user_cate8_type6_rate_all).reset_index()
temp.columns=['user_id','user_cate8_type6_rate_all_before15']
train=pd.merge(train,temp,on='user_id',how='left')

#前15
user_all_before14_cate8_action=actionAll[actionAll.time_diff<=10][['user_id','type','cate']]

df = pd.get_dummies(user_all_before14_cate8_action['type'], prefix='type')
temp = pd.concat([user_all_before14_cate8_action[['user_id','cate']], df], axis=1)
df=temp.groupby(['user_id','cate']).sum().reset_index()
def user_cate8_type1_rate_all(df):
    return df[df.cate==8].type_1.sum()*1.0/(df.type_1.sum()+0.0001)
temp=df.groupby('user_id')[['cate','type_1']].apply(user_cate8_type1_rate_all).reset_index()
temp.columns=['user_id','user_cate8_type1_rate_all_before10']
train=pd.merge(train,temp,on='user_id',how='left')

def user_cate8_type2_rate_all(df):
    return df[df.cate==8].type_2.sum()*1.0/(df.type_2.sum()+0.0001)
temp=df.groupby('user_id')[['cate','type_2']].apply(user_cate8_type2_rate_all).reset_index()
temp.columns=['user_id','user_cate8_type2_rate_all_before10']
train=pd.merge(train,temp,on='user_id',how='left')

def user_cate8_type3_rate_all(df):
    return df[df.cate==8].type_3.sum()*1.0/(df.type_3.sum()+0.0001)
temp=df.groupby('user_id')[['cate','type_3']].apply(user_cate8_type3_rate_all).reset_index()
temp.columns=['user_id','user_cate8_type3_rate_all_before10']
train=pd.merge(train,temp,on='user_id',how='left')

def user_cate8_type4_rate_all(df):
    return df[df.cate==8].type_4.sum()*1.0/(df.type_4.sum()+0.0001)
temp=df.groupby('user_id')[['cate','type_4']].apply(user_cate8_type4_rate_all).reset_index()
temp.columns=['user_id','user_cate8_type4_rate_all_before10']
train=pd.merge(train,temp,on='user_id',how='left')

def user_cate8_type5_rate_all(df):
    return df[df.cate==8].type_5.sum()*1.0/(df.type_5.sum()+0.0001)
temp=df.groupby('user_id')[['cate','type_5']].apply(user_cate8_type5_rate_all).reset_index()
temp.columns=['user_id','user_cate8_type5_rate_all_before10']
train=pd.merge(train,temp,on='user_id',how='left')

def user_cate8_type6_rate_all(df):
    return df[df.cate==8].type_6.sum()*1.0/(df.type_6.sum()+0.0001)
temp=df.groupby('user_id')[['cate','type_6']].apply(user_cate8_type6_rate_all).reset_index()
temp.columns=['user_id','user_cate8_type6_rate_all_before10']
train=pd.merge(train,temp,on='user_id',how='left')

#前7
user_all_before7_cate8_action=actionAll[actionAll.time_diff<=7][['user_id','type','cate']]
df = pd.get_dummies(user_all_before7_cate8_action['type'], prefix='type')
temp = pd.concat([user_all_before7_cate8_action[['user_id','cate']], df], axis=1)
df=temp.groupby(['user_id','cate']).sum().reset_index()
def user_cate8_type1_rate_all(df):
    return df[df.cate==8].type_1.sum()*1.0/(df.type_1.sum()+0.0001)
temp=df.groupby('user_id')[['cate','type_1']].apply(user_cate8_type1_rate_all).reset_index()
temp.columns=['user_id','user_cate8_type1_rate_all_before7']
train=pd.merge(train,temp,on='user_id',how='left')

def user_cate8_type2_rate_all(df):
    return df[df.cate==8].type_2.sum()*1.0/(df.type_2.sum()+0.0001)
temp=df.groupby('user_id')[['cate','type_2']].apply(user_cate8_type2_rate_all).reset_index()
temp.columns=['user_id','user_cate8_type2_rate_all_before7']
train=pd.merge(train,temp,on='user_id',how='left')

def user_cate8_type3_rate_all(df):
    return df[df.cate==8].type_3.sum()*1.0/(df.type_3.sum()+0.0001)
temp=df.groupby('user_id')[['cate','type_3']].apply(user_cate8_type3_rate_all).reset_index()
temp.columns=['user_id','user_cate8_type3_rate_all_before7']
train=pd.merge(train,temp,on='user_id',how='left')

def user_cate8_type4_rate_all(df):
    return df[df.cate==8].type_4.sum()*1.0/(df.type_4.sum()+0.0001)
temp=df.groupby('user_id')[['cate','type_4']].apply(user_cate8_type4_rate_all).reset_index()
temp.columns=['user_id','user_cate8_type4_rate_all_before7']
train=pd.merge(train,temp,on='user_id',how='left')

def user_cate8_type5_rate_all(df):
    return df[df.cate==8].type_5.sum()*1.0/(df.type_5.sum()+0.0001)
temp=df.groupby('user_id')[['cate','type_5']].apply(user_cate8_type5_rate_all).reset_index()
temp.columns=['user_id','user_cate8_type5_rate_all_before7']
train=pd.merge(train,temp,on='user_id',how='left')

def user_cate8_type6_rate_all(df):
    return df[df.cate==8].type_6.sum()*1.0/(df.type_6.sum()+0.0001)
temp=df.groupby('user_id')[['cate','type_6']].apply(user_cate8_type6_rate_all).reset_index()
temp.columns=['user_id','user_cate8_type6_rate_all_before7']
train=pd.merge(train,temp,on='user_id',how='left')


#按时段划分，有行为的天数
def have_action_days(df):
    return len(df.unique())
user_all_action_days=actionAll[['user_id','type','cate','time_diff']]
temp=user_all_action_days.groupby('user_id')['time_diff'].apply(have_action_days).reset_index()
temp.columns=['user_id','all_user_action_days']
train=pd.merge(train,temp,on='user_id',how='left')

# temp_action=actionAll[actionAll.time_diff<=61][['user_id','type','cate','time_diff']]
# temp=temp_action.groupby('user_id')['time_diff'].apply(have_action_days).reset_index()
# temp.columns=['user_id','all_user_before61_action_days']
# train=pd.merge(train,temp,on='user_id',how='left')
#
# temp_action=actionAll[actionAll.time_diff<=56][['user_id','type','cate','time_diff']]
# temp=temp_action.groupby('user_id')['time_diff'].apply(have_action_days).reset_index()
# temp.columns=['user_id','all_user_before56_action_days']
# train=pd.merge(train,temp,on='user_id',how='left')
#
# temp_action=actionAll[actionAll.time_diff<=49][['user_id','type','cate','time_diff']]
# temp=temp_action.groupby('user_id')['time_diff'].apply(have_action_days).reset_index()
# temp.columns=['user_id','all_user_before49_action_days']
# train=pd.merge(train,temp,on='user_id',how='left')

temp_action=actionAll[actionAll.time_diff<=42][['user_id','type','cate','time_diff']]
temp=temp_action.groupby('user_id')['time_diff'].apply(have_action_days).reset_index()
temp.columns=['user_id','all_user_before42_action_days']
train=pd.merge(train,temp,on='user_id',how='left')

temp_action=actionAll[actionAll.time_diff<=35][['user_id','type','cate','time_diff']]
temp=temp_action.groupby('user_id')['time_diff'].apply(have_action_days).reset_index()
temp.columns=['user_id','all_user_before35_action_days']
train=pd.merge(train,temp,on='user_id',how='left')

user_all_before21_action_days=actionAll[actionAll.time_diff<=21][['user_id','type','cate','time_diff']]
temp=user_all_before21_action_days.groupby('user_id')['time_diff'].apply(have_action_days).reset_index()
temp.columns=['user_id','all_user_before21_action_days']
train=pd.merge(train,temp,on='user_id',how='left')

user_all_before14_action_days=actionAll[actionAll.time_diff<=15][['user_id','type','cate','time_diff']]
temp=user_all_before14_action_days.groupby('user_id')['time_diff'].apply(have_action_days).reset_index()
temp.columns=['user_id','all_user_before15_action_days']
train=pd.merge(train,temp,on='user_id',how='left')

user_all_before10_action_days=actionAll[actionAll.time_diff<=10][['user_id','type','cate','time_diff']]
temp=user_all_before10_action_days.groupby('user_id')['time_diff'].apply(have_action_days).reset_index()
temp.columns=['user_id','all_user_before10_action_days']
train=pd.merge(train,temp,on='user_id',how='left')

user_all_before7_action_days=actionAll[actionAll.time_diff<=7][['user_id','type','cate','time_diff']]
temp=user_all_before7_action_days.groupby('user_id')['time_diff'].apply(have_action_days).reset_index()
temp.columns=['user_id','all_user_before7_action_days']
train=pd.merge(train,temp,on='user_id',how='left')

#cate8行为天数/总行为天数
def user_cate8_action_days_rate_all(df):
    return len(df[df.cate==8].time_diff.unique())*1.0/(len(df.time_diff.unique())+0.0001)
user_all_action_days=actionAll[['user_id','type','cate','time_diff']]
temp=user_all_action_days.groupby('user_id')['cate','time_diff'].apply(user_cate8_action_days_rate_all).reset_index()
temp.columns=['user_id','user_cate8_action_days_rate_all']
train=pd.merge(train,temp,on='user_id',how='left')

# temp_action=actionAll[actionAll.time_diff<=61][['user_id','type','cate','time_diff']]
# temp=temp_action.groupby('user_id')['cate','time_diff'].apply(user_cate8_action_days_rate_all).reset_index()
# temp.columns=['user_id','user_cate8_before61_action_days_rate_all']
# train=pd.merge(train,temp,on='user_id',how='left')
#
# temp_action=actionAll[actionAll.time_diff<=56][['user_id','type','cate','time_diff']]
# temp=temp_action.groupby('user_id')['cate','time_diff'].apply(user_cate8_action_days_rate_all).reset_index()
# temp.columns=['user_id','user_cate8_before56_action_days_rate_all']
# train=pd.merge(train,temp,on='user_id',how='left')
#
# temp_action=actionAll[actionAll.time_diff<=49][['user_id','type','cate','time_diff']]
# temp=temp_action.groupby('user_id')['cate','time_diff'].apply(user_cate8_action_days_rate_all).reset_index()
# temp.columns=['user_id','user_cate8_before49_action_days_rate_all']
# train=pd.merge(train,temp,on='user_id',how='left')

temp_action=actionAll[actionAll.time_diff<=42][['user_id','type','cate','time_diff']]
temp=temp_action.groupby('user_id')['cate','time_diff'].apply(user_cate8_action_days_rate_all).reset_index()
temp.columns=['user_id','user_cate8_before42_action_days_rate_all']
train=pd.merge(train,temp,on='user_id',how='left')

temp_action=actionAll[actionAll.time_diff<=35][['user_id','type','cate','time_diff']]
temp=temp_action.groupby('user_id')['cate','time_diff'].apply(user_cate8_action_days_rate_all).reset_index()
temp.columns=['user_id','user_cate8_before35_action_days_rate_all']
train=pd.merge(train,temp,on='user_id',how='left')

user_all_before21_action_days=actionAll[actionAll.time_diff<=21][['user_id','type','cate','time_diff']]
temp=user_all_before21_action_days.groupby('user_id')['cate','time_diff'].apply(user_cate8_action_days_rate_all).reset_index()
temp.columns=['user_id','user_cate8_before21_action_days_rate_all']
train=pd.merge(train,temp,on='user_id',how='left')

user_all_before15_action_days=actionAll[actionAll.time_diff<=15][['user_id','type','cate','time_diff']]
temp=user_all_before15_action_days.groupby('user_id')['cate','time_diff'].apply(user_cate8_action_days_rate_all).reset_index()
temp.columns=['user_id','user_cate8_before15_action_days_rate_all']
train=pd.merge(train,temp,on='user_id',how='left')

user_all_before10_action_days=actionAll[actionAll.time_diff<=10][['user_id','type','cate','time_diff']]
temp=user_all_before10_action_days.groupby('user_id')['cate','time_diff'].apply(user_cate8_action_days_rate_all).reset_index()
temp.columns=['user_id','user_cate8_before10_action_days_rate_all']
train=pd.merge(train,temp,on='user_id',how='left')

user_all_before7_action_days=actionAll[actionAll.time_diff<=7][['user_id','type','cate','time_diff']]
temp=user_all_before7_action_days.groupby('user_id')['cate','time_diff'].apply(user_cate8_action_days_rate_all).reset_index()
temp.columns=['user_id','user_cate8_before7_action_days_rate_all']
train=pd.merge(train,temp,on='user_id',how='left')


#用户购买行为天数/总行为天数
def user_buy_action_days_rate_all(df):
    return len(df[df.type==4].time_diff.unique())*1.0/(len(df.time_diff.unique())+0.0001)
user_buy_action_days=actionAll[['user_id','type','time_diff']]
temp=user_buy_action_days.groupby('user_id')['type','time_diff'].apply(user_buy_action_days_rate_all).reset_index()
temp.columns=['user_id','user_buy_action_days_rate_all']
train=pd.merge(train,temp,on='user_id',how='left')

# temp_action=actionAll[actionAll.time_diff<=61][['user_id','type','time_diff']]
# temp=temp_action.groupby('user_id')['type','time_diff'].apply(user_buy_action_days_rate_all).reset_index()
# temp.columns=['user_id','user_before61_buy_action_days_rate']
# train=pd.merge(train,temp,on='user_id',how='left')
#
# temp_action=actionAll[actionAll.time_diff<=56][['user_id','type','time_diff']]
# temp=temp_action.groupby('user_id')['type','time_diff'].apply(user_buy_action_days_rate_all).reset_index()
# temp.columns=['user_id','user_before56_buy_action_days_rate']
# train=pd.merge(train,temp,on='user_id',how='left')
#
# temp_action=actionAll[actionAll.time_diff<=49][['user_id','type','time_diff']]
# temp=temp_action.groupby('user_id')['type','time_diff'].apply(user_buy_action_days_rate_all).reset_index()
# temp.columns=['user_id','user_before49_buy_action_days_rate']
# train=pd.merge(train,temp,on='user_id',how='left')

temp_action=actionAll[actionAll.time_diff<=42][['user_id','type','time_diff']]
temp=temp_action.groupby('user_id')['type','time_diff'].apply(user_buy_action_days_rate_all).reset_index()
temp.columns=['user_id','user_before42_buy_action_days_rate']
train=pd.merge(train,temp,on='user_id',how='left')

temp_action=actionAll[actionAll.time_diff<=35][['user_id','type','time_diff']]
temp=temp_action.groupby('user_id')['type','time_diff'].apply(user_buy_action_days_rate_all).reset_index()
temp.columns=['user_id','user_before35_buy_action_days_rate']
train=pd.merge(train,temp,on='user_id',how='left')

user_before21_buy_action_days=actionAll[actionAll.time_diff<=21][['user_id','type','time_diff']]
temp=user_before21_buy_action_days.groupby('user_id')['type','time_diff'].apply(user_buy_action_days_rate_all).reset_index()
temp.columns=['user_id','user_before21_buy_action_days_rate']
train=pd.merge(train,temp,on='user_id',how='left')

user_before15_buy_action_days=actionAll[actionAll.time_diff<=15][['user_id','type','time_diff']]
temp=user_before15_buy_action_days.groupby('user_id')['type','time_diff'].apply(user_buy_action_days_rate_all).reset_index()
temp.columns=['user_id','user_before15_buy_action_days_rate']
train=pd.merge(train,temp,on='user_id',how='left')

user_before10_buy_action_days=actionAll[actionAll.time_diff<=10][['user_id','type','time_diff']]
temp=user_before10_buy_action_days.groupby('user_id')['type','time_diff'].apply(user_buy_action_days_rate_all).reset_index()
temp.columns=['user_id','user_before10_buy_action_days_rate']
train=pd.merge(train,temp,on='user_id',how='left')

user_before7_buy_action_days=actionAll[actionAll.time_diff<=7][['user_id','type','time_diff']]
temp=user_before7_buy_action_days.groupby('user_id')['type','time_diff'].apply(user_buy_action_days_rate_all).reset_index()
temp.columns=['user_id','user_before7_buy_action_days_rate']
train=pd.merge(train,temp,on='user_id',how='left')

#用户平均登录时间间隔
user_buy_action_days=actionAll[['user_id','type','time_diff']]
def user_action_days_diff_max(df):
    return pd.Series(df.unique()).sort_values().diff(1).max()
temp=user_buy_action_days.groupby('user_id')['time_diff'].apply(user_action_days_diff_max).reset_index()
temp.columns=['user_id','user_action_days_diff_max']
train=pd.merge(train,temp,on='user_id',how='left')

def user_action_days_diff_min(df):
    return pd.Series(df.unique()).sort_values().diff(1).min()
temp=user_buy_action_days.groupby('user_id')['time_diff'].apply(user_action_days_diff_min).reset_index()
temp.columns=['user_id','user_action_days_diff_min']
train=pd.merge(train,temp,on='user_id',how='left')

def user_action_days_diff_mean(df):
    return pd.Series(df.unique()).sort_values().diff(1).mean()
temp=user_buy_action_days.groupby('user_id')['time_diff'].apply(user_action_days_diff_mean).reset_index()
temp.columns=['user_id','user_action_days_diff_mean']
train=pd.merge(train,temp,on='user_id',how='left')

def user_action_days_diff_std(df):
    return pd.Series(df.unique()).sort_values().diff(1).std()
temp=user_buy_action_days.groupby('user_id')['time_diff'].apply(user_action_days_diff_std).reset_index()
temp.columns=['user_id','user_action_days_diff_std']
train=pd.merge(train,temp,on='user_id',how='left')

# temp_action=actionAll[actionAll.time_diff<=61][['user_id','type','time_diff']]
# temp=temp_action.groupby('user_id')['time_diff'].apply(user_action_days_diff_max).reset_index()
# temp.columns=['user_id','user_before61_action_days_diff_max']
# train=pd.merge(train,temp,on='user_id',how='left')
#
# temp=user_buy_action_days.groupby('user_id')['time_diff'].apply(user_action_days_diff_min).reset_index()
# temp.columns=['user_id','user_before61_action_days_diff_min']
# train=pd.merge(train,temp,on='user_id',how='left')
#
# temp=user_buy_action_days.groupby('user_id')['time_diff'].apply(user_action_days_diff_mean).reset_index()
# temp.columns=['user_id','user_before61_action_days_diff_mean']
# train=pd.merge(train,temp,on='user_id',how='left')
#
# temp=user_buy_action_days.groupby('user_id')['time_diff'].apply(user_action_days_diff_std).reset_index()
# temp.columns=['user_id','user_before61_action_days_diff_std']
# train=pd.merge(train,temp,on='user_id',how='left')
#
#
# temp_action=actionAll[actionAll.time_diff<=56][['user_id','type','time_diff']]
# temp=temp_action.groupby('user_id')['time_diff'].apply(user_action_days_diff_max).reset_index()
# temp.columns=['user_id','user_before56_action_days_diff_max']
# train=pd.merge(train,temp,on='user_id',how='left')
#
# temp=user_buy_action_days.groupby('user_id')['time_diff'].apply(user_action_days_diff_min).reset_index()
# temp.columns=['user_id','user_before56_action_days_diff_min']
# train=pd.merge(train,temp,on='user_id',how='left')
#
# temp=user_buy_action_days.groupby('user_id')['time_diff'].apply(user_action_days_diff_mean).reset_index()
# temp.columns=['user_id','user_before56_action_days_diff_mean']
# train=pd.merge(train,temp,on='user_id',how='left')
#
# temp=user_buy_action_days.groupby('user_id')['time_diff'].apply(user_action_days_diff_std).reset_index()
# temp.columns=['user_id','user_before56_action_days_diff_std']
# train=pd.merge(train,temp,on='user_id',how='left')
#
# temp_action=actionAll[actionAll.time_diff<=49][['user_id','type','time_diff']]
# temp=temp_action.groupby('user_id')['time_diff'].apply(user_action_days_diff_max).reset_index()
# temp.columns=['user_id','user_before49_action_days_diff_max']
# train=pd.merge(train,temp,on='user_id',how='left')
#
# temp=user_buy_action_days.groupby('user_id')['time_diff'].apply(user_action_days_diff_min).reset_index()
# temp.columns=['user_id','user_before49_action_days_diff_min']
# train=pd.merge(train,temp,on='user_id',how='left')
#
# temp=user_buy_action_days.groupby('user_id')['time_diff'].apply(user_action_days_diff_mean).reset_index()
# temp.columns=['user_id','user_before49_action_days_diff_mean']
# train=pd.merge(train,temp,on='user_id',how='left')
#
# temp=user_buy_action_days.groupby('user_id')['time_diff'].apply(user_action_days_diff_std).reset_index()
# temp.columns=['user_id','user_before49_action_days_diff_std']
# train=pd.merge(train,temp,on='user_id',how='left')


temp_action=actionAll[actionAll.time_diff<=42][['user_id','type','time_diff']]
temp=temp_action.groupby('user_id')['time_diff'].apply(user_action_days_diff_max).reset_index()
temp.columns=['user_id','user_before42_action_days_diff_max']
train=pd.merge(train,temp,on='user_id',how='left')

temp=user_buy_action_days.groupby('user_id')['time_diff'].apply(user_action_days_diff_min).reset_index()
temp.columns=['user_id','user_before42_action_days_diff_min']
train=pd.merge(train,temp,on='user_id',how='left')

temp=user_buy_action_days.groupby('user_id')['time_diff'].apply(user_action_days_diff_mean).reset_index()
temp.columns=['user_id','user_before42_action_days_diff_mean']
train=pd.merge(train,temp,on='user_id',how='left')

temp=user_buy_action_days.groupby('user_id')['time_diff'].apply(user_action_days_diff_std).reset_index()
temp.columns=['user_id','user_before42_action_days_diff_std']
train=pd.merge(train,temp,on='user_id',how='left')


temp_action=actionAll[actionAll.time_diff<=35][['user_id','type','time_diff']]
temp=temp_action.groupby('user_id')['time_diff'].apply(user_action_days_diff_max).reset_index()
temp.columns=['user_id','user_before35_action_days_diff_max']
train=pd.merge(train,temp,on='user_id',how='left')

temp=user_buy_action_days.groupby('user_id')['time_diff'].apply(user_action_days_diff_min).reset_index()
temp.columns=['user_id','user_before35_action_days_diff_min']
train=pd.merge(train,temp,on='user_id',how='left')

temp=user_buy_action_days.groupby('user_id')['time_diff'].apply(user_action_days_diff_mean).reset_index()
temp.columns=['user_id','user_before35_action_days_diff_mean']
train=pd.merge(train,temp,on='user_id',how='left')

temp=user_buy_action_days.groupby('user_id')['time_diff'].apply(user_action_days_diff_std).reset_index()
temp.columns=['user_id','user_before35_action_days_diff_std']
train=pd.merge(train,temp,on='user_id',how='left')

user_buy_action_days=actionAll[actionAll.time_diff<=21][['user_id','type','time_diff']]
temp=user_buy_action_days.groupby('user_id')['time_diff'].apply(user_action_days_diff_max).reset_index()
temp.columns=['user_id','user_before21_action_days_diff_max']
train=pd.merge(train,temp,on='user_id',how='left')

temp=user_buy_action_days.groupby('user_id')['time_diff'].apply(user_action_days_diff_min).reset_index()
temp.columns=['user_id','user_before21_action_days_diff_min']
train=pd.merge(train,temp,on='user_id',how='left')

temp=user_buy_action_days.groupby('user_id')['time_diff'].apply(user_action_days_diff_mean).reset_index()
temp.columns=['user_id','user_before21_action_days_diff_mean']
train=pd.merge(train,temp,on='user_id',how='left')

temp=user_buy_action_days.groupby('user_id')['time_diff'].apply(user_action_days_diff_std).reset_index()
temp.columns=['user_id','user_before21_action_days_diff_std']
train=pd.merge(train,temp,on='user_id',how='left')

user_buy_action_days=actionAll[actionAll.time_diff<=14][['user_id','type','time_diff']]
temp=user_buy_action_days.groupby('user_id')['time_diff'].apply(user_action_days_diff_max).reset_index()
temp.columns=['user_id','user_before14_action_days_diff_max']
train=pd.merge(train,temp,on='user_id',how='left')

temp=user_buy_action_days.groupby('user_id')['time_diff'].apply(user_action_days_diff_min).reset_index()
temp.columns=['user_id','user_before14_action_days_diff_min']
train=pd.merge(train,temp,on='user_id',how='left')

temp=user_buy_action_days.groupby('user_id')['time_diff'].apply(user_action_days_diff_mean).reset_index()
temp.columns=['user_id','user_before14_action_days_diff_mean']
train=pd.merge(train,temp,on='user_id',how='left')

temp=user_buy_action_days.groupby('user_id')['time_diff'].apply(user_action_days_diff_std).reset_index()
temp.columns=['user_id','user_before14_action_days_diff_std']
train=pd.merge(train,temp,on='user_id',how='left')

user_buy_action_days=actionAll[actionAll.time_diff<=10][['user_id','type','time_diff']]
temp=user_buy_action_days.groupby('user_id')['time_diff'].apply(user_action_days_diff_max).reset_index()
temp.columns=['user_id','user_before10_action_days_diff_max']
train=pd.merge(train,temp,on='user_id',how='left')

temp=user_buy_action_days.groupby('user_id')['time_diff'].apply(user_action_days_diff_min).reset_index()
temp.columns=['user_id','user_before10_action_days_diff_min']
train=pd.merge(train,temp,on='user_id',how='left')

temp=user_buy_action_days.groupby('user_id')['time_diff'].apply(user_action_days_diff_mean).reset_index()
temp.columns=['user_id','user_before10_action_days_diff_mean']
train=pd.merge(train,temp,on='user_id',how='left')

temp=user_buy_action_days.groupby('user_id')['time_diff'].apply(user_action_days_diff_std).reset_index()
temp.columns=['user_id','user_before10_action_days_diff_std']
train=pd.merge(train,temp,on='user_id',how='left')

user_buy_action_days=actionAll[actionAll.time_diff<=7][['user_id','type','time_diff']]
temp=user_buy_action_days.groupby('user_id')['time_diff'].apply(user_action_days_diff_max).reset_index()
temp.columns=['user_id','user_before7_action_days_diff_max']
train=pd.merge(train,temp,on='user_id',how='left')

temp=user_buy_action_days.groupby('user_id')['time_diff'].apply(user_action_days_diff_min).reset_index()
temp.columns=['user_id','user_before7_action_days_diff_min']
train=pd.merge(train,temp,on='user_id',how='left')

temp=user_buy_action_days.groupby('user_id')['time_diff'].apply(user_action_days_diff_mean).reset_index()
temp.columns=['user_id','user_before7_action_days_diff_mean']
train=pd.merge(train,temp,on='user_id',how='left')

temp=user_buy_action_days.groupby('user_id')['time_diff'].apply(user_action_days_diff_std).reset_index()
temp.columns=['user_id','user_before7_action_days_diff_std']
train=pd.merge(train,temp,on='user_id',how='left')
#用户两次购买时间差的max。min。mean。std
temp=user_buy_action_days[user_buy_action_days.type==4].groupby('user_id')['time_diff'].apply(user_action_days_diff_max).reset_index()
temp.columns=['user_id','user_two_buy_days_diff_max']
train=pd.merge(train,temp,on='user_id',how='left')

temp=user_buy_action_days[user_buy_action_days.type==4].groupby('user_id')['time_diff'].apply(user_action_days_diff_min).reset_index()
temp.columns=['user_id','user_two_buy_days_diff_min']
train=pd.merge(train,temp,on='user_id',how='left')

temp=user_buy_action_days[user_buy_action_days.type==4].groupby('user_id')['time_diff'].apply(user_action_days_diff_mean).reset_index()
temp.columns=['user_id','user_two_buy_days_diff_mean']
train=pd.merge(train,temp,on='user_id',how='left')

temp=user_buy_action_days[user_buy_action_days.type==4].groupby('user_id')['time_diff'].apply(user_action_days_diff_std).reset_index()
temp.columns=['user_id','user_two_buy_days_diff_std']
train=pd.merge(train,temp,on='user_id',how='left')

train.fillna(0,inplace=True)
train.to_csv('./sub/train_all_cate_action_feature_15.csv',index=False)
