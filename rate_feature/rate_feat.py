# -*- coding:utf-8 -*-
import pandas as pd
import csv
import numpy as np
from datetime import date, datetime
from datetime import timedelta

actions=pd.read_csv("H:/anaconda/JD/JData_Action_201604")
def get_actions(start_date, end_date):
    """

    :param start_date:
    :param end_date:
    :return: actions: pd.Dataframe
    """

    feature = ['sku_id', 'a_rate_total_type4_1', 'a_rate_total_type4_2', 'a_rate_total_type4_3',
                'a_rate_total_type4_5', 'a_rate_total_type4_6']
    actions = get_actions(start_date, end_date)
    actions = actions[(actions.time >= start_date) & (actions.time < end_date)]
    df = pd.get_dummies(actions['type'], prefix='action')
    actions = pd.concat([actions['sku_id'], df], axis=1)
    actions = actions.groupby(['sku_id'], as_index=False).sum()
    actions['a_rate_total_type4_1'] = actions['action_4'] / actions['action_1']
    actions['a_rate_total_type4_2'] = actions['action_4'] / actions['action_2']
    actions['a_rate_total_type4_3'] = actions['action_4'] / actions['action_3']
    actions['a_rate_total_type4_5'] = actions['action_4'] / actions['action_5']
    actions['a_rate_total_type4_6'] = actions['action_4'] / actions['action_6']
    actions_fet = actions[feature]
    actions_fet.to_csv("H:/anaconda/JD/data")
if __name__ == '__main__':
    start_date="2016/4/2"
    end_date="2016/4/8"
    get_actions(start_date, end_date)

