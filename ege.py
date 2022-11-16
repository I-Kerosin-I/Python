from itertools import product
k = []
for i in product('авеикнор', repeat=3):
    if i.count('в') == 1:
        k.append(''.join(i))
for i in range(len(k)):
    if 'а' not in k[i]:
        print(i+1)
        break