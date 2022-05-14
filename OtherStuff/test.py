l = ["a", "b", "c"]
i = 0
k = 0
while True:
    if l[i] == "b" and k != 5:
        l.insert(i, "d")
    print(l[i])
    input(l)
    i+=1
    k+=1