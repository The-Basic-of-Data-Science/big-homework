str=input()
M=eval(str)
size=len(M)
ctd=[0]*size
res=0
i=0
j=0
k=0
while(i<size):
    if(ctd[i]==0):
        ctd[i]=1
        j=i
        while(j<size):
            k=j
            while(k<size):
                if(M[j][k]==1 and ctd[j]==1):
                    ctd[k]=1
                k+=1
            j=j+1
        res+=1
    i+=1
print(res)