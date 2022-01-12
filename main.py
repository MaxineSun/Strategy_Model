from utils.ReadFile import ReadFile
from utils.ETF import ETF

if __name__ == '__main__':
    File = ReadFile('S&P_TR.xlsx')
    data = File.ReadData()
    d = data['B']
    num = len(d)
    close = [item.value for item in d[1:num]]
    print(close[0])
    yst = []
    ETFdata = ETF(close)
    for i in range(1,num-1):
        yst.append(ETFdata.posinegaCal(i))


