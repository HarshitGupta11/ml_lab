import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt

class Hidden_Layer:
    def __init__(self,inp,out):
        #input size of the hidden layer
        self.input_size=inp
        #outout size of the hidden layer
        self.output_size=out
        #the input buffer used to calc the local gradient
        self.fwi=np.random.rand(inp)
        #layer weight matrix (dimensions already transposed)
        self.w=np.random.rand(out,inp)
        #bias for the layer weights
        self.b=np.random.rand(out)

    def forward(self,x):
        #store the forward buffer
        self.fwi=x
        ret=[]
        for sample in x:
            #output = wTx + b
            ret.append(np.matmul(self.w,sample)+self.b)
        return ret

    def back_prop(self,grad,step):
        #calc the local gradient
        #wTx+b
        #out * 1 @ 1 * input
        #initialize an empty zero array in the size of weight matrix
        lgw=np.zeros((self.output_size,self.input_size))
        for sample in self.fwi:
            #delta(W) = delta(stream) @ xT
            lgw+=np.matmul(grad.reshape((self.output_size,1)),sample.reshape((1,self.input_size)))
        #renormalize the update with sample length
        lgw=lgw/len(self.fwi)
        #negative gradient step
        self.w=self.w-step*lgw
        self.b=self.b-step*grad

        #calc the global gradient
        #grad = W @ delta
        sgw=np.matmul(self.w.T,grad.reshape(self.output_size))
        return sgw

class Sigmoid_Layer:
    def __init__(self):
        self.s="Sig"

    def forward(self,x):
        ret=[]
        for sample in x:
            ret.append(np.exp(sample)/(1+np.exp(sample)))
        return ret

    def back_prop(self,grad,step=0):
        #the sigmoid function becomes flat after +4 and -4 so as to prevent exploding gradient we will clip it
        for i in range(len(grad)):
            grad[i]=min(grad[i],4)
            grad[i]=max(grad[i],-4)
        #calc the sigmoid function
        temp=(np.exp(grad)/(1+np.exp(grad)))
        #calc the grdient
        sgw=temp*(1-temp)
        return sgw

def RMSE(targ,y):
    #calculate the Root Mean Squared Error in the network
    err=((targ-y)**2)
    return np.sqrt(np.sum(err))/len(targ)

def forward(layers,x):
    for ly in layers:
        x=ly.forward(x)
    return x

def backward(layers,err):
    #reverse the layers only a reference is revrsed the layer object remains same
    rev_layers=layers[::-1]
    grad=err
    for ly in rev_layers:
        #back prop the error with learning rate
        grad=ly.back_prop(grad,1e-2)
    return

def main():
    df=pd.read_csv("reg.csv")
    #drop the date columns
    df=df.drop(columns="date")
    print(df.head())
    data=np.array(df)
    data=data[:,:-1]
    #select the first 5000 training samples
    data=data[0:5000]
    #renormalize the data helps in better optimization
    for i in range(len(data[0])):
        data[:,i]=(data[:,i]-np.mean(data[:,i]))/np.std(data[:,i])
    x=data[:,:-1]
    print(x.shape)
    y=data[:,-1]
    print(y.shape)
    #initialize the neural network/ multi-layered perceptron the layers can be changed as per convinience
    layers=[Hidden_Layer(len(x[0]),100),
            Sigmoid_Layer(),
            Hidden_Layer(100,30),
            Sigmoid_Layer(),
            Hidden_Layer(30,10),
            Sigmoid_Layer(),
            Hidden_Layer(10,1)]
    reps=100000
    errors=[]
    for i in range(reps):
        #feed the data forward in the network, final_value is also known as y_dash
        final_value=forward(layers,x)
        #calculate the error
        err=RMSE(y,final_value)
        #if the loss function diverges break the loop
        if i!=0 and err > errors[-1]:
            break
        errors.append(err)
        print("Error",err)
        #backpropogate the error
        backward(layers,err)
    #plot the errors
    plt.plot(errors)
    plt.show()
    return    

if __name__=="__main__":
    main()

