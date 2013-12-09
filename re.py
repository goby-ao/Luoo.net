import re
import os
'''
f = open('luoo.txt')
output = file('name.txt','w')
lines = f.readlines()
n = 0
length = len(lines)
x = 0
while (x >= 0):
    name = re.findall(r'VOL.*?(?=\<)',lines[x])
    if name == []:
                x += 2
                continue
    print name[0].decode('utf-8')
    x += 2  
    output.write(name[0])
    output.write('\n')

'''
f = open('nameeee.txt')
lines = f.readlines()
a = lines[2]
name = "%s " % lines[2]
path = 'd:\\Luoo.net'
path = path + '\\' + a
os.mkdir(path)
'''
output = file('nameeee.txt','w')
x = len(lines) - 1
results = []
while(x >= 0 ):
        result = "%s" % lines[x]
        output.write(result)
        x = x - 1

'''
