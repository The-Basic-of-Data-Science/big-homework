nums=int(input())
inputStr=[" "]*nums
for i in range(0,nums):
    inputStr[i]=input()

cdn=inputStr
x_base=eval(cdn[1])[0]-eval(cdn[0])[0]
y_base=eval(cdn[1])[1]-eval(cdn[0])[1]
print(x_base," ",y_base)
print(cdn)
firstPoint=eval(cdn[0])
res=True
for i in cdn:
    i=eval(i)
    if((i[0]-firstPoint[0])%x_base!=0 or (i[1]-firstPoint[1])%y_base!=0):
        res=False
        break;
print(res)