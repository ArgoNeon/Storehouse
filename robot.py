import random as rand
from coordinates import Coordinates
from mail import Mail
from cell import Cell

class Robot():
    def __init__(self, robot_id, robot_row, robot_col, robot_direction, number_of_pheromone):
        self.__pheromone_life_time = 5
        self.__pheromone_value = 1.0

        self.__id = robot_id
        self.__coordinates = Coordinates(robot_row, robot_col)
        self.__direction = robot_direction
        self.__new_direction = robot_direction
        self.__new_coordinates = Coordinates(robot_row, robot_col)
        self.__mail_directions = range(number_of_pheromone)

        self.__number_of_pheromone = number_of_pheromone
        self.__current_pheromone = number_of_pheromone - 1
        self.__current_pheromone_around = [1.0, 1.0, 1.0, 1.0]

        self.__mail = None 
        
        self.__is_hold = 1
        self.__is_rotate = 0
        self.__is_charge = 0

        self.is_search_input = 0
        self.is_search_output = 0

        self.__pheromone_list = []

        for i in range(number_of_pheromone):
            self.__pheromone_list.append(1.0)

    def getPheromoneValue(self):
        return self.__pheromone_value

    def isHold(self):
        return self.__is_hold

    def startHold(self):
        self.__is_hold = 1

    def startProcess(self):
        self.__is_hold = 0

    def isRotate(self):
        return self.__is_rotate

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

    def chooseDirection(self):
        self.__new_direction = rand.choices([0, 1, 2, 3], weights=self.__current_pheromone_around)

        if (self.__new_direction == 0):
            self.__new_coordinates.setCoordinates(self.__coordinates.getRow() - 1, self.__coordinates.getCol())
        if (self.__new_direction == 1):
            self.__new_coordinates.setCoordinates(self.__coordinates.getRow(), self.__coordinates.getCol() + 1)
        if (self.__new_direction == 2):
            self.__new_coordinates.setCoordinates(self.__coordinates.getRow() + 1, self.__coordinates.getCol())
        if (self.__new_direction == 3):
            self.__new_coordinates.setCoordinates(self.__coordinates.getRow(), self.__coordinates.getCol() - 1)

        return self.__new_direction, self.__new_coordinates.getCoordinates() 

    def getCurrentPheromoneAround(self):
        return self.__current_pheromone_around

    def updateCurrentPheromoneAround(self, direction, pheromone):
        self.__current_pheromone_around[direction] = pheromone

    def updateCurrentPheromonesAround(self, pheromone_up, pheromone_right, pheromone_down, pheromone_left):
        self.__current_pheromone_around.clear()
        self.__current_pheromone_around = [pheromone_up, pheromone_right, pheromone_down, pheromone_left]

    def getCurrentPheromone(self):
        return self.__current_pheromone

    def getNumberOfPheromone(self):
        return self.__number_of_pheromone

    def updateCurrentPheromon(self):
        if (self.__mail != None):
            self.__current_pheromone = self.__mail.getMailDirection()
        else:
            self.__current_pheromone = self.__number_of_pheromone - 1

    def getMail(self, mail):
        self.__mail = mail

    def putMail(self):
        self.__mail = None

    def getID(self):
        return self.__id

    def getCoordinates(self):
        return self.__coordinates.getCoordinates()

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
        self.startProcess()
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

    def setNewCoordinates(self, robot_row, robot_col):
        self.__new_coordinates.setCoordinates(robot_row, robot_col)

    def setID(self, new_id):
        self.__id = new_id

    def setDirection(self, direction):
        self.__direction  = direction

    def setNewDirection(self, new_direction):
        self.__new_direction  = new_direction

    def changeDirection(self):
        if (self.__new_direction != self.__direction):
            self.startProcess()
            self.startRotate()
            if ((self.__new_direction - self.__direction) % 4 < 3):
                self.RotateRight()
            else:
                self.RotateLeft()

            if (self.__new_direction == self.__direction):
                self.stopRotate()
                self.startHold()
        else:
            self.stopRotate()
            self.startHold()
    
    def getPheromoneList(self):
        return self.__pheromone_list    

    def updatePheromoneList(self):
        for ipheromone in __pheromone_list:
            ipheromone = (ipheromone - 1.0) * math.exp(- 1.0 / self.__pheromone_life_time) + 1.0

    def changePheromoneList(self, pheromone_id, pheromone_data):
        self.__pheromone_list[pheromone_id] = pheromone_data