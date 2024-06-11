def weight_table(n):
    t = [[0]*n for _ in range(n)]
    c = 0
    while c < n:
        i = 0
        while i+c < n:
            t[c][i+c], t[n-1][i+c], t[i+c][c], t[i+c][n-1] = c, c, c, c
            i += 1
        n -= 1
        c += 1
    return t


for row in weight_table(5):
    print(row)
