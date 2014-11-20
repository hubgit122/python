import random

for j in range(1000):
    for i in range(0,5):
        k = random.randint(0,3)
        if(k==0): print 'A',
        elif(k==1): print 'B',
        elif(k==2): print 'C',
        else: print 'D',
        
    print
        
            