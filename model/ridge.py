from sklearn import linear_model
import numpy as np
from aifc import data
import matplotlib.pyplot as plt  

def test_Ridge(*data):
    x_train,x_test,y_train,y_test=data
    regr=linear_model.Ridge()
    regr.fit(x_train,y_train)
    print'Coefficients:%s,intercept %.2f'%(regr.coef_,regr.intercept_)
    print"Residual sum of squares: %.2f"% np.mean((regr.predict(x_test)-y_test)**2)
    print'Score:%.2f'%regr.score(x_test,y_test)
 
 
def test_Ridge_alpha(*data):
    x_train,x_test,y_train,y_test=data
    alphas=[0.01,0.02,0.05,0.1,0.2,0.5,1,2,5,10,20,50,100,200,500,1000]
    scores=[]
    for i,alpha in enumerate(alphas):
        regr=linear_model.Ridge(alpha=alpha)
        regr.fit(x_train,y_train)
        scores.append(regr.score(x_test,y_test))
    fig=plt.figure()
    ax=fig.add_subplot(1,1,1)
    ax.plot(alphas,scores) 
    ax.set_xlabel(r"$\alpha$")
    ax.set_ylabel(r"score")
    ax.set_xscale('log')
    ax.set_title("Ridge")
    plt.show 

if __name__ == '__main__':
    x_train,x_test,y_train,y_test=data
    test_Ridge(x_train,x_test,y_train,y_test)
    test_Ridge_alpha(x_train,x_test,y_train,y_test)