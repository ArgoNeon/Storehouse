import math
from coordinates import Coordinates
from points import InputPoint, Outputpoint

class Cell():
    def __init__(self, cell_row, cell_col, cell_type, number_of_pheromone, life_time):
        self.__pheromone_life_time = life_time
        self.__coordinates = Coordinates(cell_row, cell_col)
        self.__type = cell_type
        self.__point_direction = -1
        self.__mail_direction = -1
        self.__robot = None
        self.__input_point = None
        self.__output_point = None

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

    def getMailDirectionForOutputPoint(self):
        return self.__output_point.getMailDirection()

    def getNumberOfReceivedMailsForOutputPoint(self):
        return self.__output_point.getNumberOfReceivedMails()

    def getNumberOfMailsForInputPoint(self):
        return self.__input_point.getNumberOfMails()

    def newMailForInputPoint(self):
        self.__input_point.newMail()

    def giveMailForInputPoint(self):
        return self.__input_point.giveMail()

    def receiveMailForOutputPoint(self, mail):
        self.__output_point.receiveMail(mail)

    def setInputPoint(self, input_point):
        self.__input_point = input_point

    def setOutputPoint(self, output_point):
        self.__output_point = output_point

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
        for i in range(len(self.__pheromone_list)):
            if (self.__type != 'b'):
                self.__pheromone_list[i] = (self.__pheromone_list[i] - 1.0) * math.exp(- 1.0 / self.__pheromone_life_time) + 1.0

    def addPheromone(self, pheromone_id, pheromone_data):
        self.__pheromone_list[pheromone_id] = self.__pheromone_list[pheromone_id] + pheromone_data