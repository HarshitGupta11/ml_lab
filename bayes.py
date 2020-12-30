import pandas as pd 
import numpy as np
from math import pi

class Distribution:

    def __init__(self):
        #initiate the distribution
        self.mean=0
        self.var=1
        self.const=np.sqrt(2*pi)

    def init_distribution(self,arr):
        #initiate the mean
        self.mean=np.mean(arr)
        #initiate the standard deviation
        self.var=np.std(arr)
        #initiate the constant of distribution
        self.const=self.const*self.var

    def calc_prob(self,x):
        #calc (x-mu)/sigma
        norm=(x-self.mean)/self.var
        #calc the exp
        prob=np.exp(-1*norm*norm/2)
        #get the final density of probability
        prob=prob/self.const
        return prob

def calc(df):
    #compute P(Y)
    #enumerate the all the different targets
    all_targs=dict(df["target"].value_counts())
    #initialize an empty dict
    prior={}
    for key in all_targs:
        #calcs the prior probability of the distribution
        prior[key]=all_targs[key]/len(df)
    
    #compute P(X) for all the features
    #gets the list of columns
    cols=list(df.columns)
    #remove the target column
    cols=cols[:-1]
    #initialize the individual dictionary to calculate the probability of all features.
    individual={}
    for col in cols:
        #initialize the distribution
        dist=Distribution()
        dist.init_distribution(np.array(df[col]))
        #store the object
        individual[col]=dist

    #compute P(X|Y) for all the features
    #likelihood measures the probability of the sample existing given the class
    likelihood={}
    for target in all_targs:
        #initialize the probability for likelihood for the given class
        likelihood[target]={}
        #selects all the records with same target
        tdf=df[df["target"]==target]
        for col in cols:
            dist=Distribution()
            #initiate the distribution given the class
            dist.init_distribution(np.array(tdf[col]))
            likelihood[target][col]=dist
        
    return likelihood,prior,individual

def get_class_prob(x,y,prior,likelihood,individual):
    #calculate P(X)
    p_x=1
    for feature in x:
        if feature=="target":
            continue
        #P(X)=P(X_1 & X_2.....X_N)=P(X_1)*P(X_2)...P(X_N) assuming feature independence
        p_x=p_x*individual[feature].calc_prob(x[feature])


    #calculate P(X|Y)
    p_x_y=1
    for feature in x:
        if feature=="target":
            continue
        p_x_y=p_x_y*likelihood[y][feature].calc_prob(x[feature])

    #implementation of the bayes theorm
    final_prob=prior[y]*p_x_y/p_x

    return final_prob

def classify(x,prior,likelihood,individual):
    print(x)
    #initiate empty dictionary for all the classes
    all_class={}
    #initiate a sum variable since we are measuring the probability over continuous distribution density can be greate than one
    s=0
    #iterate over classes
    for cl in prior:
        #get the class probability
        all_class[cl]=get_class_prob(x,cl,prior,likelihood,individual)
        #add it to sum variable for normalizing
        s+=all_class[cl]
    
    #normalize the class probability
    for cl in prior:
        all_class[cl]/=s
    #print the decision
    print(all_class)

def main():
    #read the dataset
    df=pd.read_csv("naive.csv")
    #rename the last column as target
    cols=list(df.columns)
    cols[-1]="target"
    df.columns=cols
    #print the head of dataset
    print(df.head(10))
    #initiate the classifier
    likelihood,prior,individual=calc(df)
    #classify all the rows once again we can add specific addtions as well :)
    for index,row in df.iterrows():
        classify(dict(row),prior,likelihood,individual)  
        
if __name__=="__main__":
    main()
    
            

