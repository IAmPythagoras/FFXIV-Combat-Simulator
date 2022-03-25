from tkinter import Y


class test():
    def __init__(self):
        self.x = 2

y = test()

z = 2*y.x

y.x = 0

print(z)