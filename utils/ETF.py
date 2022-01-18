class ETF:
    def __init__(self, data):
        self.data = data

    def simpleReturn(self, t, m):
        r = (self.data[t] / self.data[t - m]) - 1
        return r

    def positionReturn(self, t, d):
        if d == 1:
            return self.simpleReturn(t,1)
        if d == 0:
            return self.simpleReturn(t,1)*(-1)

    def posinegaCal(self, tplusone):
        rplusone = self.simpleReturn(tplusone, 1)
        y = 0
        if (rplusone >= 0):
            y = 1
        elif (rplusone < 0):
            y = 0
        return y

    def DPR(self, t, d, commission = 0.0006):
        return self.positionReturn(t, d) - commission

    def CPR(self, DPR, t):
        res = []
        pro = [1]
        for i in range(t):
            p = pro[-1] * (DPR[i] + 1)
            pro.append(p)
            res.append(p - 1)
        return res

