from utils.ReadFile import ReadFile

if __name__ == '__main__':
    File = ReadFile('Market_relevant_data.xlsx')
    data = File.ReadData()
    print(type(data))
