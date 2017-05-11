import pandas as pd

pred=pd.read_csv('C:/Users/liu/Desktop/logistic_result.csv')
pred=pred.drop_duplicates('user_id')[['user_id','sku_id']]
pred.to_csv('C:/Users/liu/Desktop/logistic_result.csv',index=False)