str=input()
nums=list(map(int,str[1:len(str)-1].split(",")))
len=len(nums)
countA=0
countB=0
for i in range(0,len):
    if(countA==0|a==nums[i]):
        a=nums[i]
        countA+=1
    else if(countB==0|b==nums[i]):
        b=nums[i]
        countB+=1
    else:
        countA--
        countB--
countA=0
countB=0
for i in range(0,len):
    if(nums[i]==a):
        countA+=1
    if(nums[i]==b):
        countB+=1
if(countA>len/3&&countB>len/3):
    print([a,b])
else if(countA>len/3):
    print([a])
else:
    print([b])
        