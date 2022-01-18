import torch


class LSTM(torch.nn.Module):
    def __init__(self, input_size=25, hidden_layer_size=100, output_size=250):
        super().__init__()
        self.hidden_layer_size = hidden_layer_size

        self.lstm = torch.nn.LSTM(input_size, hidden_layer_size)

        self.linear = torch.nn.Linear(hidden_layer_size, output_size)

        self.hidden_cell = (torch.zeros(1, 1, self.hidden_layer_size),
                            torch.zeros(1, 1, self.hidden_layer_size))

    def forward(self, input_seq):
        lstm_out, self.hidden_cell = self.lstm(input_seq.view(len(input_seq), 1, -1), self.hidden_cell)
        S = torch.nn.Sigmoid()
        predictions = S(self.linear(lstm_out.view(len(input_seq), -1)))
        return predictions[-1]
