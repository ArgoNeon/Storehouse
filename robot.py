import random as rand
import math

from coordinates import Coordinates
from mail import Mail
from cell import Cell

class Robot():
    def __init__(self, robot_id, robot_row, robot_col, robot_direction, number_of_pheromone, life_time):
        self.__pheromone_value      = 1.0
        self.__base_pheromone_value = 0.0
        self.__pheromone_life_time  = life_time

        self.__id               = robot_id
        self.__coordinates      = Coordinates(robot_row, robot_col)
        self.__old_coordinates  = Coordinates(robot_row, robot_col)
        self.__direction        = robot_direction
        self.__new_direction    = robot_direction
        self.__new_coordinates  = Coordinates(robot_row, robot_col)
        self.__mail_directions  = range(number_of_pheromone)

        self.__number_of_pheromone  = number_of_pheromone
        self.__current_pheromone    = number_of_pheromone - 1
        self.__previous_pheromone   = number_of_pheromone - 1 

        self.__current_pheromone_around     = []
        self.__current_cell_types_around    = []

        self.__mail = None 
        
        self.__is_hold      = 1
        self.__is_rotate    = 0
        self.__is_wait      = 0
        self.__is_charge    = 0
        self.__is_done      = 0

        self.is_search_input    = 0
        self.is_search_output   = 0

        self.__pheromone_list = []
        self.__cell_type_list = []

        for i in range(number_of_pheromone):
            self.__pheromone_list.append(self.__base_pheromone_value)

    def getRow(self):
        return self.__coordinates.getRow()

    def getCol(self):
        return self.__coordinates.getCol()

    def getOldRow(self):
        return self.__old_coordinates.getRow()

    def getOldCol(self):
        return self.__old_coordinates.getCol()

    def isDone(self):
        return self.__is_done

    def isMail(self):
        return (self.__mail != None)

    def isWait(self):
        return self.__is_wait

    def startWait(self):
        self.__is_wait = 1

    def stopWait(self):
        self.__is_wait = 0

    def getCurrentPheromoneValue(self):
        return self.__pheromone_list[self.__current_pheromone]

    def getPreviousPheromoneValue(self):
        return self.__pheromone_list[self.__previous_pheromone]

    def getPheromoneValue(self, pheromone_id):
        return self.__pheromone_list[pheromone_id]

    def isHold(self):
        return self.__is_hold

    def startHold(self):
        self.__is_hold = 1

    def stopHold(self):
        self.__is_hold = 0

    def isRotate(self):
        return self.__is_rotate

    def checkRotate(self):
        return self.__direction != self.__new_direction

    def checkHold(self):
        return self.__coordinates != self.__new_coordinates

    def startRotate(self):
        self.__is_rotate = 1

    def stopRotate(self):
        self.__is_rotate = 0

    def chooseParticularDirection(self, direction):
        self.__new_direction = direction

        if (self.__new_direction == 0):
            self.__new_coordinates.setCoordinates(self.__coordinates.getRow() - 1, self.__coordinates.getCol())
        if (self.__new_direction == 1):
            self.__new_coordinates.setCoordinates(self.__coordinates.getRow(), self.__coordinates.getCol() + 1)
        if (self.__new_direction == 2):
            self.__new_coordinates.setCoordinates(self.__coordinates.getRow() + 1, self.__coordinates.getCol())
        if (self.__new_direction == 3):
            self.__new_coordinates.setCoordinates(self.__coordinates.getRow(), self.__coordinates.getCol() - 1)

        return self.__new_direction, self.__new_coordinates.getCoordinates() 

    def sumCurrentPheromoneAround(self):
        summ = 0
        for i in range(len(self.__current_pheromone_around)):
            summ = summ + self.__current_pheromone_around[i]

        return summ

    def chooseDirection(self):
        new_direction = rand.choices(range(4), weights=self.__current_pheromone_around)
        self.__new_direction = new_direction[0]        

        if (self.__new_direction == 0):
            self.__new_coordinates.setCoordinates(self.__coordinates.getRow() - 1, self.__coordinates.getCol())
        if (self.__new_direction == 1):
            self.__new_coordinates.setCoordinates(self.__coordinates.getRow(), self.__coordinates.getCol() + 1)
        if (self.__new_direction == 2):
            self.__new_coordinates.setCoordinates(self.__coordinates.getRow() + 1, self.__coordinates.getCol())
        if (self.__new_direction == 3):
            self.__new_coordinates.setCoordinates(self.__coordinates.getRow(), self.__coordinates.getCol() - 1)

        new_row, new_col = self.__new_coordinates.getCoordinates() 

        return self.__new_direction, new_row, new_col

    def getCurrentPheromoneAround(self):
        return self.__current_pheromone_around

    def updateCurrentPheromoneAround(self, direction, pheromone):
        self.__current_pheromone_around[direction] = pheromone

    def updateCurrentPheromonesAround(self, pheromone_up, pheromone_right, pheromone_down, pheromone_left):
        self.__current_pheromone_around.clear()
        self.__current_pheromone_around = [pheromone_up, pheromone_right, pheromone_down, pheromone_left]

    def updateCellTypeAround(self, direction, cell_type):
        self.__current_cell_types_around[direction] = cell_type

    def updateCellTypesAround(self, cell_type_up, cell_type_right, cell_type_down, cell_type_left):
        self.__current_cell_types_around.clear()
        self.__current_cell_types_around = [cell_type_up, cell_type_right, cell_type_down, cell_type_left]

    def getCurrentPheromone(self):
        return self.__current_pheromone

    def getPreviousPheromone(self):
        return self.__previous_pheromone

    def getNumberOfPheromone(self):
        return self.__number_of_pheromone

    def updateCurrentPheromon(self):
        if (self.__mail != None):
            self.__current_pheromone = self.__mail.getMailDirection()
        else:
            self.__current_pheromone = self.__number_of_pheromone - 1

    def receiveMail(self, mail):
        self.__mail = mail
        self.__pheromone_list[self.__current_pheromone] = self.__pheromone_value

        if (self.__mail != None):
            self.__previous_pheromone = self.__current_pheromone
            self.__current_pheromone = self.__mail.getMailDirection()
        else:
            self.__previous_pheromone = self.__current_pheromone
            self.__current_pheromone = self.__number_of_pheromone - 1

    def getMail(self):
        return self.__mail

    def putMail(self):
        mail = self.__mail
        self.__mail = None

        self.__pheromone_list[self.__current_pheromone] = self.__pheromone_value

        self.__previous_pheromone = self.__current_pheromone
        self.__current_pheromone = self.__number_of_pheromone - 1

        return mail

    def getMailDirection(self):
        return self.__mail.getMailDirection()

    def getID(self):
        return self.__id

    def getCoordinates(self):
        return self.__coordinates.getCoordinates()

    def getOldCoordinates(self):
        return self.__old_coordinates.getCoordinates()

    def getNewCoordinates(self):
        return self.__new_coordinates.getCoordinates()

    def getNewDirection(self):
        return self.__new_direction

    def getDirection(self):
        return self.__direction

    def RotateRight(self):
        self.__direction = (self.__direction + 1) % 4
        return self.__direction

    def RotateLeft(self):
        self.__direction = (self.__direction - 1) % 4
        return self.__direction

    def wait(self):
        pass

    def Move(self):
        old_row, old_col = self.__coordinates.getCoordinates()
        self.setOldCoordinates(old_row, old_col)

        self.stopHold()
        if (self.__direction == 0):
            self.__coordinates.setCoordinates(self.__coordinates.getRow() - 1, self.__coordinates.getCol())
        if (self.__direction == 1):
            self.__coordinates.setCoordinates(self.__coordinates.getRow(), self.__coordinates.getCol() + 1)
        if (self.__direction == 2):
            self.__coordinates.setCoordinates(self.__coordinates.getRow() + 1, self.__coordinates.getCol())
        if (self.__direction == 3):
            self.__coordinates.setCoordinates(self.__coordinates.getRow(), self.__coordinates.getCol() - 1)
        self.startHold()

        return self.__coordinates.getCoordinates()    

    def setCoordinates(self, robot_row, robot_col):
        self.__coordinates.setCoordinates(robot_row, robot_col)

    def setOldCoordinates(self, robot_row, robot_col):
        self.__old_coordinates.setCoordinates(robot_row, robot_col)

    def setNewCoordinates(self, robot_row, robot_col):
        self.__new_coordinates.setCoordinates(robot_row, robot_col)

    def setID(self, new_id):
        self.__id = new_id

    def setDirection(self, direction):
        self.__direction  = direction

    def setNewDirection(self, new_direction):
        self.__new_direction  = new_direction
        self.__is_rotate = 1

    def changeDirection(self):
        if (((self.__new_direction - self.__direction) % 4) < 3):
            self.RotateRight()
        else:
            self.RotateLeft()

        if (not self.checkRotate()):
            self.stopRotate()

        return self.__direction
    
    def getPheromoneList(self):
        return self.__pheromone_list    

    def updatePheromoneList(self):
        for i in range(len(self.__pheromone_list)):
            self.__pheromone_list[i] = (self.__pheromone_list[i] - self.__base_pheromone_value) * math.exp(- 1.0 / self.__pheromone_life_time) + self.__base_pheromone_value

    def changePheromoneListForOutputPoint(self, point_id):
        self.__pheromone_list[point_id] = self.__pheromone_value

    def changePheromoneListForInputPoint(self):
        self.__pheromone_list[self.__number_of_pheromone - 1] = self.__pheromone_value