def f(x):
    return x

a = [f]
print(a[0] == f)
a.remove(f)