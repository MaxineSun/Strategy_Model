import networkx as nx
from utils.PullData import PullData

class ETF:
    def __init__(self, ):
        self.Graph = nx.DiGraph()

    def Create_node(self, item):
        F = 0