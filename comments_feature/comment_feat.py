# -*- coding: UTF-8 -*-
import time
from datetime import datetime
from datetime import timedelta
import pandas as pd
import math
import numpy as np

action_1_path = "/home/javis/jd2017/jdata/JData_Action_201602.csv"
action_2_path = "/home/javis/jd2017/jdata/JData_Action_201603.csv"
action_3_path = "/home/javis/jd2017/jdata/JData_Action_201604.csv"
comment_path = "/home/javis/jd2017/jdata/JData_Comment.csv"
product_path = "/home/javis/jd2017/jdata/JData_Product.csv"
user_path = "/home/javis/jd2017/jdata/JData_User.csv"

comment_date = ["2016/02/06", "2016/02/12", "2016/02/19", "2016/2/26", "2016/03/04", "2016/03/11", "2016/03/18",
                "2016/03/25", "2016/04/01",
                "2016/04/08", "2016/04/15"]


def convert_age(age_str):
    if age_str == u'-1':
        return 0
    elif age_str == u'15岁以下':
        return 1
    elif age_str == u'16-25岁':
        return 2
    elif age_str == u'26-35岁':
        return 3
    elif age_str == u'36-45岁':
        return 4
    elif age_str == u'46-55岁':
        return 5
    elif age_str == u'56岁以上':
        return 6
    else:
        return -1

def get_basic_user_feat():
    user = pd.read_csv(user_path, encoding='gbk')
    user['age'] = user['age'].map(convert_age)
    age_df = pd.get_dummies(user["age"], prefix="age")
    sex_df = pd.get_dummies(user["sex"], prefix="sex")
    user_lv_df = pd.get_dummies(user["user_lv_cd"], prefix="user_lv_cd")
    user = pd.concat([user['user_id'], age_df, sex_df, user_lv_df], axis=1)
    user.to_csv("/home/javis/jd2017/lwb/jd1/jd/cache/basicuser_feat")

def get_basic_product_feat():
    product = pd.read_csv(product_path)
    attr1_df = pd.get_dummies(product["a1"], prefix="a1")
    attr2_df = pd.get_dummies(product["a2"], prefix="a2")
    attr3_df = pd.get_dummies(product["a3"], prefix="a3")
    product = pd.concat([product[['sku_id', 'cate', 'brand']], attr1_df, attr2_df, attr3_df], axis=1)
    product.to_csv("/home/javis/jd2017/lwb/jd1/jd/cache/basicproduct_feat")

#dump_path = u'/home/javis/jd2017/jdata/action8.csv' % (start_date, end_date)

def get_action_feat(start_date, end_date):
    actions = get_actions(start_date, end_date)
    actions = actions[['user_id', 'sku_id', 'type']]
    df = pd.get_dummies(actions['type'], prefix='%s-%s-action' % (start_date, end_date))
    actions = pd.concat([actions, df], axis=1)  # type: pd.DataFrame
    actions = actions.groupby(['user_id', 'sku_id'], as_index=False).sum()
    del actions['type']
    actions.to_csv("/home/javis/jd2017/lwb/jd1/jd/cache/basic_action_feat")

def get_comments_product_feat(start_date, end_date):
    comments = pd.read_csv(comment_path)
    comment_date_end = end_date
    comment_date_begin = comment_date[0]
    for date in reversed(comment_date):
        if date < comment_date_end:
            comment_date_begin = date
            break
    comments = comments[(comments.dt >= comment_date_begin) & (comments.dt < comment_date_end)]
    df = pd.get_dummies(comments['comment_num'], prefix='comment_num')
    comments = pd.concat([comments, df], axis=1) # type: pd.DataFrame
        #del comments['dt']
        #del comments['comment_num']
    comments = comments[['sku_id', 'has_bad_comment', 'bad_comment_rate', 'comment_num_1', 'comment_num_2', 'comment_num_3', 'comment_num_4']]
    comments.to_csv("/home/javis/jd2017/lwb/jd1/jd/cache/comments_feat")
    

def make_train_set(train_start_date, train_end_date, test_start_date, test_end_date, days=30):
    start_days = "2016/02/05"
    user = get_basic_user_feat()
    product = get_basic_product_feat()
    product_acc = get_accumulate_product_feat(start_days, train_end_date)
    comment_acc = get_comments_product_feat(train_start_date, train_end_date)

    # generate 时间窗口
    # actions = get_accumulate_action_feat(train_start_date, train_end_date)
    actions = None
    for i in (1, 2, 3, 5, 7, 10, 15, 21, 30):
        start_days = datetime.strptime(train_end_date, '%Y/%m/%d') - timedelta(days=i)
        start_days = start_days.strftime('%Y/%m/%d')
        if actions is None:
            actions = get_action_feat(start_days, train_end_date)
        else:
            actions = pd.merge(actions, get_action_feat(start_days, train_end_date), how='left',
                                on=['user_id', 'sku_id'])

    actions = pd.merge(actions, user, how='left', on='user_id')
    actions = pd.merge(actions, user_acc, how='left', on='user_id')
    actions = pd.merge(actions, product, how='left', on='sku_id')
    actions = pd.merge(actions, product_acc, how='left', on='sku_id')
    actions = pd.merge(actions, comment_acc, how='left', on='sku_id')
    actions = actions.fillna(0)

    users = actions[['user_id', 'sku_id']].copy()
    del actions['user_id']
    del actions['sku_id']

    return users, actions,

def make_test_set(train_start_date, train_end_date):
    start_days = "2016/02/05"
    user = get_basic_user_feat()
    product = get_basic_product_feat()
    product_acc = get_accumulate_product_feat(start_days, train_end_date)
    comment_acc = get_comments_product_feat(train_start_date, train_end_date)
        #labels = get_labels(test_start_date, test_end_date)

        # generate ʱ�䴰��
        # actions = get_accumulate_action_feat(train_start_date, train_end_date)
    actions = None
    for i in (1, 2, 3, 5, 4, 5, 6, 7):
        start_days = datetime.strptime(train_end_date, '%Y/%m/%d') - timedelta(days=i)
        start_days = start_days.strftime('%Y/%m/%d')
        if actions is None:
            actions = get_action_feat(start_days, train_end_date)
        else:
            actions = pd.merge(actions, get_action_feat(start_days, train_end_date), how='left',
                                on=['user_id', 'sku_id'])

    actions = pd.merge(actions, user, how='left', on='user_id')
    actions = pd.merge(actions, product, how='left', on='sku_id')
    actions = pd.merge(actions, product_acc, how='left', on='sku_id')
    actions = pd.merge(actions, comment_acc, how='left', on='sku_id')
    #actions = pd.merge(actions, labels, how='left', on=['user_id', 'sku_id'])
    actions = actions.fillna(0)
    actions = actions[actions['cate'] == 8]

if __name__ == '__main__':
    train_start_date = '2016/04/02'
    train_end_date = '2016/04/08'
    test_start_date = '2016/04/09'
    test_end_date = '2016/04/15'
    user, action= make_train_set(train_start_date, train_end_date, test_start_date, test_end_date)





