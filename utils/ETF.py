class ETF:
    def __init__(self, data):
        self.data = data

    def simpleReturn(self, t, m):
        self.data[t - m]
        r = (self.data[t] / self.data[t - m]) - 1
        return r

    def posinegaCal(self, tplusone):
        rplusone = self.simpleReturn(tplusone, 1)
        y = 0
        if (rplusone >= 0):
            y = 1
        elif (rplusone < 0):
            y = 0
        return y
