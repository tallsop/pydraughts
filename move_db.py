#Move database
class DataBase:
    def __init__(self):
        self.records = []

    def addRecord(self, rec):
        self.records.append(rec)

    def sortRecords(self):
        #Since it will be nearly sorted insertion sort will be used.
        for i = 1 in range(len(self.records)):
            value = self.records[i]
            placement = i

            while placement > 0 and value < self.records[placement-1]:
                self.records[placement] = self.records[placement-1]
                placement -= 1

            

class Record:
    def __init__(self):
        self.boardNode = None
        self.timesUsed = 0

    def incCounter(self):
        self.timesUsed += 1

    def getMove(self):
        return self.boardNode
        
