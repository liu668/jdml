import pandas as pd

pred=pd.read_csv('C:/Users/Administrator/Desktop/logistic_result2.csv')
pred=pred.drop_duplicates('user_id')[['user_id','sku_id']]
pred.to_csv('C:/Users/Administrator/Desktop/logistic_result2.csv',index=False)