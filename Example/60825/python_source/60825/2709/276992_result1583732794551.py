def iii():
    s=input()
    row=-1
    for x in s:
        if x=='[':
            row+=1;
    s=s.replace('[','')
    s=s.replace(']','')
    s=s.replace(',',' ')
    l=s.split()
    l= list(map(int, l))

    gap=len(l)/row

    d1=[]
    for i in range(0, len(l), gap):
        dd=[]
        for j in range(gap):
            dd.append(l[i+j])
        d1.append(dd)

    return d1
def hitBricks(grid, hits):
    m,n = len(grid),len(grid[0])
    for i,j in hits:
        grid[i][j] -= 1
    flag = [[0]*n for i in range(m)]
    queue = []
    for j in range(n):
        flag[0][j] = 1
        if grid[0][j] == 1:
            queue.append((0,j))
    tmp = [(0,1),(1,0),(0,-1),(-1,0)]
    while queue:
        i,j = queue.pop(0)
        for di,dj in tmp:
            a,b = i+di,j+dj
            if 0<=a<m and 0<=b<n and grid[a][b] == 1 and not flag[a][b]:
                flag[a][b] = 1
                queue.append((a,b))
    res = []
    for i,j in hits[::-1]:
        grid[i][j] += 1
        remain = 0
        if grid[i][j] == 1:
            if i != 0:
                for di,dj in tmp:
                    a,b = i+di,j+dj
                    if 0<=a<m and 0<=b<n and grid[a][b] == 1 and flag[a][b]:
                        flag[i][j] = 1
                        break
            if flag[i][j]:
                queue = [(i,j)]
                while queue:
                    ii,jj = queue.pop(0)
                    for di,dj in tmp:
                        a,b = ii+di,jj+dj
                        if 0<=a<m and 0<=b<n and grid[a][b] == 1 and not flag[a][b]:
                            flag[a][b] = 1
                            remain += 1
                            queue.append((a,b))
        res.insert(0,remain)
    return res

d1=iii()
d2=iii()
print(hitBricks(d1,d2))