a = int(input())
count = 0
j = []
l = []
r = []
d = []
u = []
for i in range(a):
    n, m = input().split()
    j.append(n)
    if n == 'L':
        l.append(int(m))
    elif n == 'R':
        r.append(int(m))
    elif n == 'D':
        d.append(int(m))
    elif n == 'U':
        u.append(int(m))
if ('L' not in j or 'R' not in j) and ('U' not in j or 'D' not in j):
    count = a
elif 'L' not in j or 'R' not in j:
    count += len(l) + len(r)
    u1 = min(u)
    d1 = max(d)
    u += d
    u.sort()
    for i in u:
        if u1 <= i and i <= d1:
            count += 1
elif 'U' not in j or 'D' not in j:
    count += len(u) + len(d)
    l1 = min(l)
    r1 = max(r)
    l += r
    l.sort()
    for i in l:
        if r1 <= i and i <= l1:
            count += 1
else:
    l1,r1,u1,d1 = max(l),min(r),min(u),max(d)
    l += r
    u += d
    l.sort()
    u.sort()
    for i in l:
        if r1 <= i and i <= l1:
            count += 1
    for i in u:
        if u1 <= i and i <= d1:
            count += 1
print(count)