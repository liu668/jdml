import pandas as pd
import csv
import os
import pickle

def get_rate_feat(start_date, end_date):
    feature = ['sku_id', 'a_rate_max_type4_1', 'a_rate_max_type4_2', 'a_rate_max_type4_3',
               'a_rate_max_type4_5', 'a_rate_max_type4_6']
    dump_path = './cache/product_feat_accumulate_%s_%s.pkl' % (start_date, end_date)
    if os.path.exists(dump_path):
        actions = pickle.load(open(dump_path))
    else:
        actions = get_actions(start_date, end_date)
        df = pd.get_dummies(actions['type'], prefix='action')
        actions = pd.concat([actions['sku_id'], df], axis=1)
        actions = actions.groupby(['sku_id'], as_index=False).sum()
        actions['a_rate_max_type4_1'] = actions['action_4'] / actions['action_1']
        actions['a_rate_max_type4_2'] = actions['action_4'] / actions['action_2']
        actions['a_rate_max_type4_3'] = actions['action_4'] / actions['action_3']
        actions['a_rate_max_type4_5'] = actions['action_4'] / actions['action_5']
        actions['a_rate_max_type4_1'] = actions['action_4'] / actions['action_6']
        actions = actions[feature]
        pickle.dump(actions, open(dump_path, 'w'))
    return actions



#���û�  A      min���µ���/������� 
a_rate_min_type4_1=

#���û�  A      min���µ���/�ӹ����� 
a_rate_min_type4_2=

#���û�  A      min���µ���/ɾ������ 
a_rate_min_type4_3=

#���û�  A      min���µ���/��ע���� 
a_rate_min_type4_5=

#���û�  A      min���µ���/������� 
a_rate_min_type4_6=

#���û�  A      avg���µ���/������� 
a_rate_avg_type4_1

#���û�  A      avg���µ���/�ӹ����� 
a_rate_avg_type4_2

#���û�  A      avg���µ���/ɾ������ 
a_rate_avg_type4_3

#���û�  A      avg���µ���/��ע���� 
a_rate_avg_type4_5

#���û�  A      avg���µ���/������� 
a_rate_avg_type4_6

#���û�  A      median���µ���/������� 
a_rate_med_type4_1

#���û�  A      median���µ���/�ӹ����� 
a_rate_med_type4_2

#���û�  A      median���µ���/ɾ������ 
a_rate_med_type4_3

#���û�  A      median���µ���/��ע���� 
a_rate_med_type4_5

#���û�  A      median���µ���/������� 
a_rate_med_type4_6