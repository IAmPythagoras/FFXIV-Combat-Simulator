x = [1,2,3]
remove = []
k = 0
a = len(x)
j = 0
while j+k < len(x):
    i = x[j + k]
    if i == 4: x.append(5)
    if i == 2:
        remove += [i]
    if i == 3:
        x.append(4)
    if a != len(x):
        #input("Len has changed : " + str(len(x)) + " : " + str(a))
        #input(x)
        if a > len(x):
            k-=1
            a = len(x)

    input(i)
    if j+k == len(x)-1 : break
    j+=1

for r in remove:
    x.remove(r)

print(x)

