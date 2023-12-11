class Coordinates():
    def __init__(self, row, col):
        self.__row = row
        self.__col = col
    
    def getCoordinates(self):
        return self.__row, self.__col

    def getRow(self):
        return self.__row

    def getCol(self):
        return self.__col

    def setCoordinates(self, row, col):
        self.__row = row
        self.__col = col

    def setRow(self, row):
        self.__row = row

    def setCol(self, col):
        self.__col = col 