file = open('Random Text.txt', 'r')

content = file.readlines()
outStr = ''

for i in range(len(content)):
    outStr += content[i]

outStr = outStr.replace('.', ' ')
outStr = outStr.replace(',', '')
outStr = outStr.replace(' ', '#')

print(outStr)
