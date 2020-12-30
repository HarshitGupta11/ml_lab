import pandas as pd 
import numpy as np 
from math import log2 

class Node():
    def __init__(self,c,a,t="NA"):
        self.col_name=c
        self.attr=a
        self.children=[]
        self.ta=t


def calc_entropy(df):
    #get the value counts of each class
    all_v=dict(df.target.value_counts())
    tot=len(df)
    for key in all_v:
        all_v[key]/=tot
    ent=0
    for key in all_v:
        if all_v[key]!=0:
            ent+=(all_v[key]*log2(all_v[key]))
    return -ent

def calc_max_entropy_column(df):
    #print(df)
    ent_org=calc_entropy(df)
    entropies=[]
    cols=list(df.columns)[:-1]
    for c in cols:
        new_ent=0
        for val in list(df[c].unique()):
            tdf=df[df[c]==val]
            new_ent+=(len(tdf)/len(df))*calc_entropy(tdf)
        entropies.append(new_ent)
    print(entropies)
    print(ent_org)
    return cols[entropies.index(min(entropies))],ent_org-min(entropies)

def build(df,root):
    #print(df)
    if len(df.target.unique())==1:
        root.ta=df.iloc[0].target
        return

    col,inf_gain=calc_max_entropy_column(df)
    print("Best Split is:{}\nInformation Gain:{}".format(col,inf_gain))
    uni=list(df[col].unique())
    for k in uni:
        tdf=df[df[col]==k]
        tdf=tdf.drop(columns=col)
        new_node=Node(col,k)
        build(tdf,new_node)
        root.children.append(new_node)    
    return

def print_node(node):
    print(node.col_name,node.attr,node.ta)
    for chld in node.children:
        print_node(chld)
    return    

def classify(v,root):
    print(root.col_name)
    if len(root.children)==0 and root.col_name!="Root":
        #print_node(root)
        print("Leaf Reached")
        print(root.ta)
        return 1

    ret=0

    for key in v:
        #print(key)
        for chld in root.children:
            #print(chld.col_name)
            if chld.col_name==key and chld.attr==v[key]:
                ret=classify(v,chld) 
                if ret==1:
                    break

        if ret:
            break
    return ret
    
def main():
    df=pd.read_csv("df.csv")
    cols=list(df.columns)
    cols=cols[1:]+[cols[0]]
    df=df[cols]
    ls=list(df.columns)
    ls[-1]="target"
    df.columns=ls
    print(df)
    r=Node("Root","Root") 
    try:
        build(df,r)
    except:
        print("Ambiguos Data:(")
        return
    ls=ls[:-1]
    #vals={x:0 for x in ls}
    #for key in vals:
        #vals[key]=input(key+":")
    print_node(r)
    for i in range(len(df)):
        vals=dict(df.loc[i])
        print(vals)
        classify(vals,r) 
        if i==10:
            break       

if __name__=="__main__":
    main()

