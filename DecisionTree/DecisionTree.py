# -*- coding:utf-8 -*-
from sklearn.tree import DecisionTreeRegressor  
from sklearn.ensemble import RandomForestRegressor 
from sklearn.cross_validation import cross_val_score, ShuffleSplit  
import numpy as np  
   
from sklearn.datasets import load_iris  
iris=load_iris()   
print iris['target'].shape  
rf=RandomForestRegressor()
rf.fit(iris.data[:150],iris.target[:150])
instance=iris.data[[100,109]]  
print instance  
print 'instance 0 prediction;',rf.predict(instance[0])  
print 'instance 1 prediction;',rf.predict(instance[1])  
print iris.target[100],iris.target[109]  

 
X = iris["data"]  
Y = iris["target"]  
names = iris["feature_names"]  
rf = RandomForestRegressor()  
scores = []  
for i in range(X.shape[1]):  
     score = cross_val_score(rf, X[:, i:i+1], Y, scoring="r2",  
                              cv=ShuffleSplit(len(X), 3, .3))  
     scores.append((round(np.mean(score), 3), names[i]))  
print sorted(scores, reverse=True)  
