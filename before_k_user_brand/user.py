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
all_data_end_week=8
all_data_start_week=1
history_data_end_week=7
history_data_start_week=1
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


#时间特征
#diff_reg
user_data=pd.read_csv('D:/Competition/JD/Jdata/JData_User.csv')
user_data['user_reg_tm']=pd.to_datetime(user_data['user_reg_tm'],format='%Y/%m/%d')
user_data.dropna(inplace=True)
user_data['diff_reg']=[-int(i.days) for i in (user_data['user_reg_tm']-(end_day))]
train=pd.merge(train,user_data[['user_id','diff_reg']],on='user_id',how='left')
#diff_last_action  用户在训练集内    最后一次行为  离 起点 时长
action_user_train=action_user[(action_user.date>=(end_day-timedelta(window_len))) & (action_user.date<=(end_day-timedelta(1)))]
action_user_train['total_secends']=[ -int(i.total_seconds())/3600.0 for i in (action_user_train.time-end_day)]
diff_last_action=action_user_train.groupby('user_id')['total_secends'].min().reset_index()
diff_last_action.columns=['user_id','diff_last_action']
train=pd.merge(train,diff_last_action,on='user_id',how='left')
#用户在训练集内    最后一次各种行为   离起点的时长
last_type=pd.DataFrame(train['user_id'])
for i in (1,2,3,4,5,6):
    diff_last_type = action_user_train[action_user_train.type == i].groupby('user_id')['total_secends'].min().reset_index()
    diff_last_type.columns = ['user_id', 'diff_last_type%s'%i]
    last_type=pd.merge(last_type, diff_last_type, on='user_id', how='left')
#用-1填充缺失值
last_type.fillna(-1,inplace=True)
train = pd.merge(train, last_type, on='user_id', how='left')
#用户在T   倒数第二次下单  离 起点 时长
def diff_2nd_last_type4(df):
    if len(df)>1:
        df=pd.Series(df)
        x=df.sort_values()
        x=x.values
        return x[1]
    else:
        return -1
diff_2nd_last_type4 = action_user_train[action_user_train.type == 4].groupby('user_id')['total_secends'].apply(diff_2nd_last_type4).reset_index()
diff_2nd_last_type4.columns=['user_id','diff_2nd_last_type4']
train = pd.merge(train, diff_2nd_last_type4, on='user_id', how='left')
train.diff_2nd_last_type4.fillna(-1,inplace=True)
#用户在T    活跃度
def dif_days(df):
    return len(df.unique())
train_days_action=action_user_train.groupby('user_id')['date'].apply(dif_days).reset_index()
train_days_action.columns=['user_id','train_days_action']
train=pd.merge(train,train_days_action,on='user_id',how='left')
train_days=train[['user_id']]
for i in (1,2,3,4,5,6):
    train_days_type=action_user_train[action_user_train.type==i].groupby('user_id')['date'].apply(dif_days).reset_index()
    train_days_type.columns=['user_id','train_days_type%s'%i]
    train_days=pd.merge(train_days,train_days_type,on='user_id',how='left')
train_days.fillna(0,inplace=True)
train=pd.merge(train,train_days,on='user_id',how='left')
#用户在T          最近两天是否活跃，任意一天活跃算活跃
def flag_last2days_action(df):
    df=[i.date() for i in df]
    if ((end_day-timedelta(1)).date() in df) | ((end_day-timedelta(2)).date() in df):
        return 1
    else:
        return 0
train_flag_last2days_action=action_user_train.groupby('user_id')['date'].apply(flag_last2days_action).reset_index()
train_flag_last2days_action.columns=['user_id','train_flag_last2days_action']
train=pd.merge(train,train_flag_last2days_action,on='user_id',how='left')

#用户在T          最近两天是否活跃，任意一天活跃算活跃
def flag_last1days_action(df):
    df=[i.date() for i in df]
    if ((end_day-timedelta(1)).date() in df) :
        return 1
    else:
        return 0
train_flag_last1days_action=action_user_train.groupby('user_id')['date'].apply(flag_last1days_action).reset_index()
train_flag_last1days_action.columns=['user_id','train_flag_last1days_action']
train=pd.merge(train,train_flag_last1days_action,on='user_id',how='left')

#该用户第j周      周六-周三       各种行为次数/ 第j周总该行为次数  j = 1, 2, 3, 4, 5, 6,             7, 8  9,                               10
def compute_week(df):
    if (df>=datetime(2016,2,6)) &(df<=datetime(2016,2,12)):
        return 1
    if (df>=datetime(2016,2,13)) &(df<=datetime(2016,2,19)):
        return 2
    if (df>=datetime(2016,2,20)) &(df<=datetime(2016,2,26)):
        return 3
    if (df>=datetime(2016,2,27)) &(df<=datetime(2016,3,4)):
        return 4
    if (df>=datetime(2016,3,5)) &(df<=datetime(2016,3,11)):
        return 5
    if (df>=datetime(2016,3,19)) &(df<=datetime(2016,3,25)):
        return 6
    if (df>=datetime(2016,3,26)) &(df<=datetime(2016,4,1)):
        return 7
    if (df>=datetime(2016,4,2)) &(df<=datetime(2016,4,8)):
        return 8
    if (df>=datetime(2016,4,9)) &(df<=datetime(2016,4,15)):
        return 9
    else:
        return -1
action8['week_num']=action8.date.apply(compute_week)
action8['week_day']=[i.isoweekday() for i in action8['date']]
def between_sw(df):
    if (df>=3) & (df<=6):
        return 1
    else:
        return 0
action8['between_sw']=[between_sw(i) for i in action8['week_day']]
sw_ratio_type=pd.DataFrame(train['user_id'])
def between_sw_ratio_type(df):
    return len(df[df.week_day>=3][df.week_day<=6])*1.0/len(df)
for j in range(1,all_data_end_week+1):
    for i in (1,2,3,4,5,6):#
        rate=action8[action8.week_num==j][action8.type==i].groupby('user_id').apply(between_sw_ratio_type).reset_index()
        rate.columns=['user_id','the_%s_sw_ratio_type%s'%(j,i)]
        sw_ratio_type=pd.merge(sw_ratio_type,rate,on='user_id',how='left')
sw_ratio_type.fillna(-1,inplace=True)
train=pd.merge(train,sw_ratio_type,on='user_id',how='left')
#该用户   H  是否行为过 cate8
h_action8_data=action8[(action8.week_num>=history_data_start_week) &(action8.week_num<=history_data_end_week)]
end5_user_h_action8=pd.merge(train[['user_id']],h_action8_data,on='user_id',how='left')
def is_type_action(df):
#     print df
    if len(df.values)>0:
        return 1
    else:
        return 0
h_has_type=train[['user_id']]
for i in (1,2,3,4,5,6):
    is_type=end5_user_h_action8[end5_user_h_action8.type==i].groupby('user_id')['type'].apply(is_type_action).reset_index()
    is_type.columns=['user_id','h_flag_8_type%s'%i]
    h_has_type=pd.merge(h_has_type,is_type,on='user_id',how='left')
h_has_type.fillna(0,inplace=True)
train=pd.merge(train,h_has_type,on='user_id',how='left')

#train用户在所有数据集中的购买次数统计
a_action8_data=action8[(action8.week_num>=all_data_start_week) &(action8.week_num<=all_data_end_week)]
end5_user_a_action8=pd.merge(train[['user_id']],a_action8_data,on='user_id',how='left')
def type4_count(df):
    count=0
    for i in range(len(df)):
        count=count+1
    return count
type4_count=end5_user_a_action8[end5_user_a_action8.type==4].groupby('user_id')['type'].apply(type4_count).reset_index()
type4_count.columns=['user_id','type4_count']
many_type4=type4_count[type4_count['type4_count']>=2]
#得到购买过两次以上的用户的行为数据
many_type4=pd.merge(many_type4[['user_id']],end5_user_a_action8,on='user_id',how='left')
#该用户  A   max（每两次下单时间）
def type4_max_diff(df):
    if len(df)>1:
        x=[]
        df=df.sort_values()
        df=df.values
        for i in range(len(df)-1):
            diff=(df[i+1]-df[i])
            x.append(diff)
        max_diff=np.max(x)
        return max_diff
    return -1
x=many_type4[many_type4.type==4].groupby('user_id')['time'].apply(type4_max_diff).reset_index()
x['time']=[int(i.total_seconds())/3600.0 for i in (x.time)]
x.columns=['user_id','a_diff_max_type4_next4']
train=pd.merge(train,x,on='user_id',how='left')
train.a_diff_max_type4_next4.fillna(-1,inplace=True)

#该用户  A   min（每两次下单时间）
def type4_min_diff(df):
    if len(df)>1:
        x=[]
        df=df.sort_values()
        df=df.values
        for i in range(len(df)-1):
            diff=(df[i+1]-df[i])
            x.append(diff)
        max_diff=np.min(x)
        return max_diff
    return -1
x=many_type4[many_type4.type==4].groupby('user_id')['time'].apply(type4_min_diff).reset_index()
x['time']=[int(i.total_seconds())/3600.0 for i in (x.time)]
x.columns=['user_id','a_diff_min_type4_next4']
train=pd.merge(train,x,on='user_id',how='left')
train.a_diff_min_type4_next4.fillna(-1,inplace=True)

#该用户  A   avg（每两次下单时间）
def type4_avg_diff(df):
    if len(df)>1:
        x=[]
        df=df.sort_values()
        df=df.values
        for i in range(len(df)-1):
            diff=(df[i+1]-df[i])
            x.append(diff)
        max_diff=np.mean(x)
        return max_diff
    return -1
x=many_type4[many_type4.type==4].groupby('user_id')['time'].apply(type4_avg_diff).reset_index()
x['time']=[int(i.total_seconds())/3600.0 for i in (x.time)]
x.columns=['user_id','a_diff_avg_type4_next4']
train=pd.merge(train,x,on='user_id',how='left')
train.a_diff_avg_type4_next4.fillna(-1,inplace=True)
#该用户  A   median（每两次下单时间）
def type4_median_diff(df):
    if len(df)>1:
        x=[]
        df=df.sort_values()
        df=df.values
        for i in range(len(df)-1):
            diff=(df[i+1]-df[i])
            x.append(diff)
        max_diff=np.median(x)
        return max_diff
    return -1
x=many_type4[many_type4.type==4].groupby('user_id')['time'].apply(type4_median_diff).reset_index()
x['time']=[int(i.total_seconds())/3600.0 for i in (x.time)]
x.columns=['user_id','a_diff_median_type4_next4']
train=pd.merge(train,x,on='user_id',how='left')
train.a_diff_median_type4_next4.fillna(-1,inplace=True)

#该用户    A  加购之后 k天之内购买次数/ 该用户加购购买总次数
#s删除未加购过的用户
cart_user_action=end5_user_a_action8[end5_user_a_action8.type==2]
cart_user_action=cart_user_action[['user_id']].drop_duplicates()
cart_user_action=pd.merge(cart_user_action,end5_user_a_action8,on='user_id',how='left')



#下过单的用户-商品对行为
buy_user_action=end5_user_a_action8[end5_user_a_action8.type==4]
buy_user_action=buy_user_action[['user_id','sku_id']].drop_duplicates()
buy_user_action=pd.merge(buy_user_action,end5_user_a_action8,on=['user_id','sku_id'],how='left')
buy_user_action['totals']=[int(i.total_seconds())/3600.0 for i in (buy_user_action['time']-datetime(2016,2,1))]

#该用户  A      max（浏览 - 下单） 时长
def type14_max_diff(df):
    if len(df[df.type==4])==1:
        df=df.sort_values('totals')
        type4_time=df[df.type==4].totals.values[0]
        if len(df[df.totals<type4_time][df.type==1].totals)>0:
            max_type1_time=np.min(df[df.totals<type4_time][df.type==1].totals.values)
            return type4_time-max_type1_time
        return -1
    if len(df[df.type==4])>1:
        x=[]
        df=df.sort_values('totals')
        for i in range(len(df[df.type==4])-1):
            type4_time1=df[df.type==4].totals.values[i]
            type4_time2=df[df.type==4].totals.values[i+1]
            if len(df[df.totals<type4_time1][df.totals>type4_time2][df.type==1].totals)>0:
                max_type1_time1=np.min(df[df.totals<type4_time1][df.totals>type4_time2][df.type==1].totals)
                diff=(type4_time1-max_type1_time1)
                x.append(diff)
        type4_time=df[df.type==4].totals.values[len(df[df.type==4])-1]
        if len(df[df.totals<type4_time][df.type==1].totals)>0:
            max_type1_time=np.min(df[df.totals<type4_time][df.type==1].totals.values)
            diff=(type4_time-max_type1_time)
            x.append(diff)
        if len(x)>0:
            max_diff=np.max(x)
            return max_diff
    return -1
type14_max_diff=buy_user_action.groupby(['user_id','sku_id']).apply(type14_max_diff).reset_index()
type14_max_diff.columns=['user_id','sku_id','type14_max_diff']
type14_user_max_diff=type14_max_diff.groupby('user_id')['type14_max_diff'].max().reset_index()
type14_user_max_diff.columns=['user_id','a_diff_max_type1_4']
train=pd.merge(train,type14_user_max_diff,on='user_id',how='left')
train.a_diff_max_type1_4.fillna(-1,inplace=True)

#该用户  A     max（加购 - 下单） 时长
def type24_max_diff(df):
    if len(df[df.type==4])==1:
        df=df.sort_values('totals')
        type4_time=df[df.type==4].totals.values[0]
        if len(df[df.totals<type4_time][df.type==2].totals)>0:
            max_type1_time=np.min(df[df.totals<type4_time][df.type==2].totals.values)
            return type4_time-max_type1_time
        return -1
    if len(df[df.type==4])>1:
        x=[]
        df=df.sort_values('totals')
        for i in range(len(df[df.type==4])-1):
            type4_time1=df[df.type==4].totals.values[i]
            type4_time2=df[df.type==4].totals.values[i+1]
            if len(df[df.totals<type4_time1][df.totals>type4_time2][df.type==2].totals)>0:
                max_type1_time1=np.min(df[df.totals<type4_time1][df.totals>type4_time2][df.type==2].totals)
                diff=(type4_time1-max_type1_time1)
                x.append(diff)
        type4_time=df[df.type==4].totals.values[len(df[df.type==4])-1]
        if len(df[df.totals<type4_time][df.type==2].totals)>0:
            max_type1_time=np.min(df[df.totals<type4_time][df.type==2].totals.values)
            diff=(type4_time-max_type1_time)
            x.append(diff)
        if len(x)>0:
            max_diff=np.max(x)
            return max_diff
    return -1
type24_max_diff=buy_user_action.groupby(['user_id','sku_id']).apply(type24_max_diff).reset_index()
type24_max_diff.columns=['user_id','sku_id','type24_max_diff']
type24_user_max_diff=type24_max_diff.groupby('user_id')['type24_max_diff'].max().reset_index()
type24_user_max_diff.columns=['user_id','a_diff_max_type2_4']
train=pd.merge(train,type24_user_max_diff,on='user_id',how='left')
train.a_diff_max_type2_4.fillna(-1,inplace=True)

#该用户  A     max（删购 - 下单） 时长
def type34_max_diff(df):
    if len(df[df.type==4])==1:
        df=df.sort_values('totals')
        type4_time=df[df.type==4].totals.values[0]
        if len(df[df.totals<type4_time][df.type==3].totals)>0:
            max_type1_time=np.min(df[df.totals<type4_time][df.type==3].totals.values)
            return type4_time-max_type1_time
        return -1
    if len(df[df.type==4])>1:
        x=[]
        df=df.sort_values('totals')
        for i in range(len(df[df.type==4])-1):
            type4_time1=df[df.type==4].totals.values[i]
            type4_time2=df[df.type==4].totals.values[i+1]
            if len(df[df.totals<type4_time1][df.totals>type4_time2][df.type==3].totals)>0:
                max_type1_time1=np.min(df[df.totals<type4_time1][df.totals>type4_time2][df.type==3].totals)
                diff=(type4_time1-max_type1_time1)
                x.append(diff)
        type4_time=df[df.type==4].totals.values[len(df[df.type==4])-1]
        if len(df[df.totals<type4_time][df.type==3].totals)>0:
            max_type1_time=np.min(df[df.totals<type4_time][df.type==3].totals.values)
            diff=(type4_time-max_type1_time)
            x.append(diff)
        if len(x)>0:
            max_diff=np.max(x)
            return max_diff
    return -1
type34_max_diff=buy_user_action.groupby(['user_id','sku_id']).apply(type34_max_diff).reset_index()
type34_max_diff.columns=['user_id','sku_id','type34_max_diff']
type34_user_max_diff=type34_max_diff.groupby('user_id')['type34_max_diff'].max().reset_index()
type34_user_max_diff.columns=['user_id','a_diff_max_type3_4']
train=pd.merge(train,type34_user_max_diff,on='user_id',how='left')
train.a_diff_max_type3_4.fillna(-1,inplace=True)

#该用户  A     max（关注 - 下单） 时长
def type54_max_diff(df):
    if len(df[df.type==4])==1:
        df=df.sort_values('totals')
        type4_time=df[df.type==4].totals.values[0]
        if len(df[df.totals<type4_time][df.type==5].totals)>0:
            max_type1_time=np.min(df[df.totals<type4_time][df.type==5].totals.values)
            return type4_time-max_type1_time
        return -1
    if len(df[df.type==4])>1:
        x=[]
        df=df.sort_values('totals')
        for i in range(len(df[df.type==4])-1):
            type4_time1=df[df.type==4].totals.values[i]
            type4_time2=df[df.type==4].totals.values[i+1]
            if len(df[df.totals<type4_time1][df.totals>type4_time2][df.type==5].totals)>0:
                max_type1_time1=np.min(df[df.totals<type4_time1][df.totals>type4_time2][df.type==5].totals)
                diff=(type4_time1-max_type1_time1)
                x.append(diff)
        type4_time=df[df.type==4].totals.values[len(df[df.type==4])-1]
        if len(df[df.totals<type4_time][df.type==5].totals)>0:
            max_type1_time=np.min(df[df.totals<type4_time][df.type==5].totals.values)
            diff=(type4_time-max_type1_time)
            x.append(diff)
        if len(x)>0:
            max_diff=np.max(x)
            return max_diff
    return -1
type54_max_diff=buy_user_action.groupby(['user_id','sku_id']).apply(type54_max_diff).reset_index()
type54_max_diff.columns=['user_id','sku_id','type54_max_diff']
type54_user_max_diff=type54_max_diff.groupby('user_id')['type54_max_diff'].max().reset_index()
type54_user_max_diff.columns=['user_id','a_diff_max_type5_4']
train=pd.merge(train,type54_user_max_diff,on='user_id',how='left')
train.a_diff_max_type5_4.fillna(-1,inplace=True)

#该用户  A      max（点击 - 下单） 时长
def type64_max_diff(df):
    if len(df[df.type==4])==1:
        df=df.sort_values('totals')
        type4_time=df[df.type==4].totals.values[0]
        if len(df[df.totals<type4_time][df.type==6].totals)>0:
            max_type1_time=np.min(df[df.totals<type4_time][df.type==6].totals.values)
            return type4_time-max_type1_time
        return -1
    if len(df[df.type==4])>1:
        x=[]
        df=df.sort_values('totals')
        for i in range(len(df[df.type==4])-1):
            type4_time1=df[df.type==4].totals.values[i]
            type4_time2=df[df.type==4].totals.values[i+1]
            if len(df[df.totals<type4_time1][df.totals>type4_time2][df.type==6].totals)>0:
                max_type1_time1=np.min(df[df.totals<type4_time1][df.totals>type4_time2][df.type==6].totals)
                diff=(type4_time1-max_type1_time1)
                x.append(diff)
        type4_time=df[df.type==4].totals.values[len(df[df.type==4])-1]
        if len(df[df.totals<type4_time][df.type==6].totals)>0:
            max_type1_time=np.min(df[df.totals<type4_time][df.type==6].totals.values)
            diff=(type4_time-max_type1_time)
            x.append(diff)
        if len(x)>0:
            max_diff=np.max(x)
            return max_diff
    return -1
type64_max_diff=buy_user_action.groupby(['user_id','sku_id']).apply(type64_max_diff).reset_index()
type64_max_diff.columns=['user_id','sku_id','type64_max_diff']
type64_user_max_diff=type64_max_diff.groupby('user_id')['type64_max_diff'].max().reset_index()
type64_user_max_diff.columns=['user_id','a_diff_max_type6_4']
train=pd.merge(train,type64_user_max_diff,on='user_id',how='left')
train.a_diff_max_type6_4.fillna(-1,inplace=True)

#该用户  A      min（浏览 - 下单） 时长
def type14_min_diff(df):
    if len(df[df.type==4])==1:
        df=df.sort_values('totals')
        type4_time=df[df.type==4].totals.values[0]
        if len(df[df.totals<type4_time][df.type==1].totals)>0:
            max_type1_time=np.max(df[df.totals<type4_time][df.type==1].totals.values)
            return type4_time-max_type1_time
        # return timedelta(-1).days
    if len(df[df.type==4])>1:
        x=[]
        df=df.sort_values('totals')
        for i in range(len(df[df.type==4])-1):
            type4_time1=df[df.type==4].totals.values[i]
            type4_time2=df[df.type==4].totals.values[i+1]
            if len(df[df.totals<type4_time1][df.totals>type4_time2][df.type==1].totals)>0:
                max_type1_time1=np.max(df[df.totals<type4_time1][df.totals>type4_time2][df.type==1].totals)
                diff=(type4_time1-max_type1_time1)
                x.append(diff)
        type4_time=df[df.type==4].totals.values[len(df[df.type==4])-1]
        if len(df[df.totals<type4_time][df.type==1].totals)>0:
            max_type1_time=np.max(df[df.totals<type4_time][df.type==1].totals.values)
            diff=(type4_time-max_type1_time)
            x.append(diff)
        if len(x)>0:
            max_diff=np.min(x)
            return max_diff
    # return timedelta(-1).days
type14_max_diff=buy_user_action.groupby(['user_id','sku_id']).apply(type14_min_diff).reset_index()
type14_max_diff.columns=['user_id','sku_id','type14_min_diff']
type14_user_max_diff=type14_max_diff.groupby('user_id')['type14_min_diff'].min().reset_index()
type14_user_max_diff.columns=['user_id','a_diff_min_type1_4']
train=pd.merge(train,type14_user_max_diff,on='user_id',how='left')
train.a_diff_min_type1_4.fillna(-1,inplace=True)

#该用户  A     min（加购 - 下单） 时长
def type24_min_diff(df):
    if len(df[df.type==4])==1:
        df=df.sort_values('totals')
        type4_time=df[df.type==4].totals.values[0]
        if len(df[df.totals<type4_time][df.type==2].totals)>0:
            max_type1_time=np.max(df[df.totals<type4_time][df.type==2].totals.values)
            return type4_time-max_type1_time
        # return timedelta(-1).days
    if len(df[df.type==4])>1:
        x=[]
        df=df.sort_values('totals')
        for i in range(len(df[df.type==4])-1):
            type4_time1=df[df.type==4].totals.values[i]
            type4_time2=df[df.type==4].totals.values[i+1]
            if len(df[df.totals<type4_time1][df.totals>type4_time2][df.type==2].totals)>0:
                max_type1_time1=np.max(df[df.totals<type4_time1][df.totals>type4_time2][df.type==2].totals)
                diff=(type4_time1-max_type1_time1)
                x.append(diff)
        type4_time=df[df.type==4].totals.values[len(df[df.type==4])-1]
        if len(df[df.totals<type4_time][df.type==2].totals)>0:
            max_type1_time=np.max(df[df.totals<type4_time][df.type==2].totals.values)
            diff=(type4_time-max_type1_time)
            x.append(diff)
        if len(x)>0:
            max_diff=np.min(x)
            return max_diff
    # return timedelta(-1).days
type24_max_diff=buy_user_action.groupby(['user_id','sku_id']).apply(type24_min_diff).reset_index()
type24_max_diff.columns=['user_id','sku_id','type24_min_diff']
type24_user_max_diff=type24_max_diff.groupby('user_id')['type24_min_diff'].min().reset_index()
type24_user_max_diff.columns=['user_id','a_diff_min_type2_4']
train=pd.merge(train,type24_user_max_diff,on='user_id',how='left')
train.a_diff_min_type2_4.fillna(-1,inplace=True)

#该用户  A    min（删购 - 下单） 时长
def type34_min_diff(df):
    if len(df[df.type==4])==1:
        df=df.sort_values('totals')
        type4_time=df[df.type==4].totals.values[0]
        if len(df[df.totals<type4_time][df.type==3].totals)>0:
            max_type1_time=np.max(df[df.totals<type4_time][df.type==3].totals.values)
            return type4_time-max_type1_time
        # return timedelta(-1).days
    if len(df[df.type==4])>1:
        x=[]
        df=df.sort_values('totals')
        for i in range(len(df[df.type==4])-1):
            type4_time1=df[df.type==4].totals.values[i]
            type4_time2=df[df.type==4].totals.values[i+1]
            if len(df[df.totals<type4_time1][df.totals>type4_time2][df.type==3].totals)>0:
                max_type1_time1=np.max(df[df.totals<type4_time1][df.totals>type4_time2][df.type==3].totals)
                diff=(type4_time1-max_type1_time1)
                x.append(diff)
        type4_time=df[df.type==4].totals.values[len(df[df.type==4])-1]
        if len(df[df.totals<type4_time][df.type==3].totals)>0:
            max_type1_time=np.max(df[df.totals<type4_time][df.type==3].totals.values)
            diff=(type4_time-max_type1_time)
            x.append(diff)
        if len(x)>0:
            max_diff=np.min(x)
            return max_diff
    # return timedelta(-1).days
type34_max_diff=buy_user_action.groupby(['user_id','sku_id']).apply(type34_min_diff).reset_index()
type34_max_diff.columns=['user_id','sku_id','type34_min_diff']
type34_user_max_diff=type34_max_diff.groupby('user_id')['type34_min_diff'].min().reset_index()
type34_user_max_diff.columns=['user_id','a_diff_min_type3_4']
train=pd.merge(train,type34_user_max_diff,on='user_id',how='left')
train.a_diff_min_type3_4.fillna(-1,inplace=True)

#该用户  A     min（关注 - 下单） 时长
def type54_min_diff(df):
    if len(df[df.type==4])==1:
        df=df.sort_values('totals')
        type4_time=df[df.type==4].totals.values[0]
        if len(df[df.totals<type4_time][df.type==5].totals)>0:
            max_type1_time=np.max(df[df.totals<type4_time][df.type==5].totals.values)
            return type4_time-max_type1_time
        # return timedelta(-1).days
    if len(df[df.type==4])>1:
        x=[]
        df=df.sort_values('totals')
        for i in range(len(df[df.type==4])-1):
            type4_time1=df[df.type==4].totals.values[i]
            type4_time2=df[df.type==4].totals.values[i+1]
            if len(df[df.totals<type4_time1][df.totals>type4_time2][df.type==5].totals)>0:
                max_type1_time1=np.max(df[df.totals<type4_time1][df.totals>type4_time2][df.type==5].totals)
                diff=(type4_time1-max_type1_time1)
                x.append(diff)
        type4_time=df[df.type==4].totals.values[len(df[df.type==4])-1]
        if len(df[df.totals<type4_time][df.type==5].totals)>0:
            max_type1_time=np.max(df[df.totals<type4_time][df.type==5].totals.values)
            diff=(type4_time-max_type1_time)
            x.append(diff)
        if len(x)>0:
            max_diff=np.min(x)
            return max_diff
    # return timedelta(-1).days
type54_max_diff=buy_user_action.groupby(['user_id','sku_id']).apply(type54_min_diff).reset_index()
type54_max_diff.columns=['user_id','sku_id','type54_min_diff']
type54_user_max_diff=type54_max_diff.groupby('user_id')['type54_min_diff'].min().reset_index()
type54_user_max_diff.columns=['user_id','a_diff_min_type5_4']
train=pd.merge(train,type54_user_max_diff,on='user_id',how='left')
train.a_diff_min_type5_4.fillna(-1,inplace=True)

#该用户  A      min（点击 - 下单） 时长
def type64_min_diff(df):
    if len(df[df.type==4])==1:
        df=df.sort_values('totals')
        type4_time=df[df.type==4].totals.values[0]
        if len(df[df.totals<type4_time][df.type==6].totals)>0:
            max_type1_time=np.max(df[df.totals<type4_time][df.type==6].totals.values)
            return type4_time-max_type1_time
        return -1
    if len(df[df.type==4])>1:
        x=[]
        df=df.sort_values('totals')
        for i in range(len(df[df.type==4])-1):
            type4_time1=df[df.type==4].totals.values[i]
            type4_time2=df[df.type==4].totals.values[i+1]
            if len(df[df.totals<type4_time1][df.totals>type4_time2][df.type==6].totals)>0:
                max_type1_time1=np.max(df[df.totals<type4_time1][df.totals>type4_time2][df.type==6].totals)
                diff=(type4_time1-max_type1_time1)
                x.append(diff)
        type4_time=df[df.type==4].totals.values[len(df[df.type==4])-1]
        if len(df[df.totals<type4_time][df.type==6].totals)>0:
            max_type1_time=np.max(df[df.totals<type4_time][df.type==6].totals.values)
            diff=(type4_time-max_type1_time)
            x.append(diff)
        if len(x)>0:
            max_diff=np.min(x)
            return max_diff
    return -1
type64_max_diff=buy_user_action.groupby(['user_id','sku_id']).apply(type64_min_diff).reset_index()
type64_max_diff.columns=['user_id','sku_id','type64_min_diff']
type64_user_max_diff=type64_max_diff.groupby('user_id')['type64_min_diff'].min().reset_index()
type64_user_max_diff.columns=['user_id','a_diff_min_type6_4']
train=pd.merge(train,type64_user_max_diff,on='user_id',how='left')
train.a_diff_min_type6_4.fillna(-1,inplace=True)

#该用户  A     avg（浏览 - 下单） 时长
def type14_avg_diff(df):
    if len(df[df.type==4])==1:
        df=df.sort_values('totals')
        type4_time=df[df.type==4].totals.values[0]
        if len(df[df.totals<type4_time][df.type==1].time)>0:
            max_type1_time=np.mean(df[df.totals<type4_time][df.type==1].totals.values)
            return (type4_time-max_type1_time)
        return -1
    if len(df[df.type==4])>1:
        x=[]
        df=df.sort_values('time')
        for i in range(len(df[df.type==4])-1):
            type4_time1=df[df.type==4].totals.values[i]
            type4_time2=df[df.type==4].totals.values[i+1]
            if len(df[df.totals<type4_time1][df.totals>type4_time2][df.type==1].time)>0:
                max_type1_time1=np.mean(df[df.totals<type4_time1][df.totals>type4_time2][df.type==1].time)
                diff=(type4_time1-max_type1_time1)
                x.append(diff)
        type4_time=df[df.type==4].totals.values[len(df[df.type==4])-1]
        if len(df[df.totals<type4_time][df.type==1].time)>0:
            max_type1_time=np.mean(df[df.totals<type4_time][df.type==1].totals.values)
            diff=(type4_time-max_type1_time)
            x.append(diff)
        if len(x)>0:
            max_diff=np.mean(x)
            return max_diff
    return -1
type14_max_diff=buy_user_action.groupby(['user_id','sku_id']).apply(type14_avg_diff).reset_index()
type14_max_diff.columns=['user_id','sku_id','type14_avg_diff']
type14_user_max_diff=type14_max_diff.groupby('user_id')['type14_avg_diff'].mean().reset_index()
type14_user_max_diff.columns=['user_id','a_diff_avg_type1_4']
# type14_user_max_diff['a_diff_avg_type1_4']=[int(i.total_seconds())/3600.0 for i in (type14_user_max_diff['a_diff_avg_type1_4'])]
train=pd.merge(train,type14_user_max_diff,on='user_id',how='left')
train.a_diff_avg_type1_4.fillna(-1,inplace=True)

#该用户  A    avg（加购 - 下单） 时长
def type24_avg_diff(df):
    if len(df[df.type==4])==1:
        df=df.sort_values('totals')
        type4_time=df[df.type==4].totals.values[0]
        if len(df[df.totals<type4_time][df.type==2].time)>0:
            max_type1_time=np.mean(df[df.totals<type4_time][df.type==2].totals.values)
            return (type4_time-max_type1_time)
        return -1
    if len(df[df.type==4])>1:
        x=[]
        df=df.sort_values('time')
        for i in range(len(df[df.type==4])-1):
            type4_time1=df[df.type==4].totals.values[i]
            type4_time2=df[df.type==4].totals.values[i+1]
            if len(df[df.totals<type4_time1][df.totals>type4_time2][df.type==2].time)>0:
                max_type1_time1=np.mean(df[df.totals<type4_time1][df.totals>type4_time2][df.type==2].time)
                diff=(type4_time1-max_type1_time1)
                x.append(diff)
        type4_time=df[df.type==4].totals.values[len(df[df.type==4])-1]
        if len(df[df.totals<type4_time][df.type==2].time)>0:
            max_type1_time=np.mean(df[df.totals<type4_time][df.type==2].totals.values)
            diff=(type4_time-max_type1_time)
            x.append(diff)
        if len(x)>0:
            max_diff=np.mean(x)
            return max_diff
    return -1
type14_max_diff=buy_user_action.groupby(['user_id','sku_id']).apply(type24_avg_diff).reset_index()
type14_max_diff.columns=['user_id','sku_id','type24_avg_diff']
type14_user_max_diff=type14_max_diff.groupby('user_id')['type24_avg_diff'].mean().reset_index()
type14_user_max_diff.columns=['user_id','a_diff_avg_type2_4']
# type14_user_max_diff['a_diff_avg_type1_4']=[int(i.total_seconds())/3600.0 for i in (type14_user_max_diff['a_diff_avg_type1_4'])]
train=pd.merge(train,type14_user_max_diff,on='user_id',how='left')
train.a_diff_avg_type2_4.fillna(-1,inplace=True)
#该用户  A    avg（删购 - 下单） 时长
def type34_avg_diff(df):
    if len(df[df.type==4])==1:
        df=df.sort_values('totals')
        type4_time=df[df.type==4].totals.values[0]
        if len(df[df.totals<type4_time][df.type==3].time)>0:
            max_type1_time=np.mean(df[df.totals<type4_time][df.type==3].totals.values)
            return (type4_time-max_type1_time)
        return -1
    if len(df[df.type==4])>1:
        x=[]
        df=df.sort_values('time')
        for i in range(len(df[df.type==4])-1):
            type4_time1=df[df.type==4].totals.values[i]
            type4_time2=df[df.type==4].totals.values[i+1]
            if len(df[df.totals<type4_time1][df.totals>type4_time2][df.type==3].time)>0:
                max_type1_time1=np.mean(df[df.totals<type4_time1][df.totals>type4_time2][df.type==3].time)
                diff=(type4_time1-max_type1_time1)
                x.append(diff)
        type4_time=df[df.type==4].totals.values[len(df[df.type==4])-1]
        if len(df[df.totals<type4_time][df.type==3].time)>0:
            max_type1_time=np.mean(df[df.totals<type4_time][df.type==3].totals.values)
            diff=(type4_time-max_type1_time)
            x.append(diff)
        if len(x)>0:
            max_diff=np.mean(x)
            return max_diff
    return -1
type14_max_diff=buy_user_action.groupby(['user_id','sku_id']).apply(type34_avg_diff).reset_index()
type14_max_diff.columns=['user_id','sku_id','type34_avg_diff']
type14_user_max_diff=type14_max_diff.groupby('user_id')['type34_avg_diff'].mean().reset_index()
type14_user_max_diff.columns=['user_id','a_diff_avg_type3_4']
# type14_user_max_diff['a_diff_avg_type1_4']=[int(i.total_seconds())/3600.0 for i in (type14_user_max_diff['a_diff_avg_type1_4'])]
train=pd.merge(train,type14_user_max_diff,on='user_id',how='left')
train.a_diff_avg_type3_4.fillna(-1,inplace=True)

#该用户  A     avg（关注 - 下单） 时长
def type54_avg_diff(df):
    if len(df[df.type==4])==1:
        df=df.sort_values('totals')
        type4_time=df[df.type==4].totals.values[0]
        if len(df[df.totals<type4_time][df.type==5].time)>0:
            max_type1_time=np.mean(df[df.totals<type4_time][df.type==5].totals.values)
            return (type4_time-max_type1_time)
        return -1
    if len(df[df.type==4])>1:
        x=[]
        df=df.sort_values('time')
        for i in range(len(df[df.type==4])-1):
            type4_time1=df[df.type==4].totals.values[i]
            type4_time2=df[df.type==4].totals.values[i+1]
            if len(df[df.totals<type4_time1][df.totals>type4_time2][df.type==5].time)>0:
                max_type1_time1=np.mean(df[df.totals<type4_time1][df.totals>type4_time2][df.type==5].time)
                diff=(type4_time1-max_type1_time1)
                x.append(diff)
        type4_time=df[df.type==4].totals.values[len(df[df.type==4])-1]
        if len(df[df.totals<type4_time][df.type==5].time)>0:
            max_type1_time=np.mean(df[df.totals<type4_time][df.type==5].totals.values)
            diff=(type4_time-max_type1_time)
            x.append(diff)
        if len(x)>0:
            max_diff=np.mean(x)
            return max_diff
    return -1
type14_max_diff=buy_user_action.groupby(['user_id','sku_id']).apply(type54_avg_diff).reset_index()
type14_max_diff.columns=['user_id','sku_id','type54_avg_diff']
type14_user_max_diff=type14_max_diff.groupby('user_id')['type54_avg_diff'].mean().reset_index()
type14_user_max_diff.columns=['user_id','a_diff_avg_type5_4']
# type14_user_max_diff['a_diff_avg_type1_4']=[int(i.total_seconds())/3600.0 for i in (type14_user_max_diff['a_diff_avg_type1_4'])]
train=pd.merge(train,type14_user_max_diff,on='user_id',how='left')
train.a_diff_avg_type5_4.fillna(-1,inplace=True)


#该用户  A      avg（点击 - 下单） 时长
def type64_avg_diff(df):
    if len(df[df.type==4])==1:
        df=df.sort_values('totals')
        type4_time=df[df.type==4].totals.values[0]
        if len(df[df.totals<type4_time][df.type==6].time)>0:
            max_type1_time=np.mean(df[df.totals<type4_time][df.type==6].totals.values)
            return (type4_time-max_type1_time)
        return -1
    if len(df[df.type==4])>1:
        x=[]
        df=df.sort_values('time')
        for i in range(len(df[df.type==4])-1):
            type4_time1=df[df.type==4].totals.values[i]
            type4_time2=df[df.type==4].totals.values[i+1]
            if len(df[df.totals<type4_time1][df.totals>type4_time2][df.type==6].time)>0:
                max_type1_time1=np.mean(df[df.totals<type4_time1][df.totals>type4_time2][df.type==6].time)
                diff=(type4_time1-max_type1_time1)
                x.append(diff)
        type4_time=df[df.type==4].totals.values[len(df[df.type==4])-1]
        if len(df[df.totals<type4_time][df.type==6].time)>0:
            max_type1_time=np.mean(df[df.totals<type4_time][df.type==6].totals.values)
            diff=(type4_time-max_type1_time)
            x.append(diff)
        if len(x)>0:
            max_diff=np.mean(x)
            return max_diff
    return -1
type14_max_diff=buy_user_action.groupby(['user_id','sku_id']).apply(type64_avg_diff).reset_index()
type14_max_diff.columns=['user_id','sku_id','type64_avg_diff']
type14_user_max_diff=type14_max_diff.groupby('user_id')['type64_avg_diff'].mean().reset_index()
type14_user_max_diff.columns=['user_id','a_diff_avg_type6_4']
# type14_user_max_diff['a_diff_avg_type1_4']=[int(i.total_seconds())/3600.0 for i in (type14_user_max_diff['a_diff_avg_type1_4'])]
train=pd.merge(train,type14_user_max_diff,on='user_id',how='left')
train.a_diff_avg_type6_4.fillna(-1,inplace=True)

#该用户  A     median（浏览 - 下单） 时长
def type14_median_diff(df):
    if len(df[df.type==4])==1:
        df=df.sort_values('totals')
        type4_time=df[df.type==4].totals.values[0]
        if len(df[df.totals<type4_time][df.type==1].time)>0:
            max_type1_time=np.median(df[df.totals<type4_time][df.type==1].totals.values)
            return (type4_time-max_type1_time)
        return -1
    if len(df[df.type==4])>1:
        x=[]
        df=df.sort_values('time')
        for i in range(len(df[df.type==4])-1):
            type4_time1=df[df.type==4].totals.values[i]
            type4_time2=df[df.type==4].totals.values[i+1]
            if len(df[df.totals<type4_time1][df.totals>type4_time2][df.type==1].time)>0:
                max_type1_time1=np.median(df[df.totals<type4_time1][df.totals>type4_time2][df.type==1].time)
                diff=(type4_time1-max_type1_time1)
                x.append(diff)
        type4_time=df[df.type==4].totals.values[len(df[df.type==4])-1]
        if len(df[df.totals<type4_time][df.type==1].time)>0:
            max_type1_time=np.median(df[df.totals<type4_time][df.type==1].totals.values)
            diff=(type4_time-max_type1_time)
            x.append(diff)
        if len(x)>0:
            max_diff=np.median(x)
            return max_diff
    return -1
type14_max_diff=buy_user_action.groupby(['user_id','sku_id']).apply(type14_median_diff).reset_index()
type14_max_diff.columns=['user_id','sku_id','type14_median_diff']
type14_user_max_diff=type14_max_diff.groupby('user_id')['type14_median_diff'].mean().reset_index()
type14_user_max_diff.columns=['user_id','a_diff_median_type1_4']
# type14_user_max_diff['a_diff_avg_type1_4']=[int(i.total_seconds())/3600.0 for i in (type14_user_max_diff['a_diff_avg_type1_4'])]
train=pd.merge(train,type14_user_max_diff,on='user_id',how='left')
train.a_diff_median_type1_4.fillna(-1,inplace=True)

#该用户  A    median（加购 - 下单） 时长
def type24_median_diff(df):
    if len(df[df.type==4])==1:
        df=df.sort_values('totals')
        type4_time=df[df.type==4].totals.values[0]
        if len(df[df.totals<type4_time][df.type==2].time)>0:
            max_type1_time=np.median(df[df.totals<type4_time][df.type==2].totals.values)
            return (type4_time-max_type1_time)
        return -1
    if len(df[df.type==4])>1:
        x=[]
        df=df.sort_values('time')
        for i in range(len(df[df.type==4])-1):
            type4_time1=df[df.type==4].totals.values[i]
            type4_time2=df[df.type==4].totals.values[i+1]
            if len(df[df.totals<type4_time1][df.totals>type4_time2][df.type==2].time)>0:
                max_type1_time1=np.median(df[df.totals<type4_time1][df.totals>type4_time2][df.type==2].time)
                diff=(type4_time1-max_type1_time1)
                x.append(diff)
        type4_time=df[df.type==4].totals.values[len(df[df.type==4])-1]
        if len(df[df.totals<type4_time][df.type==2].time)>0:
            max_type1_time=np.median(df[df.totals<type4_time][df.type==2].totals.values)
            diff=(type4_time-max_type1_time)
            x.append(diff)
        if len(x)>0:
            max_diff=np.median(x)
            return max_diff
    return -1
type14_max_diff=buy_user_action.groupby(['user_id','sku_id']).apply(type24_median_diff).reset_index()
type14_max_diff.columns=['user_id','sku_id','type24_median_diff']
type14_user_max_diff=type14_max_diff.groupby('user_id')['type24_median_diff'].mean().reset_index()
type14_user_max_diff.columns=['user_id','a_diff_median_type2_4']
# type14_user_max_diff['a_diff_avg_type1_4']=[int(i.total_seconds())/3600.0 for i in (type14_user_max_diff['a_diff_avg_type1_4'])]
train=pd.merge(train,type14_user_max_diff,on='user_id',how='left')
train.a_diff_median_type2_4.fillna(-1,inplace=True)

#该用户  A    median（删购 - 下单） 时长
def type34_median_diff(df):
    if len(df[df.type==4])==1:
        df=df.sort_values('totals')
        type4_time=df[df.type==4].totals.values[0]
        if len(df[df.totals<type4_time][df.type==3].time)>0:
            max_type1_time=np.median(df[df.totals<type4_time][df.type==3].totals.values)
            return (type4_time-max_type1_time)
        return -1
    if len(df[df.type==4])>1:
        x=[]
        df=df.sort_values('time')
        for i in range(len(df[df.type==4])-1):
            type4_time1=df[df.type==4].totals.values[i]
            type4_time2=df[df.type==4].totals.values[i+1]
            if len(df[df.totals<type4_time1][df.totals>type4_time2][df.type==3].time)>0:
                max_type1_time1=np.median(df[df.totals<type4_time1][df.totals>type4_time2][df.type==3].time)
                diff=(type4_time1-max_type1_time1)
                x.append(diff)
        type4_time=df[df.type==4].totals.values[len(df[df.type==4])-1]
        if len(df[df.totals<type4_time][df.type==3].time)>0:
            max_type1_time=np.median(df[df.totals<type4_time][df.type==3].totals.values)
            diff=(type4_time-max_type1_time)
            x.append(diff)
        if len(x)>0:
            max_diff=np.median(x)
            return max_diff
    return -1
type14_max_diff=buy_user_action.groupby(['user_id','sku_id']).apply(type34_median_diff).reset_index()
type14_max_diff.columns=['user_id','sku_id','type34_median_diff']
type14_user_max_diff=type14_max_diff.groupby('user_id')['type34_median_diff'].mean().reset_index()
type14_user_max_diff.columns=['user_id','a_diff_median_type3_4']
# type14_user_max_diff['a_diff_avg_type1_4']=[int(i.total_seconds())/3600.0 for i in (type14_user_max_diff['a_diff_avg_type1_4'])]
train=pd.merge(train,type14_user_max_diff,on='user_id',how='left')
train.a_diff_median_type3_4.fillna(-1,inplace=True)

#该用户  A    median（关注 - 下单） 时长
def type54_median_diff(df):
    if len(df[df.type==4])==1:
        df=df.sort_values('totals')
        type4_time=df[df.type==4].totals.values[0]
        if len(df[df.totals<type4_time][df.type==5].time)>0:
            max_type1_time=np.median(df[df.totals<type4_time][df.type==5].totals.values)
            return (type4_time-max_type1_time)
        return -1
    if len(df[df.type==4])>1:
        x=[]
        df=df.sort_values('time')
        for i in range(len(df[df.type==4])-1):
            type4_time1=df[df.type==4].totals.values[i]
            type4_time2=df[df.type==4].totals.values[i+1]
            if len(df[df.totals<type4_time1][df.totals>type4_time2][df.type==5].time)>0:
                max_type1_time1=np.median(df[df.totals<type4_time1][df.totals>type4_time2][df.type==5].time)
                diff=(type4_time1-max_type1_time1)
                x.append(diff)
        type4_time=df[df.type==4].totals.values[len(df[df.type==4])-1]
        if len(df[df.totals<type4_time][df.type==5].time)>0:
            max_type1_time=np.median(df[df.totals<type4_time][df.type==5].totals.values)
            diff=(type4_time-max_type1_time)
            x.append(diff)
        if len(x)>0:
            max_diff=np.median(x)
            return max_diff
    return -1
type14_max_diff=buy_user_action.groupby(['user_id','sku_id']).apply(type54_median_diff).reset_index()
type14_max_diff.columns=['user_id','sku_id','type54_median_diff']
type14_user_max_diff=type14_max_diff.groupby('user_id')['type54_median_diff'].mean().reset_index()
type14_user_max_diff.columns=['user_id','a_diff_median_type5_4']
# type14_user_max_diff['a_diff_avg_type1_4']=[int(i.total_seconds())/3600.0 for i in (type14_user_max_diff['a_diff_avg_type1_4'])]
train=pd.merge(train,type14_user_max_diff,on='user_id',how='left')
train.a_diff_median_type5_4.fillna(-1,inplace=True)


#该用户  A      median（点击 - 下单） 时长
def type64_median_diff(df):
    if len(df[df.type==4])==1:
        df=df.sort_values('totals')
        type4_time=df[df.type==4].totals.values[0]
        if len(df[df.totals<type4_time][df.type==6].time)>0:
            max_type1_time=np.median(df[df.totals<type4_time][df.type==6].totals.values)
            return (type4_time-max_type1_time)
        return -1
    if len(df[df.type==4])>1:
        x=[]
        df=df.sort_values('time')
        for i in range(len(df[df.type==4])-1):
            type4_time1=df[df.type==4].totals.values[i]
            type4_time2=df[df.type==4].totals.values[i+1]
            if len(df[df.totals<type4_time1][df.totals>type4_time2][df.type==6].time)>0:
                max_type1_time1=np.median(df[df.totals<type4_time1][df.totals>type4_time2][df.type==6].time)
                diff=(type4_time1-max_type1_time1)
                x.append(diff)
        type4_time=df[df.type==4].totals.values[len(df[df.type==4])-1]
        if len(df[df.totals<type4_time][df.type==6].time)>0:
            max_type1_time=np.median(df[df.totals<type4_time][df.type==6].totals.values)
            diff=(type4_time-max_type1_time)
            x.append(diff)
        if len(x)>0:
            max_diff=np.median(x)
            return max_diff
    return -1
type14_max_diff=buy_user_action.groupby(['user_id','sku_id']).apply(type64_median_diff).reset_index()
type14_max_diff.columns=['user_id','sku_id','type64_median_diff']
type14_user_max_diff=type14_max_diff.groupby('user_id')['type64_median_diff'].mean().reset_index()
type14_user_max_diff.columns=['user_id','a_diff_median_type6_4']
# type14_user_max_diff['a_diff_avg_type1_4']=[int(i.total_seconds())/3600.0 for i in (type14_user_max_diff['a_diff_avg_type1_4'])]
train=pd.merge(train,type14_user_max_diff,on='user_id',how='left')
train.a_diff_median_type6_4.fillna(-1,inplace=True)

#该用户  A      只加购一次就下单   次数
#train里user的行为
action_user=pd.merge(train[['user_id']],action8,on='user_id',how='left')
df = pd.get_dummies(action_user['type'], prefix='type')
action_user = pd.concat([action_user, df], axis=1)
action_user_a=action_user[action_user.week_num>=all_data_start_week][action_user.week_num<=all_data_end_week]
extract_type_relation_featrue_data=action_user.groupby(['user_id','sku_id'])['type_1','type_2','type_3','type_4','type_5','type_6'].sum().reset_index()
type2_4=extract_type_relation_featrue_data[extract_type_relation_featrue_data.type_2==1][extract_type_relation_featrue_data.type_4==1][['user_id','sku_id']]
a_times_one_type2_4=type2_4.groupby('user_id').size().reset_index()
a_times_one_type2_4.columns=['user_id','a_times_one_type2_4']
train=pd.merge(train,a_times_one_type2_4,on='user_id',how='left')
train.a_times_one_type2_4.fillna(0,inplace=True)
#该用户  A      加购+删购    没有下单    次数
type23_not4=extract_type_relation_featrue_data[extract_type_relation_featrue_data.type_2>0][extract_type_relation_featrue_data.type_4==0][extract_type_relation_featrue_data.type_3>0][['user_id','sku_id']]
a_times_one_type2_3=type23_not4.groupby('user_id').size().reset_index()
a_times_one_type2_3.columns=['user_id','a_times_one_type2_3']
train=pd.merge(train,a_times_one_type2_3,on='user_id',how='left')
train.a_times_one_type2_3.fillna(0,inplace=True)
#该用户  A     针对cate8任一件商品  加购  + 删购  + 加购 （超过2次加购同一件商品）  并最终下单  次数
type2_4=extract_type_relation_featrue_data[extract_type_relation_featrue_data.type_2>1][extract_type_relation_featrue_data.type_4>=1][['user_id','sku_id']]
a_times_more_type2_4=type2_4.groupby('user_id').size().reset_index()
a_times_more_type2_4.columns=['user_id','a_times_more_type2_4']
train=pd.merge(train,a_times_more_type2_4,on='user_id',how='left')
train.a_times_more_type2_4.fillna(0,inplace=True)

#A  中用户总共  有行为的周数  （有几周有行为记录）
def action_week(df):
    return len(df.unique())
a_count_sku_active_weeks=end5_user_a_action8.groupby('user_id')['week_num'].apply(action_week).reset_index()
a_count_sku_active_weeks.columns=['user_id','a_count_sku_active_weeks']
train=pd.merge(train,a_count_sku_active_weeks,on='user_id',how='left')
train.a_count_sku_active_weeks.fillna(0,inplace=True)
train.to_csv(u'D:/Competition/JD/JNEWdata/train_user.csv',index=False)

#A  中用户 每一周   最多加购,删购，下单次数
df = pd.get_dummies(end5_user_a_action8['type'], prefix='type')
end5_user_a_cate8_action = pd.concat([end5_user_a_action8, df], axis=1)
week_action_data=end5_user_a_cate8_action[['user_id','week_num','type_1','type_2','type_3','type_4','type_5','type_6']]
user_week_action_sum=week_action_data.groupby(['user_id','week_num']).sum().reset_index()
temp= user_week_action_sum.groupby('user_id')['type_2','type_3','type_4'].max().reset_index()
temp.columns=['user_id','a_count_max_sku_weekly_type2','a_count_max_sku_weekly_type3','a_count_max_sku_weekly_type4']
train=pd.merge(train,temp,on='user_id',how='left')

#A  中用户 每一周   最少，加购，删购，下单
user_week_action_sum=week_action_data.groupby(['user_id','week_num']).sum().reset_index()
temp= user_week_action_sum.groupby('user_id')['type_2','type_3','type_4'].min().reset_index()
temp.columns=['user_id','a_count_min_sku_weekly_type2','a_count_min_sku_weekly_type3','a_count_min_sku_weekly_type4']
train=pd.merge(train,temp,on='user_id',how='left')

#A  中用户 每一周   平均，加购，删购，下单
user_week_action_sum=week_action_data.groupby(['user_id','week_num']).sum().reset_index()
temp= user_week_action_sum.groupby('user_id')['type_2','type_3','type_4'].mean().reset_index()
temp.columns=['user_id','a_count_mean_sku_weekly_type2','a_count_mean_sku_weekly_type3','a_count_mean_sku_weekly_type4']
train=pd.merge(train,temp,on='user_id',how='left')

#A  中用户 每一周   中位数，加购，删购，下单
user_week_action_sum=week_action_data.groupby(['user_id','week_num']).sum().reset_index()
temp= user_week_action_sum.groupby('user_id')['type_2','type_3','type_4'].median().reset_index()
temp.columns=['user_id','a_count_median_sku_weekly_type2','a_count_median_sku_weekly_type3','a_count_median_sku_weekly_type4']
train=pd.merge(train,temp,on='user_id',how='left')









