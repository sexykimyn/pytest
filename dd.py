print("---출력1---")
i_list = range(1,6)
for i in i_list:
    print('*' * i)
print("---출력2---")
for i in i_list:
    print(' ' * (5 - i) + '*' * i)
print("---출력3---")
n = 3
for i in range(1, n + 1):
    print(' ' * (n - i) + '*' * (2 * i - 1))
for i in range(n - 1, 0, -1):
    print(' ' * (n - i) + '*' * (2 * i - 1))