from random import Random,randint, random
import math

#inNum=int(raw_input("How many inputs:"))
#outNum=int(raw_input("How many outputs:"))
#layerNum=int(raw_input("Layers of net:"))
#TLU_Num=inNum#int(raw_input("TLUs in each layer:"))

#if raw_input("use built-in trainingSet?(y/n)")=='n':
    #m=int(raw_input("rows of trainingSet:"))
    #n=inNum+1
    #trainingSet=[];
    #temp=[];
    #for i in range(0,m):
        #for j in range(0,n):
            #temp.append(int(raw_input("input trainingSet[%d][%d]"%(i,j))))
        #trainingSet.append(temp)
        #temp=[];
    #print "trainingSet\n",trainingSet
#else:
    #trainingSet=[[1,0,0,1],[0,1,1,0],[1,1,0,1],[1,1,1,0],[0,0,1,0],[1,0,1,1]]
    #print "trainingSet\n",trainingSet

#weightVector=[]
#temp=[]
#temp_=[]
#temp__=[]
#if raw_input("use zeros weightVector?(y/n)")=='n':
    #for i in range(0,outNum):
        #for j in range(0,layerNum):
            #for k in range(0,TLU_Num):
                #for l in range(0,len(trainingSet[0])-1):
                    #temp__.append(float(raw_input("the No. %d component of No. %d weightVector of Net %d, layer %d "%(l,k,i,j))))
                #temp_.append(temp__)
                #temp__=[]
            #temp.append(temp_)
            #temp_=[]
        #weightVector.append(temp)
        #temp=[]
    #print "weightVector\n",weightVector
#else:
    #for i in range(0,outNum):
        #for j in range(0,layerNum):
            #for k in range(0,TLU_Num):
                #for l in range(0,len(trainingSet[0])-1):
                    #temp__.append(float(0))
                #temp_.append(temp__)
                #temp__=[]
            #temp.append(temp_)
            #temp_=[]
        #weightVector.append(temp)
        #temp=[]
    #print "weightVector\n",weightVector

#def s(weightVector,inPuts):
    #if len(inPuts)!=len(weightVector)-1:
        #return None
    #else:
        #temp=0
        #for i in range(0,len(inPuts)):
            #temp=weightVector[i]*inPuts[i]
        #temp=temp-weightVector[-1]
        #return temp>0;

#def f(weightVector,inPuts):
    #global inNum
    #global outNum
    #global layerNum
    #global TLU_Num
    #result=[]
    #inPuts_=inPuts
    #inPuts__=[]
    #for i in range(0,outNum):
        #for j in range(0,layerNum):
            #for k in range(0,TLU_Num):
                #inPuts__[k]=s(weightVector[i][j][k],inPuts_)
            #inPuts_=inPuts__
        #result.append()

def s(W,X):
    if len(X)!=len(W)-1:
        return None
    else:
        temp=0
        for i in range(0,len(X)):
            temp=temp+W[i]*X[i]
        temp=temp+W[-1]
        return temp;

def f(weightVector,inPuts):
    if s(weightVector,inPuts)>1000.0:
        return 0
    elif s(weightVector,inPuts)<-1000.0:
        return 1
    else:
        return 1/(1+math.exp(-s(weightVector,inPuts)))

def test(trainnigSet):
    global W
    for i in range(0,len(trainingSet)):
        if (s(W,trainingSet[i][0:-1])>0)!=trainingSet[i][-1]:
            #print i+1,"Vector(s) Matched, but vetor",trainingSet[i],"not matched! "
            return False
    else:
        print i,"Vectors Matched!"
        return True

#----------------------------------------------------------------------
def  resize(V):
    """"""
    temp=0
    for i in range(0,len(V)):
        temp+=V[i]*V[i]
    temp=math.sqrt(temp)
    if temp>0:
        for i in range(0,len(V)):
            V[i]/=temp
    return V

def train(W,trainingVector):
    learnCoefficient= 0.01
    out=f(W,trainingVector[0:-1])
    for i in range(0,len(W)-1):
        W[i]=W[i]+learnCoefficient*(trainingVector[-1]-out)*out*(1-out)*trainingVector[i]
    W[-1]=W[-1]+learnCoefficient*(trainingVector[-1]-out)*out*(1-out)
    
    W=resize(W)
    return W

inNum=3
if raw_input("use built-in trainingSet?(y/n)")=='n':
    m=int(raw_input("rows of trainingSet:"))
    n=inNum+1
    trainingSet=[];
    for i in range(0,m):
        for j in range(0,n):
            trainingSet.append(int(raw_input("input trainingSet[%d][%d]"%(i,j))))
    print "trainingSet\n",trainingSet
else:
    trainingSet=[[1,0,0,1],[0,1,1,0],[1,1,0,1],[1,1,1,0],[0,0,1,0],[1,0,1,1]]
    #trainingSet=[[1,0,0,1],[0,1,1,0],[1,1,0,1],[1,1,1,0],[0,0,1,0],[1,0,1,1]]
    print "trainingSet\n",trainingSet

W=[]
if raw_input("use zeros weightVector?(y/n)")=='n':
    for l in range(0,len(trainingSet[0])):
        W.append(float(raw_input("the No. %d component of No. %d weightVector of Net %d, layer %d "%(l,k,i,j))))
else:
    #for l in range(0,len(trainingSet[0])):
        #W.append(float(random()))
    #W=[-1.0,-1.0,20,10]
    W=[0,0,0,0]
resize(W)
print "weightVector\n",W

while test(trainingSet)==False:
    ran=randint(0,len(trainingSet)-1)
    print "trainingVector",trainingSet[ran]
    W=train(W,trainingSet[ran])
    print "weightVector after training",W
print "weightVector after training",W
#for i in range(0,len(trainingSet)):#test(trainingSet)==False:
    ##ran=randint(0,len(trainingSet)-1)
    ##print "trainingVector",trainingSet[ran]
    #print "trainingVector",trainingSet[i]
    #weightVector=train(weightVector,trainingSet[i])
    #print "weightVector after training",weightVector
    ##i+=1
    ##i%=len(trainingSet)
