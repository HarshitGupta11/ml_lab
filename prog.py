import pandas as pd 
import numpy as np
from math import pi

class Distribution:

    def __init__(self):
        self.mean=0
        self.var=1
        self.const=np.sqrt(2*pi)

    def init_distribution(self,arr):
        self.mean=np.mean(arr)
        self.var=np.std(arr)
        self.const=self.const*self.var

    def calc_prob(self,x):
        norm=(x-self.mean)/self.var
        prob=np.exp(-1*norm*norm/2)
        prob=prob/self.const
        return prob

def calc(df):
    all_targs=dict(df["target"].value_counts())
    prior={}
    for key in all_targs:
        prior[key]=all_targs[key]/len(df)    

    cols=list(df.columns)
    cols=cols[:-1]
    individual={}
    for col in cols:
        dist=Distribution()
        dist.init_distribution(np.array(df[col]))
        individual[col]=dist

    likelihood={}
    for target in all_targs:
        likelihood[target]={}
        tdf=df[df["target"]==target]
        for col in cols:
            dist=Distribution()
            dist.init_distribution(np.array(tdf[col]))
            likelihood[target][col]=dist
        
    return likelihood,prior,individual

def get_class_prob(x,y,prior,likelihood,individual):
    p_x=1
    for feature in x:
        if feature=="target":
            continue
        p_x=p_x*individual[feature].calc_prob(x[feature])

    p_x_y=1
    for feature in x:
        if feature=="target":
            continue
        p_x_y=p_x_y*likelihood[y][feature].calc_prob(x[feature])

    final_prob=prior[y]*p_x_y/p_x

    return final_prob

def classify(x,prior,likelihood,individual):
    all_class={}
    s=0
    for cl in prior:
        all_class[cl]=get_class_prob(x,cl,prior,likelihood,individual)
        s+=all_class[cl]
    
    for cl in prior:
        all_class[cl]/=s
    return all_class

def main():
    df=pd.read_csv("ml_lab.csv",header=None)
    ls=list(df.columns)
    ls[-1]="target"
    df.columns=ls
    print(df.head(10))
    likelihood,prior,individual=calc(df)
    acc_pos=0
    acc_neg=0
    for index,row in df.iterrows():
        preds=classify(dict(row),prior,likelihood,individual)  
        actual=row["target"]
        max_prob=0
        pred=""
        for cl in preds:
            if preds[cl]>max_prob:
                max_prob=preds[cl]
                pred=cl
        if pred==actual and pred==1:
            acc_pos+=1
        if pred==actual and pred==0:
            acc_neg+=1
        
    count_actual_pos=len(df[df["target"]==1])
    count_actual_neg=len(df)-count_actual_pos

    print("Precision:{}".format((acc_pos+acc_neg)/len(df)))
    print("Recall:{}".format((count_actual_pos-acc_pos)/count_actual_pos))
    confusion_matrix=[
        [acc_pos,count_actual_pos-acc_pos],
        [acc_neg,count_actual_neg-acc_neg]
    ]
    print(confusion_matrix)
    return 

        
if __name__=="__main__":
    main()
    
            

