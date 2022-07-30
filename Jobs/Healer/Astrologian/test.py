def f(x,b):
    return x + b

def g(x):
    return f(x, "a")

g = f(x,b = "hey")

print(g("a"))