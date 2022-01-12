from utils.ReadFile import ReadFile
from utils.ETF import ETF

if __name__ == '__main__':
    File = ReadFile('S&P_TR.xlsx')
    data = File.ReadData()
    d = data['B']
    num = len(d)
    close = [item.value for item in d[1:num]]
    yst = []
    feature25 = []
    ETFdata = ETF(close)
    for i in range(120,num-1):
        yst.append(ETFdata.posinegaCal(i))
    for m in [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,40,60,80,100,120]:
        tem = []
        for i in range(120,num-1):
            tem.append(ETFdata.simpleReturn(i,m))
        feature25.append(tem)
    print(feature25.size())



