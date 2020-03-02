# 汉诺塔递归实现
def move(n, a, b, c):
    if n == 1:
        print(a, "-->", c)
    else:
        move(n - 1, a, c, b)
        print(a, "-->", c)
        move(n - 1, b, a, c)


print(move(4, 'A', 'B', 'C'))
