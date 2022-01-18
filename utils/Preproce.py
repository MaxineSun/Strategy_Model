from sklearn.preprocessing import MinMaxScaler
import torch
import numpy as np


class Preproce:
    def __init__(self, data_feature, data_targ, testSize):
        self.Data_feature = (np.array(data_feature)).T
        self.Data_targ = (np.array(data_targ)).T
        self.testSize = testSize

    def dataSplit(self):
        num = len(self.Data_targ) // self.testSize
        self.feature = self.Data_feature[:self.testSize * num, :]
        self.targ = self.Data_targ[:self.testSize * num]

        scaler = MinMaxScaler(feature_range=(-5, 5))
        self.feature = scaler.fit_transform(self.feature)
        inout = []
        L = len(self.feature)
        for i in range(L - 5 * self.testSize):
            train_seq = torch.FloatTensor(self.feature[i:i + 2 * self.testSize])
            train_label = torch.FloatTensor(self.targ[i + 2 * self.testSize:i + 3 * self.testSize])
            inout.append((train_seq, train_label))
        test_feature = torch.FloatTensor(self.feature[L - 3 * self.testSize:L - self.testSize])
        test_trag = torch.FloatTensor(self.targ[L-self.testSize:])
        return inout, test_feature, test_trag, num
