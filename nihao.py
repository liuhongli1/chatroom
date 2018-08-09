from time import sleep
words = input('输入你最在乎的人姓名：')
print(words,'做我女朋友好么？')

for item in words.split():
    letterlist = []
    for y in range(12,-12,-1):
        lisst_X = []
        letters = ''
        for x in range(-30,30):
            expression = ((x*0.05)**2+(y*0.1)**2-1)\
            **3-(x*0.05)**2*(y*0.1)**3
            if expression <= 0:
                letters +=item[(x-y)%len(item)]
            else:
                letters +=' '
        lisst_X.append(letters)
        letterlist+=lisst_X
        # print(lisst_X)
        print('\n'.join(lisst_X))
        sleep(0.1)
    # print('\n'.join(letterlist))
    # sleep(0.5)