from openpyxl import *


class ReadFile:
    def __init__(self, dirpath):
        self.Dirpath = dirpath

    def ReadData(self):
        wb = load_workbook(self.Dirpath)
        ws = wb.active
        return ws
