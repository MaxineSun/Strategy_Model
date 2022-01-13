from utils.ReadFile import ReadFile
from utils.ETF import ETF
from utils.Preproce import Preproce
from utils.lstm import LSTM
import torch


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

    data = Preproce(feature25, yst, 250)
    inout, test_feature, test_trag = data.dataSplit()
    model = LSTM()
    loss_function = torch.nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    print(model)

    epochs = 25

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
    print(loss_function(test_pred, test_trag))





