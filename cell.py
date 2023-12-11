import math
from coordinates import Coordinatess

class Cell():
    def __init__(self, cell_row, cell_col, cell_type, number_of_pheromone):
        self.__pheromone_life_time = 10
        self.__coordinates = Coordinates(cell_row, cell_col)
        self.__type = cell_type
        self.__point_direction = -1
        self.__mail_direction = -1
        self.__robot = None

        self.__is_robot = 0
        self.__is_reserved = 0

        if (cell_type == 'i'):
            self.__point_direction = 2

        if (cell_type == 'o'):
            self.__point_direction = 0

        if (cell_type == 'r'):  
            self.__is_robot = 1 
            self.__type = 'g'

        if (cell_type == 'res'):  
            self.__is_reserved = 1 
            self.__type = 'g'

        self.__pheromone_list = []

        if (cell_type != 'b'):
            for i in range(number_of_pheromone):
                self.__pheromone_list.append(1.0)
        else:
            for i in range(number_of_pheromone):
                self.__pheromone_list.append(0.0)

    def getMailDirection(self):
        return self.__mail_direction

    def setMailDirection(self, mail_direction):
        self.__mail_direction = mail_direction

    def getPointDirection(self):
        return self.__point_direction

    def setPointDirection(self, point_direction):
        self.__point_direction

    def getRow(self):
        return self.__row

    def getCol(self):
        return self.__col

    def getType(self):
        return self.__type

    def setType(self, cell_type):
        self.__type = cell_type

    def isRobot(self):
        return self.__is_robot

    def removeRobot(self):
        self.__is_robot = 0

    def setRobot(self):
        self.__is_robot = 1

    def isReserved(self):
        return self.__is_reserved

    def removeReserved(self):
        self.__is_reserved = 0

    def setReserved(self):
        self.__is_reserved = 1

    def getPheromoneList(self):
        return self.__pheromone_list   

    def getPheromone(self, number_of_pheromone):
        return  self.__pheromone_list[number_of_pheromone]

    def updatePheromoneList(self):
        for ipheromone in __pheromone_list:
            ipheromone = (ipheromone - 1.0) * math.exp(- 1.0 / self.__pheromone_life_time) + 1.0

    def addPheromone(self, pheromone_id, pheromone_data):
        self.__pheromone_list[pheromone_id] = self.__pheromone_list[pheromone_id] + pheromone_data