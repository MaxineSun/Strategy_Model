from utils.ReadFile import ReadFile
from utils.ETF import ETF
from utils.Preproce import Preproce
from utils.lstm import LSTM
import torch
import matplotlib.pyplot as plt

if __name__ == '__main__':
    ## read the excel data
    File = ReadFile('S&P_TR.xlsx')
    data = File.ReadData()
    d = data['B']
    num = len(d)
    close = [item.value for item in d[1:num]]

    ## data preprocess
    yst = []
    feature25 = []
    ETFdata = ETF(close)
    for i in range(120, num - 1):
        yst.append(ETFdata.posinegaCal(i))
    for m in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 40, 60, 80, 100, 120]:
        tem = []
        for i in range(120, num - 1):
            tem.append(ETFdata.simpleReturn(i, m))
        feature25.append(tem)
    data = Preproce(feature25, yst, 250)
    inout, test_feature, test_trag, num = data.dataSplit()

    ## build the model
    model = LSTM()
    loss_function = torch.nn.BCELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    print(model)

    ## train the model
    epochs = 30
    for i in range(epochs):
        for seq, labels in inout:
            optimizer.zero_grad()
            model.hidden_cell = (torch.zeros(1, 1, model.hidden_layer_size),
                                 torch.zeros(1, 1, model.hidden_layer_size))

            y_pred = model(seq)
            single_loss = loss_function(y_pred, labels)
            single_loss.backward()
            optimizer.step()

        print(f'epoch: {i:3} loss: {single_loss.item():10.8f}')
        print(torch.min(y_pred))
        print(torch.max(y_pred))
        print(torch.mean(y_pred))

    print(f'epoch: {i:3} loss: {single_loss.item():10.10f}')

    model.eval()
    with torch.no_grad():
        model.hidden = (torch.zeros(1, 1, model.hidden_layer_size),
                        torch.zeros(1, 1, model.hidden_layer_size))

        test_pred = model(test_feature)
    test_pred = torch.where(test_pred > 0.5, 1, 0)

    ## evaluation of predict result
    print("")
    TP = 0
    FP = 0
    FN = 0
    TN = 0
    TPR = []
    FPR = []
    PRE = []
    REC = []
    test_pred = list(test_pred)
    test_trag = list(test_trag)
    for i in range(250):
        if test_pred[i] == 1:
            if test_trag[i] == 1:
                TP += 1
            else:
                FP += 1
        if test_pred[i] == 0:
            if test_trag[i] == 1:
                FN += 1
            else:
                TN += 1
        TPR.append(TP / max((TP + FN), 0.000001))
        FPR.append(FP / max((FP + TN), 0.000001))
        PRE.append(TP / max((TP + FP), 0.000001))
        # REC.append(TP/(TP+FN))
    acc = (TP + TN) / 250
    prec = TP / max((TP + FP), 0.000001)
    recall = TP / max((TP + FN), 0.00001)
    f1 = 2 * prec * recall / (max(prec + recall, 0.000001))
    plt.plot(FPR, TPR)
    plt.title("ROC_Curve")
    plt.xlabel("FPR")
    plt.ylabel("TPR")
    plt.show()
    plt.plot(PRE, TPR)
    plt.title("PR_Curve")
    plt.xlabel("PRE")
    plt.ylabel("REC")
    plt.show()

    ## backtest simulation
    dailyReturn = []
    for i in range(250):
        d = ETFdata.positionReturn(120 + 250 * (num - 1) + i, test_pred[i - 1])
        dailyReturn.append(d)
    cumulatReturn = ETFdata.CPR(dailyReturn, 250)
    plt.plot(cumulatReturn)
    plt.xlabel("Cumulative portfolio return")
    plt.ylabel("time")
    plt.show()
