# coding=utf-8
import pandas as pd
import lightgbm as lgb
def read_data():
    test = pd.read_csv('./data/test_516.csv')
    train = pd.read_csv('./data/train_516.csv')
    return train,test
train,test=read_data()
print '--------------------------------------------------------'

def pipeline():
    train_y = train.label
    print len(train_y[train_y==1]),len(train_y[train_y==0])
    train_x = train.drop(['label', 'user_id', 'sku_id'], axis=1)
    train_data = lgb.Dataset(train_x, label=train_y, feature_name=list(train_x.columns),silent=False)
    test_x  = test.drop(['user_id','sku_id'], axis=1)
    test_data = lgb.Dataset(test_x, feature_name=list(test_x.columns))

    print train_x.shape, test_x.shape

    param = {'objective': 'binary'}
    param['is_unbalance'] = 'true'
    param['metric'] = 'auc'
    bst = lgb.cv(param, train_data, num_boost_round=800, nfold=10, early_stopping_rounds=30)
    estimators = lgb.train(param, train_data, num_boost_round=len(bst['auc-mean']))
    estimators.save_model('./cache/lgb_model_comment.model')
    test['pred'] = estimators.predict(test_x)
    feat_imp = pd.Series(estimators.feature_importance()).sort_values(ascending=False)
    pd.DataFrame(feat_imp).to_csv('./cache/importance_model_comment.csv')
    test.to_csv('./cache/test516.csv', index=None)
if __name__ == "__main__":
    pipeline()
test=pd.read_csv('./cache/test516.csv')
submit=test[['user_id','sku_id','pred']]
submit.to_csv('./sub/516/pred_prob_comment516.csv',index=False)
def ismax(df):
    x=df['pred'].max()
    return df[df['pred']==x]
possible=submit.groupby('user_id')[['sku_id','pred']].apply(ismax).reset_index()
possible = possible.sort_values('pred', ascending=False)
possible=possible[:800]
possible['user_id']=possible.user_id.astype(int)
possible[['user_id','sku_id']].to_csv('./sub/516/submit_comment516.csv',index=False)

#特征重要度排序
importance=pd.read_csv('./cache/importance_model_comment.csv')
importance.columns=['id','important']
importance.to_csv('./cache/importance_model_comment.csv',index=False)
train0 = pd.read_csv('./data/train_516.csv')
train_x = train0.drop(['label', 'user_id', 'sku_id'], axis=1)
xyy=train_x.columns
xyy=pd.DataFrame(xyy)
xyy.to_csv('./cache/columns_name_model_1.csv')
importance=pd.read_csv('./cache/importance_model_comment.csv')
col=pd.read_csv('./cache/columns_name_model_1.csv')
col.columns=['id','name']
importance=pd.merge(importance,col,on='id')
importance.to_csv('./sub/516/importace_comment_sort516.csv',index=False)