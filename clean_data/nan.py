import pandas as pd
import numpy as np

action=pd.read_csv('/home/javis/jd2017/jdata/all_test_new429.csv')
action1=action.fillna(0,inplace=True)
action1.to_csv('/home/javis/jd2017/jdata/all_test_new429.csv')
