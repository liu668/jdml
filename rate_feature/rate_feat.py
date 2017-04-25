# -*- coding:utf-8 -*-
import pandas as pd
import csv
import numpy as np
from datetime import date, datetime
from datetime import timedelta


action_path = "/home/javis/jd2017/jdata/JData_Action_201604.csv"
start_date="2016/4/2"
end_date="2016/4/8"
actions = pd.read_csv(action_path)
feature = ['user_id', 'a_rate_total_type4_1', 'a_rate_total_type4_2', 'a_rate_total_type4_3',
               'a_rate_total_type4_5', 'a_rate_total_type4_6']
actions = actions[(actions.time >= start_date) & (actions.time < end_date)]
df = pd.get_dummies(actions['type'], prefix='action')
actions = pd.concat([actions['user_id'], df], axis=1)
actions = actions.groupby(['user_id'], as_index=False).sum()
actions['a_rate_total_type4_1'] = actions['action_4'] / actions['action_1']
actions['a_rate_total_type4_2'] = actions['action_4'] / actions['action_2']
actions['a_rate_total_type4_3'] = actions['action_4'] / actions['action_3']
actions['a_rate_total_type4_5'] = actions['action_4'] / actions['action_5']
actions['a_rate_total_type4_6'] = actions['action_4'] / actions['action_6']
actions = actions[feature]
actions.to_csv("/home/javis/jd2017/jdata/totalRate_feat.csv")



