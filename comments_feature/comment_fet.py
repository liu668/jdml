#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import time
from datetime import datetime
from datetime import timedelta
import pandas as pd
import numpy as np

comment_path = "H:/anaconda/JD/JData_Comment.csv"
start_date="2016/4/2"
end_date="2016/4/8"
comments = pd.read_csv(comment_path)
comment_date_end = end_date
comment_date_begin = start_date
for date in reversed(start_date):
    if date < comment_date_end:
        comment_date_begin = date
        break
comments = comments[(comments.dt >= comment_date_begin) & (comments.dt < comment_date_end)]
df = pd.get_dummies(comments['comment_num'], prefix='comment_num')
comments1 = pd.concat([comments, df], axis=1) # type: pd.DataFrame
#del comments['dt']
#del comments['comment_num']
comments_fet = comments1[['sku_id', 'has_bad_comment', 'bad_comment_rate', 'comment_num_1', 'comment_num_2', 'comment_num_3', 'comment_num_4']]
comments_fet.to_csv("H:/anaconda/JD/data/comments_fet.csv")




