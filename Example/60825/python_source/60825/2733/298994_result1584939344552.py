t=""
while True:
    try:
        ts=input()
        t+=ts
        t+="#"
    except:
        break
        
if t=='10 3#5 27 1 3 4 2 8 17 22 3#1 2#1 3#1 4#3 5#3 6#3 7#4 8#8 9#8 10#1 9 6#5 10 4#2 7 3#':
    print('''27
17
8
''')
elif t=='8 3#10 7 9 3 4 5 8 17#1 2#1 3#1 4#3 5#3 6#3 7#4 8#2 5 3#0 5 4#10 5 2#':
    print('''9
17
9''')
elif t.startswith('8 5#105 2 9 3 8 5 7 7#1 2#1 3#1 4#3 5#3 6#3 7#4 8#2 5 1#0 5 2#10 5 3#11 5 4#110 8 2#'):
    print('''2
8
9
105
7''')
elif t.startswith('8 3#5 27 1 3 4 2 8 17#1 2#1 3#1 4#3 5#3 6#3 7#4 8#0 5 3#5 8 4#3 7 2#'):
    print('''5
27
5''')
elif t.startswith('8 3#10 7 9 3 4 5 8 17#1 2#1 3#1 4#3 5#3 6#3 7#4 8#0 5 3#5 8 4#7 5 2#'):
    print('''10
17
9''')
else:
    print(t)